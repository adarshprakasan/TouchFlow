"""TouchFlow Windows companion. Python 3.12+ with qrcode."""
import ctypes as C
from ctypes import wintypes as W
import http.server, json, secrets, socket, threading, time, queue, sys, math
import tkinter as tk
from tkinter import messagebox, ttk
import qrcode
from pathlib import Path

VERSION = "0.2.0"
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
        return all(type(b.get(n)) in (int,float) and math.isfinite(b[n]) and abs(b[n])<=500 for n in ('x','y'))
    if k=='scroll': return type(b.get('y')) in (int,float) and math.isfinite(b['y']) and abs(b['y'])<=1200
    if k=='click': return b.get('button') in ('left','right')
    if k=='drag': return type(b.get('down')) is bool
    if k=='text': return isinstance(b.get('text'),str) and 0<len(b['text'])<=256 and not any(0xD800<=ord(c)<=0xDFFF for c in b['text'])
    if k=='key': return b.get('key') in ('Enter','Backspace','Tab','Escape','ArrowLeft','ArrowRight','ArrowUp','ArrowDown')
    return k in ('release','heartbeat')

class Handler(http.server.BaseHTTPRequestHandler):
    protocol_version='HTTP/1.1'
    def setup(self):
        super().setup()
        self.connection.settimeout(5)
    def valid_host(self):
        host=self.headers.get('Host','')
        return host in {f'{ip}:{PORT}' for ip in addresses()+['127.0.0.1','localhost']}

    def log_message(self,*args): pass
    def reply(self,status,data):
        raw=json.dumps(data).encode(); self.send_response(status)
        self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(raw)))
        self.send_header('Cache-Control','no-store'); self.send_header('X-Content-Type-Options','nosniff'); self.end_headers(); self.wfile.write(raw)
    def do_GET(self):
        if not self.valid_host(): return self.reply(403,{'error':'Host rejected'})
        assets={'/':('phone.html','text/html; charset=utf-8'),'/phone.html':('phone.html','text/html; charset=utf-8'),'/gestures.js':('gestures.js','text/javascript; charset=utf-8')}
        if self.path not in assets: return self.reply(404,{'error':'Not found'})
        name,content_type=assets[self.path]
        raw=(ROOT/name).read_bytes(); self.send_response(200)
        self.send_header('Content-Type',content_type); self.send_header('Content-Length',str(len(raw)))
        self.send_header('Cache-Control','no-store'); self.send_header('X-Frame-Options','DENY')
        self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'")
        self.end_headers(); self.wfile.write(raw)
    def do_POST(self):
        if not self.valid_host(): return self.reply(403,{'error':'Host rejected'})
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
                if now>state['expires'] or not secrets.compare_digest(str(b.get('code','')).upper().encode('utf-8'),state['code'].encode('ascii')):
                    return self.reply(403,{'error':'Code is incorrect or expired. Generate a new one on the computer.'})
                ticket=secrets.token_urlsafe(32)
                state['pending']={'ticket':ticket,'ip':self.client_address[0],'time':now,'approved':False}
                return self.reply(200,{'ticket':ticket})
            if self.path=='/status':
                pending=state['pending']
                if not pending or not secrets.compare_digest(str(b.get('ticket','')).encode('utf-8'),pending['ticket'].encode('ascii')): return self.reply(403,{'error':'Pairing was rejected or expired'})
                if pending['approved']:
                    token=state['token']; state['pending']=None
                    return self.reply(200,{'token':token})
                return self.reply(200,{'waiting':True})
            token=str(b.get('token',''))
            if not state['token'] or not secrets.compare_digest(token.encode('utf-8'),state['token'].encode('ascii')): return self.reply(401,{'error':'Disconnected. Pair again.'})
            if self.path=='/disconnect':
                state['token']=None
                try: jobs.put_nowait(('release',None))
                except queue.Full: pass
                return self.reply(200,{'ok':True})
            if self.path!='/input': return self.reply(404,{'error':'Not found'})
            seq=b.get('seq')
            if type(seq) is not int or seq<=state['seq'] or not validate(b): return self.reply(400,{'error':'Invalid command'})
            state['last']=now
            if state['paused'] and b['kind'] not in ('heartbeat','release'): return self.reply(423,{'error':'Input is paused on the computer'})
            state['seq']=seq
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

