(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  this.Sprite = (function() {
    function Sprite(opts) {
      this.id = 'anim:' + opts.id;
      this.el = opts.el;
      this.skip = opts.skip || 1;
      this.counter = 0;
    }
    Sprite.prototype.start = function(queue) {
      var len;
      len = queue.length;
      return game.addLoopItem(this.id, this.skip, __bind(function() {
        this.el.css({
          'background-position': queue[this.counter]
        });
        this.counter += 1;
        if (this.counter === len) {
          return this.counter = 0;
        }
      }, this));
    };
    Sprite.prototype.stop = function() {
      return game.removeLoopItem(this.id);
    };
    return Sprite;
  })();
}).call(this);
