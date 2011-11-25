
  this.Sprite = (function() {

    function Sprite(opts) {
      this.id = 'anim:' + opts.id;
      this.el = opts.el;
      this.index0 = opts.index0 || 1;
      this.counter = this.index0;
    }

    Sprite.prototype.start = function(queue, skip) {
      var len;
      var _this = this;
      len = queue.length;
      return game.addLoopItem(this.id, skip, function() {
        _this.el.css({
          'background-position': queue[_this.counter]
        });
        _this.counter += 1;
        if (_this.counter === len) return _this.counter = _this.index0;
      });
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