def connection_safety(now=None):
    """Release stale held input without expiring the approved session."""
    now=time.monotonic() if now is None else now
    with lock:
        if state['pending'] and now-state['pending']['time']>60:
            state['pending']=None
        stale=not state['token'] or now-state['last']>8
    if stale:
        while True:
            try: jobs.get_nowait()
            except queue.Empty: break
        release()
    return stale

def phone_url(address):
    return f'http://{address}:{PORT}'

def qr_matrix(address):
    code=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,border=4)
    code.add_data(phone_url(address)); code.make(fit=True)
    return code.get_matrix()

def qr_image(master,address):
    matrix=qr_matrix(address)
    scale=max(1,220//len(matrix)); width=len(matrix)*scale
    # Native Tk PPM image: no Pillow dependency and no external QR service.
    pixels=bytearray()
    for row in matrix:
        line=b''.join((b'\x00\x00\x00' if dark else b'\xff\xff\xff')*scale for dark in row)
        pixels.extend(line*scale)
    return tk.PhotoImage(master=master,data=f'P6\n{width} {width}\n255\n'.encode()+pixels,format='PPM')

def main():
    root=tk.Tk(); root.title('TouchFlow Windows Companion'); root.geometry('680x640'); root.minsize(650,640); root.configure(bg='#101a24')
    def label(text,size=12,color='#edf4f3'):
        w=tk.Label(root,text=text,font=('Segoe UI',size),fg=color,bg='#101a24',wraplength=530,justify='left'); w.pack(anchor='w',padx=22,pady=7); return w
    label('TouchFlow '+VERSION+' alpha',26); label('Windows companion - trusted private Wi-Fi only',11,'#80e1d1')
    label('Scan the QR code with your phone camera, then open the link.',11)
    network=tk.Frame(root,bg='#101a24'); network.pack(fill='x',padx=22,pady=8)
    details=tk.Frame(network,bg='#101a24'); details.pack(side='left',fill='both',expand=True,padx=(0,12))
    tk.Label(details,text='Choose your Wi-Fi address',bg='#101a24',fg='#edf4f3',font=('Segoe UI',11)).pack(anchor='w',pady=8)
    ips=addresses()
    selected=tk.StringVar(value=ips[0] if ips else '')
    choices=ttk.Combobox(details,textvariable=selected,values=ips,state='readonly',width=26)
    choices.pack(anchor='w',fill='x')
    url=tk.Label(details,text='',bg='#101a24',fg='#80e1d1',wraplength=330,font=('Segoe UI',12)); url.pack(anchor='w',pady=12)
    tk.Label(details,text='QR opens the local phone controls.\nEnter the pairing code and approve\nyour phone on this PC.',justify='left',bg='#101a24',fg='#9aadb3',font=('Segoe UI',10)).pack(anchor='w')
    qr_label=tk.Label(network,bg='white',padx=0,pady=0); qr_label.pack(side='right')
    def refresh_qr(_event=None):
        if selected.get():
            url.configure(text=phone_url(selected.get()))
            image=qr_image(root,selected.get()); qr_label.configure(image=image); qr_label.image=image
        else: url.configure(text='No network address found. Connect to Wi-Fi and restart TouchFlow.')
    choices.bind('<<ComboboxSelected>>',refresh_qr)
    refresh_qr()
    code=label('Pairing code: '+state['code'],20)
    status=label('Waiting for a phone. Codes expire after 2 minutes.',11)
    frame=tk.Frame(root,bg='#101a24'); frame.pack(fill='x',padx=22,pady=10)
    def clear_queue():
        while True:
            try: jobs.get_nowait()
            except queue.Empty: break

    def revoke():
        with lock:
            state['token']=None; state['pending']=None; state['seq']=0
        clear_queue(); release(); status.configure(text='Disconnected. Generate a new pairing code.')
    def new_code():
        revoke()
        with lock: state['code']=secrets.token_hex(4).upper(); state['expires']=time.monotonic()+120
        code.configure(text='Pairing code: '+state['code']); status.configure(text='Waiting for a phone. Code expires in 2 minutes.')
    def pause():
        with lock: state['paused']=not state['paused']; paused=state['paused']
        clear_queue(); release(); pause_btn.configure(text='Resume' if paused else 'Pause input'); status.configure(text='Input paused' if paused else 'Input resumed')
    for text,fn in [('New pairing code',new_code),('Disconnect phone',revoke)]: tk.Button(frame,text=text,command=fn,padx=10,pady=8).pack(side='left',padx=(0,8))
    pause_btn=tk.Button(frame,text='Pause input',command=pause,padx=10,pady=8); pause_btn.pack(side='left')
    label('No session time limit. Pause or Disconnect to stop input; close this window to end the session. Trusted private Wi-Fi only. Elevated apps and security screens are unsupported.',10,'#9aadb3')
    server=None
    try:
        server=Server(('0.0.0.0',PORT),Handler)
        threading.Thread(target=server.serve_forever,daemon=True).start()
    except OSError as e:
        messagebox.showerror('TouchFlow cannot start',str(e)); root.destroy(); raise SystemExit(1)
    asked=None

    def tick():
        nonlocal asked
        connection_safety()
        with lock: pending=state['pending']
        if pending and not pending['approved'] and asked!=pending['ticket']:
            asked=pending['ticket']
            approved=messagebox.askyesno('Approve phone?',f"Allow phone at {pending['ip']} to control this computer?\n\nApprove only your own phone.")
            with lock:
                if state['pending'] is pending:
                    if approved:
                        pending['approved']=True; state['token']=secrets.token_urlsafe(32); state['last']=time.monotonic(); state['seq']=0
                        status.configure(text='Phone connected - input enabled')
                    else: state['pending']=None
        for _ in range(64):
            try: kind,payload=jobs.get_nowait()
            except queue.Empty: break
            try:
                if kind=='release': release()
                else:
                    token,b=payload
                    with lock: allowed=token==state['token'] and (not state['paused'] or b['kind']=='release')
                    if allowed: command(b)
            except Exception as e: status.configure(text=str(e)); revoke()
        root.after(15,tick)

    def close():
        revoke()
        if server: threading.Thread(target=server.shutdown,daemon=True).start()
        root.destroy()
    root.protocol('WM_DELETE_WINDOW',close); root.after(50,tick); root.mainloop()

if __name__ == '__main__':
    if len(sys.argv)==3 and sys.argv[1]=='--self-test':
        result={'version':VERSION,'input_structure_bytes':C.sizeof(INPUT),'bundled_phone':(ROOT/'phone.html').is_file()}
        assert result['input_structure_bytes']==(40 if C.sizeof(C.c_void_p)==8 else 28)
        assert result['bundled_phone']
        assert (ROOT/'gestures.js').is_file()
        assert validate({'kind':'move','x':2,'y':-1})
        assert not validate({'kind':'move','x':float('nan'),'y':0})
        window=tk.Tk(); window.withdraw(); image=qr_image(window,'192.0.2.1'); assert image.width()>100; window.update(); window.destroy()
        result['qr_render']='passed'; result['bundled_gestures']=True
        result['tkinter']='passed'; result['status']='passed'
        Path(sys.argv[2]).write_text(json.dumps(result,indent=2))
    else:
        main()
