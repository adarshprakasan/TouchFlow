const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const html=fs.readFileSync(require('node:path').join(__dirname,'../companion/phone.html'),'utf8');
function harness(){
  const elements=new Map(),requests=[],timers=[],documentEvents={},windowEvents={};
  function element(id){if(!elements.has(id))elements.set(id,{id,value:id==='speed'?'1.5':'',textContent:'',classList:{add(){},remove(){},toggle(){}},listeners:{},addEventListener(name,fn,options){this.listeners[name]={fn,options}},append(){},setPointerCapture(){}});return elements.get(id)}
  let fail=null;
  const context=vm.createContext({console,AbortController,setTimeout,clearTimeout,TouchFlowTrackpad:require('../companion/gestures.js'),
    setInterval(fn){timers.push(fn)},window:{addEventListener(name,fn){windowEvents[name]=fn}},
    document:{hidden:false,getElementById:element,createElement:()=>element(Symbol()),addEventListener(name,fn){documentEvents[name]=fn}},
    fetch:async(path,options)=>{const body=JSON.parse(options.body);requests.push({path,...body});if(fail)throw fail;return {ok:true,json:async()=>({ok:true})}}
  });
  vm.runInContext(html.match(/<script>([\s\S]*?)<\/script>/)[1],context);
  const run=code=>vm.runInContext(code,context);
  run('token="session-token";seq=0');
  function pointer(name,id,x,y){let prevented=false;element('pad').listeners[name].fn({pointerId:id,clientX:x,clientY:y,cancelable:true,preventDefault(){prevented=true}});return prevented}
  return {elements,requests,run,pointer,documentEvents,windowEvents,context,setFail:error=>fail=error,settle:()=>run('chain')};
}
test('touchpad prevents Safari selection without disabling keyboard editing',()=>{
  assert.match(html,/-webkit-user-select:none/);assert.match(html,/-webkit-touch-callout:none/);assert.match(html,/#pad,#pad \*/);
  const h=harness();for(const name of ['selectstart','contextmenu','dragstart','dblclick','touchstart','touchmove']){let prevented=false;h.elements.get('pad').listeners[name].fn({cancelable:true,preventDefault(){prevented=true}});assert.equal(prevented,true,name)}
  assert.equal(h.elements.get('pad').listeners.touchstart.options.passive,false);
  assert.equal(h.context.document.getElementById('text').listeners.selectstart,undefined);
});
test('double tap drag sends all motion before mouse up',async()=>{
  const h=harness();assert.equal(h.pointer('pointerdown',1,10,10),true);h.pointer('pointerup',1,10,10);h.pointer('pointerdown',2,10,10);h.pointer('pointermove',2,40,30);h.pointer('pointerup',2,40,30);await h.settle();
  assert.deepEqual(h.requests.map(r=>r.kind),['click','drag','move','drag']);assert.equal(h.requests[1].down,true);assert.equal(h.requests[2].x,45);assert.equal(h.requests[2].y,30);assert.equal(h.requests[3].down,false);
});
test('network interruption preserves session and drops queued stale motion',async()=>{
  const h=harness();h.setFail(new Error('network unavailable'));
  h.run("send('move',{x:1,y:0});send('move',{x:99,y:99})");await h.settle();assert.equal(h.run('token'),'session-token');assert.equal(h.run('online'),false);assert.equal(h.requests.length,1);
  h.setFail(null);await h.run("send('heartbeat')");assert.equal(h.run('online'),true);assert.deepEqual(h.requests.map(r=>r.kind),['move','release','heartbeat']);
});
test('explicit server revocation returns to pairing',async()=>{
  const h=harness();const error=new Error('Disconnected');error.status=401;h.setFail(error);await h.run("send('heartbeat')");assert.equal(h.run('token'),null);
});
test('backgrounding releases input without discarding session',async()=>{
  const h=harness();h.context.document.hidden=true;h.documentEvents.visibilitychange();await h.settle();assert.equal(h.run('token'),'session-token');assert.ok(h.requests.some(r=>r.kind==='release'));
});
