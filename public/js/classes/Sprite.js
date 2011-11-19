(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  this.Sprite = (function() {
    function Sprite(opts) {
      this.id = 'anim:' + opts.id;
      this.el = opts.el;
      this.queue = opts.queue;
      this.skip = opts.skip || 1;
      this.len = this.queue.length;
      this.counter = 0;
    }
    Sprite.prototype.start = function() {
      return game.addLoopItem(this.id, this.skip, __bind(function() {
        this.el.css({
          'background-position': this.queue[this.counter]
        });
        if (this.counter === this.len) {
          return this.counter = 0;
        }
        return this.counter += 1;
      }, this));
    };
    Sprite.prototype.stop = function() {
      return game.removeLoopItem(this.id);
    };
    return Sprite;
  })();
}).call(this);
