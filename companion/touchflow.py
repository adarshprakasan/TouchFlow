"""TouchFlow Windows companion. Python 3.12+, standard library only."""
import ctypes as C
from ctypes import wintypes as W
import http.server, json, secrets, socket, threading, time, queue
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

PORT = 8765
ROOT = Path(__file__).resolve().parent
jobs = queue.Queue(maxsize=512)
lock = threading.Lock()
attempts = {}
state = {'code': secrets.token_hex(4).upper(), 'expires': time.monotonic()+120,
         'pending': None, 'token': None, 'last': 0, 'seq': 0, 'paused': False}
user32 = C.WinDLL('user32', use_last_error=True)
class MI(C.Structure):
    _fields_=[('dx',W.LONG),('dy',W.LONG),('mouseData',W.DWORD),('dwFlags',W.DWORD),('time',W.DWORD),('extra',C.c_size_t)]
class KI(C.Structure):
    _fields_=[('vk',W.WORD),('scan',W.WORD),('flags',W.DWORD),('time',W.DWORD),('extra',C.c_size_t)]
class UNION(C.Union):
    _fields_=[('mi',MI),('ki',KI)]
class INPUT(C.Structure):
    _anonymous_=('u',)
    _fields_=[('type',W.DWORD),('u',UNION)]
user32.SendInput.argtypes=[W.UINT,C.POINTER(INPUT),C.c_int]
user32.SendInput.restype=W.UINT

def emit(item):
    if user32.SendInput(1,C.byref(item),C.sizeof(INPUT)) != 1:
        raise RuntimeError('Windows blocked input. Elevated apps and secure screens are unsupported.')
def mouse(flags,dx=0,dy=0,data=0):
    item=INPUT(); item.type=0; item.mi=MI(dx,dy,data & 0xffffffff,flags,0,0); emit(item)
def key(vk=0,scan=0,flags=0):
    item=INPUT(); item.type=1; item.ki=KI(vk,scan,flags,0,0); emit(item)
held=False

def release():
    global held
    if held:
        mouse(4); held=False

def command(body):
    global held
    kind=body['kind']
    if kind=='move': mouse(1,int(body['x']),int(body['y']))
    elif kind=='scroll': mouse(0x800,data=int(body['y']))
    elif kind=='click':
        down,up=(2,4) if body['button']=='left' else (8,16)
        mouse(down); mouse(up)
    elif kind=='drag':
        if body['down'] and not held: mouse(2); held=True
        elif not body['down']: release()
    elif kind=='text':
        raw=body['text'].encode('utf-16-le')
        for i in range(0,len(raw),2):
            scan=int.from_bytes(raw[i:i+2],'little'); key(scan=scan,flags=4); key(scan=scan,flags=6)
    elif kind=='key':
        vk={'Enter':13,'Backspace':8,'Tab':9,'Escape':27,'ArrowLeft':37,'ArrowUp':38,'ArrowRight':39,'ArrowDown':40}[body['key']]
        key(vk); key(vk,flags=2)
    elif kind=='release': release()

def validate(b):
    k=b.get('kind')
    if k=='move':
        return all(type(b.get(n)) in (int,float) and abs(b[n])<=500 for n in ('x','y'))
    if k=='scroll': return type(b.get('y')) in (int,float) and abs(b['y'])<=1200
    if k=='click': return b.get('button') in ('left','right')
    if k=='drag': return type(b.get('down')) is bool
    if k=='text': return isinstance(b.get('text'),str) and 0<len(b['text'])<=256
    if k=='key': return b.get('key') in ('Enter','Backspace','Tab','Escape','ArrowLeft','ArrowRight','ArrowUp','ArrowDown')
    return k in ('release','heartbeat')

class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version='HTTP/1.1'
    def log_message(self,*args): pass
    def reply(self,status,data):
        raw=json.dumps(data).encode(); self.send_response(status)
        self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(raw)))
        self.send_header('Cache-Control','no-store'); self.send_header('X-Content-Type-Options','nosniff'); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        if self.path not in ('/','/phone.html'): return self.reply(404,{'error':'Not found'})
        raw=(ROOT/'phone.html').read_bytes(); self.send_response(200)
        self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(raw)))
        self.send_header('Cache-Control','no-store'); self.send_header('X-Frame-Options','DENY')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'")
        self.end_headers(); self.wfile.write(raw)
    def do_POST(self):
        # No CORS. Require a same-origin browser request and JSON to block cross-site forms.
        if self.headers.get('Origin') != 'http://'+self.headers.get('Host',''):
            return self.reply(403,{'error':'Origin rejected'})
        if self.headers.get('Content-Type')!='application/json': return self.reply(415,{'error':'JSON required'})
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=4096: return self.reply(413,{'error':'Message too large'})
            b=json.loads(self.rfile.read(size))
            if not isinstance(b,dict): raise ValueError()
        except (ValueError,TypeError): return self.reply(400,{'error':'Invalid message'})
        now=time.monotonic()
        with lock:
            if self.path=='/pair':
                ip=self.client_address[0]
                recent=[t for t in attempts.get(ip,[]) if now-t<60]
                if len(recent)>=5: return self.reply(429,{'error':'Too many pairing attempts. Wait one minute.'})
                recent.append(now); attempts[ip]=recent
                if state['token'] or state['pending']: return self.reply(409,{'error':'Another phone is connected or awaiting approval'})
                if now>state['expires'] or not secrets.compare_digest(str(b.get('code','')).upper(),state['code']):
                    return self.reply(403,{'error':'Code is incorrect or expired. Generate a new one on the computer.'})
                ticket=secrets.token_urlsafe(32)
                state['pending']={'ticket':ticket,'ip':self.client_address[0],'time':now,'approved':False}
                return self.reply(200,{'ticket':ticket})
            if self.path=='/status':
                pending=state['pending']
                if not pending or not secrets.compare_digest(str(b.get('ticket','')),pending['ticket']): return self.reply(403,{'error':'Pairing was rejected or expired'})
                if pending['approved']:
                    token=state['token']; state['pending']=None
                    return self.reply(200,{'token':token})
                return self.reply(200,{'waiting':True})
            token=str(b.get('token',''))
            if not state['token'] or not secrets.compare_digest(token,state['token']): return self.reply(401,{'error':'Disconnected. Pair again.'})
            if self.path=='/disconnect':
                state['token']=None; jobs.put_nowait(('release',None)); return self.reply(200,{'ok':True})
            if self.path!='/input': return self.reply(404,{'error':'Not found'})
            if state['paused']: return self.reply(423,{'error':'Input is paused on the computer'})
            seq=b.get('seq')
            if type(seq) is not int or seq<=state['seq'] or not validate(b): return self.reply(400,{'error':'Invalid command'})
            state['seq']=seq; state['last']=now
            if b['kind']!='heartbeat':
                try: jobs.put_nowait(('input',(token,b)))
                except queue.Full: return self.reply(429,{'error':'Too many commands'})
        self.reply(200,{'ok':True})

