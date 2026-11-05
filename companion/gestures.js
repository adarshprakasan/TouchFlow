/* Pure gesture state machine shared by the phone controller and Node tests. */
(function (scope) {
  class TouchFlowTrackpad {
    constructor(emit, speed = () => 1.5, clock = () => Date.now()) {
      this.emit = emit; this.speed = speed; this.clock = clock;
      this.points = new Map(); this.lastTap = null; this.start = null;
      this.manualDrag = false; this.autoDrag = false; this.multi = false; this.moved = false;
    }
    down(id, x, y) {
      this.points.set(id, { x, y });
      if (this.points.size === 1) {
        this.start = { x, y, time: this.clock() }; this.moved = false; this.multi = false;
        const doubleTap = this.lastTap && this.clock() - this.lastTap.time <= 350 &&
          Math.hypot(x - this.lastTap.x, y - this.lastTap.y) <= 30;
        if (doubleTap && !this.manualDrag) {
          this.autoDrag = true; this.lastTap = null;
          this.emit('drag', { down: true });
        }
      } else {
        this.multi = true; this.lastTap = null;
        if (this.autoDrag || this.manualDrag) {
          this.autoDrag = this.manualDrag = false;
          this.emit('release');
        }
      }
    }
    move(id, x, y) {
      const prior = this.points.get(id); if (!prior) return;
      this.points.set(id, { x, y });
      if (this.start && Math.hypot(x - this.start.x, y - this.start.y) > 5) this.moved = true;
      if (this.points.size > 1) this.emit('scroll', { y: -(y - prior.y) * 5 / this.points.size });
      else if (!this.multi) this.emit('move', { x: (x - prior.x) * this.speed(), y: (y - prior.y) * this.speed() });
    }
    up(id, cancelled = false) {
      if (!this.points.has(id)) return;
      this.points.delete(id);
      if (cancelled) { this.cancel(); return; }
      if (this.points.size) return;
      if (this.autoDrag) {
        this.autoDrag = false; this.emit('drag', { down: false }); this.lastTap = null;
      } else if (!this.multi && !this.moved && this.start && this.clock() - this.start.time < 300 && !this.manualDrag) {
        this.emit('click', { button: 'left' });
        this.lastTap = { x: this.start.x, y: this.start.y, time: this.clock() };
      } else this.lastTap = null;
      this.start = null;
    }
    toggleDrag() {
      this.autoDrag = false; this.lastTap = null; this.manualDrag = !this.manualDrag;
      this.emit('drag', { down: this.manualDrag });
      return this.manualDrag;
    }
    cancel() {
      this.points.clear(); this.start = this.lastTap = null;
      this.autoDrag = this.manualDrag = false; this.emit('release');
    }
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = TouchFlowTrackpad;
  else scope.TouchFlowTrackpad = TouchFlowTrackpad;
})(typeof window !== 'undefined' ? window : globalThis);
