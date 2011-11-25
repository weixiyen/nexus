(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  this.Sprite = (function() {
    function Sprite(opts) {
      this.id = 'anim:' + opts.id;
      this.el = opts.el;
      this.index0 = opts.index0 || 1;
      this.counter = this.index0;
    }
    Sprite.prototype.start = function(queue, skip) {
      var len;
      len = queue.length;
      return game.addLoopItem(this.id, skip, __bind(function() {
        this.el.css({
          'background-position': queue[this.counter]
        });
        this.counter += 1;
        if (this.counter === len) {
          return this.counter = this.index0;
        }
      }, this));
    };
    Sprite.prototype.set = function(position) {
      return this.el.css({
        'background-position': position
      });
    };
    Sprite.prototype.stop = function() {
      return game.removeLoopItem(this.id);
    };
    return Sprite;
  })();
}).call(this);
