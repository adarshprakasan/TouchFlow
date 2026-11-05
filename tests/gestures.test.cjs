const {test}=require('node:test');
const assert=require('node:assert/strict');
const Trackpad=require('../companion/gestures.js');
function setup(){let now=1000;const events=[];return {events,advance:ms=>now+=ms,pad:new Trackpad((kind,payload)=>events.push({kind,...payload}),()=>1,()=>now)}}
test('single tap emits one left click',()=>{const {pad,events,advance}=setup();pad.down(1,10,10);advance(50);pad.up(1);assert.deepEqual(events,[{kind:'click',button:'left'}])});
test('second tap holds mouse before movement and releases on lift',()=>{const {pad,events,advance}=setup();pad.down(1,10,10);advance(50);pad.up(1);advance(100);pad.down(2,12,10);pad.move(2,42,25);pad.up(2);assert.deepEqual(events,[{kind:'click',button:'left'},{kind:'drag',down:true},{kind:'move',x:30,y:15},{kind:'drag',down:false}]);assert.equal(pad.autoDrag,false)});
test('ordinary movement does not emit a click',()=>{const {pad,events}=setup();pad.down(1,10,10);pad.move(1,50,30);pad.up(1);assert.deepEqual(events,[{kind:'move',x:40,y:20}])});
test('second tap outside timing or distance does not start drag',()=>{for(const [delay,x] of [[500,10],[100,100]]){const {pad,events,advance}=setup();pad.down(1,10,10);advance(40);pad.up(1);advance(delay);pad.down(2,x,10);pad.up(2);assert.equal(events.filter(x=>x.kind==='drag').length,0)}});
test('two finger scroll does not click or jump when one finger lifts',()=>{const {pad,events}=setup();pad.down(1,10,10);pad.down(2,40,10);pad.move(1,10,30);pad.up(1);pad.move(2,70,10);pad.up(2);assert.deepEqual(events,[{kind:'scroll',y:-50}])});
test('pointer cancellation releases automatic dragging',()=>{const {pad,events,advance}=setup();pad.down(1,10,10);pad.up(1);advance(100);pad.down(2,10,10);pad.up(2,true);assert.equal(events.at(-1).kind,'release');assert.equal(pad.autoDrag,false);assert.equal(pad.points.size,0)});
test('manual drag persists across strokes until toggled off',()=>{const {pad,events}=setup();pad.toggleDrag();pad.down(1,10,10);pad.move(1,20,10);pad.up(1);assert.equal(pad.manualDrag,true);pad.toggleDrag();assert.deepEqual(events,[{kind:'drag',down:true},{kind:'move',x:10,y:0},{kind:'drag',down:false}])});
test('second finger releases drag before scrolling',()=>{const {pad,events}=setup();pad.toggleDrag();pad.down(1,10,10);pad.down(2,20,10);assert.equal(events.at(-1).kind,'release');assert.equal(pad.manualDrag,false)});