class Server(http.server.ThreadingHTTPServer):
    daemon_threads=True
    allow_reuse_address=True

def addresses():
    found=set()
    try:
        for info in socket.getaddrinfo(socket.gethostname(),None,socket.AF_INET):
            if not info[4][0].startswith('127.'): found.add(info[4][0])
    except OSError: pass
    return sorted(found)

root=tk.Tk(); root.title('TouchFlow Windows Companion'); root.geometry('570x510'); root.configure(bg='#101a24')
def label(text,size=12,color='#edf4f3'):
    w=tk.Label(root,text=text,font=('Segoe UI',size),fg=color,bg='#101a24',wraplength=530,justify='left'); w.pack(anchor='w',padx=22,pady=7); return w
label('TouchFlow',26); label('Windows companion • trusted private Wi-Fi only',11,'#80e1d1')
label('On your phone, open one of these addresses:')
url=label('\n'.join(f'http://{ip}:{PORT}' for ip in addresses()) or 'No network address found. Connect to Wi-Fi.',12,'#80e1d1')
code=label('Pairing code: '+state['code'],20)
status=label('Waiting for a phone. Codes expire after 2 minutes.',11)
frame=tk.Frame(root,bg='#101a24'); frame.pack(fill='x',padx=22,pady=10)
def revoke():
    with lock:
        state['token']=None; state['pending']=None; state['seq']=0
    release(); status.configure(text='Disconnected. Generate a new pairing code.')
def new_code():
    revoke()
    with lock: state['code']=secrets.token_hex(4).upper(); state['expires']=time.monotonic()+120
    code.configure(text='Pairing code: '+state['code']); status.configure(text='Waiting for a phone. Code expires in 2 minutes.')
def pause():
    with lock: state['paused']=not state['paused']; paused=state['paused']
    release(); pause_btn.configure(text='Resume' if paused else 'Pause input'); status.configure(text='Input paused' if paused else 'Input resumed')
for text,fn in [('New pairing code',new_code),('Disconnect phone',revoke)]: tk.Button(frame,text=text,command=fn,padx=10,pady=8).pack(side='left',padx=(0,8))
pause_btn=tk.Button(frame,text='Pause input',command=pause,padx=10,pady=8); pause_btn.pack(side='left')
label('Keep this window open. Close it to stop remote control. Input cannot reach administrator apps or Windows security screens.',10,'#9aadb3')
server=None
try:
    server=Server(('0.0.0.0',PORT),Handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
except OSError as e:
    messagebox.showerror('TouchFlow cannot start',str(e)); root.destroy(); raise SystemExit(1)
asked=None

def tick():
    global asked
    now=time.monotonic()
    with lock:
        pending=state['pending']
        if pending and now-pending['time']>60: state['pending']=None; pending=None
        if state['token'] and now-state['last']>8:
            state['token']=None; release(); status.configure(text='Phone timed out. Pair again.')
    if pending and not pending['approved'] and asked!=pending['ticket']:
        asked=pending['ticket']
        approved=messagebox.askyesno('Approve phone?',f"Allow phone at {pending['ip']} to control this computer?\n\nApprove only your own phone.")
        with lock:
            if state['pending'] is pending:
                if approved:
                    pending['approved']=True; state['token']=secrets.token_urlsafe(32); state['last']=time.monotonic(); state['seq']=0
                    status.configure(text='Phone connected — input enabled')
                else: state['pending']=None
    for _ in range(64):
        try: kind,payload=jobs.get_nowait()
        except queue.Empty: break
        try:
            if kind=='release': release()
            else:
                token,b=payload
                with lock: allowed=token==state['token'] and not state['paused']
                if allowed: command(b)
        except Exception as e: status.configure(text=str(e)); revoke()
    root.after(15,tick)

def close():
    revoke()
    if server: threading.Thread(target=server.shutdown,daemon=True).start()
    root.destroy()
root.protocol('WM_DELETE_WINDOW',close); root.after(50,tick); root.mainloop()
