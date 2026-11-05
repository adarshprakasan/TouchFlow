import importlib.util
import json
import math
from pathlib import Path
import threading
import time
import unittest
from unittest.mock import patch
import urllib.request
import urllib.error

spec=importlib.util.spec_from_file_location('touchflow',Path(__file__).parents[1]/'companion'/'touchflow.py')
app=importlib.util.module_from_spec(spec); spec.loader.exec_module(app)

class Validation(unittest.TestCase):
    def test_input_structure(self):
        self.assertEqual(app.C.sizeof(app.INPUT),40 if app.C.sizeof(app.C.c_void_p)==8 else 28)
    def test_bounded_finite_movement(self):
        for value in (float('nan'),float('inf'),501,True,'1'):
            self.assertFalse(app.validate({'kind':'move','x':value,'y':0}))
        self.assertTrue(app.validate({'kind':'move','x':-500,'y':0}))
    def test_unicode_and_limits(self):
        self.assertTrue(app.validate({'kind':'text','text':'Hello \U0001F44B'}))
        self.assertFalse(app.validate({'kind':'text','text':'x'*257}))
        self.assertFalse(app.validate({'kind':'text','text':'\ud800'}))
    def test_allowlist(self):
        self.assertFalse(app.validate({'kind':'key','key':'RunAnything'}))
        self.assertFalse(app.validate({'kind':'shell','command':'ignored'}))
        self.assertTrue(app.validate({'kind':'release'}))

class ConnectionAndQR(unittest.TestCase):
    def test_idle_session_never_expires(self):
        app.state.update(token='still-approved',last=1,pending=None)
        with patch.object(app,'release') as release:
            self.assertTrue(app.connection_safety(now=60*60*24*365))
            release.assert_called_once()
        self.assertEqual(app.state['token'],'still-approved')
    def test_safety_drops_stale_drag_without_disconnect(self):
        app.state.update(token='still-approved',last=1,pending=None)
        app.jobs.put(('input',('still-approved',{'kind':'drag','down':True})))
        with patch.object(app,'release') as release:
            app.connection_safety(now=20)
            release.assert_called_once()
        self.assertTrue(app.jobs.empty())
        self.assertEqual(app.state['token'],'still-approved')
    def test_recent_connection_keeps_commands(self):
        app.state.update(token='still-approved',last=15,pending=None)
        app.jobs.put(('input',('still-approved',{'kind':'move','x':1,'y':2})))
        with patch.object(app,'release') as release:
            self.assertFalse(app.connection_safety(now=16));release.assert_not_called()
        self.assertEqual(app.jobs.get_nowait()[1][1]['kind'],'move')
    def test_pairing_approval_expiry_is_separate(self):
        app.state.update(token='still-approved',last=100,pending={'time':0})
        with patch.object(app,'release'): app.connection_safety(now=100)
        self.assertIsNone(app.state['pending'])
        self.assertEqual(app.state['token'],'still-approved')
    def test_qr_contains_only_phone_url(self):
        with patch.object(app.qrcode,'QRCode',wraps=app.qrcode.QRCode) as factory:
            matrix=app.qr_matrix('192.0.2.10')
            self.assertGreater(len(matrix),20)
            self.assertEqual(len(matrix),len(matrix[0]))
            self.assertEqual(app.phone_url('192.0.2.10'),f'http://192.0.2.10:{app.PORT}')
            self.assertTrue(all(not any(row) for row in matrix[:4]))
            # Verify the encoder receives only the URL, never a secret/code.
        with patch.object(app.qrcode,'QRCode') as factory:
            app.qr_matrix('192.0.2.10')
            factory.return_value.add_data.assert_called_once_with(app.phone_url('192.0.2.10'))

class Protocol(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=app.Server(('127.0.0.1',0),app.Handler)
        cls.previous_port=app.PORT; app.PORT=cls.server.server_port
        threading.Thread(target=cls.server.serve_forever,daemon=True).start()
        cls.base=f'http://127.0.0.1:{app.PORT}'
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); app.PORT=cls.previous_port
    def setUp(self):
        with app.lock:
            app.state.update(code='ABCD1234',expires=time.monotonic()+120,pending=None,token=None,last=0,seq=0,paused=False)
            app.attempts.clear()
        while not app.jobs.empty(): app.jobs.get_nowait()
    def request(self,path,body,origin=True,host=None):
        headers={'Content-Type':'application/json'}
        if origin: headers['Origin']=self.base
        if host: headers['Host']=host
        req=urllib.request.Request(self.base+path,json.dumps(body).encode(),headers)
        try:
            with urllib.request.urlopen(req,timeout=2) as response: return response.status,json.load(response)
        except urllib.error.HTTPError as e: return e.code,json.load(e)
    def test_pairing_requires_approval(self):
        status,result=self.request('/pair',{'code':'ABCD1234'}); self.assertEqual(status,200)
        self.assertTrue(self.request('/status',{'ticket':result['ticket']})[1]['waiting'])
        self.assertEqual(self.request('/input',{'token':'no','seq':1,'kind':'click','button':'left'})[0],401)
        with app.lock:
            app.state['pending']['approved']=True; app.state['token']='test-token'
        self.assertEqual(self.request('/status',{'ticket':result['ticket']})[1]['token'],'test-token')
        self.assertEqual(self.request('/status',{'ticket':result['ticket']})[0],403)
    def test_expiry_origin_host_and_rate_limit(self):
        self.assertEqual(self.request('/pair',{'code':'ABCD1234'},origin=False)[0],403)
        self.assertEqual(self.request('/pair',{'code':'ABCD1234'},host='untrusted.invalid')[0],403)
        app.state['expires']=0
        self.assertEqual(self.request('/pair',{'code':'ABCD1234'})[0],403)
        for _ in range(4): self.request('/pair',{'code':'wrong'})
        self.assertEqual(self.request('/pair',{'code':'wrong'})[0],429)
    def test_sequence_pause_and_disconnect(self):
        app.state['token']='test-token'
        command={'token':'test-token','seq':1,'kind':'move','x':2,'y':0}
        self.assertEqual(self.request('/input',command)[0],200)
        self.assertEqual(self.request('/input',command)[0],400)
        # Only queued; no SendInput or GUI event loop is invoked.
        self.assertEqual(app.jobs.get_nowait()[1][1]['kind'],'move')
        app.state['paused']=True
        self.assertEqual(self.request('/input',{**command,'seq':2})[0],423)
        self.assertEqual(self.request('/input',{'token':'test-token','seq':3,'kind':'heartbeat'})[0],200)
        self.assertEqual(self.request('/disconnect',{'token':'test-token'})[0],200)
        self.assertIsNone(app.state['token'])
        self.assertEqual(self.request('/input',{**command,'seq':4})[0],401)

if __name__=='__main__': unittest.main()
