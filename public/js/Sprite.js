(function() {
  this.Sprite = (function() {
    function Sprite() {}
    Sprite.prototype.start = function(id, opts, callback) {
      var el, len, queue, skip;
      id = 'mm-anim-' + id;
      el = opts.el;
      queue = opts.queue;
      len = queue.length;
      skip = opts.skip || 1;
      global[id] = 0;
      $.loop.add(id, skip, function() {
        el.css({
          'background-position': queue[global[id]]
        });
        if (global[id] === len) {
          return global[id] = 0;
        }
        return global[id] += 1;
      });
      if (callback != null) {
        return this.callback(opts);
      }
    };
    Sprite.prototype.stop = function(id) {
      return $.loop.remove('mm-anim-' + id);
    };
    Sprite.prototype.once = function(options, callback) {};
    return Sprite;
  })();
}).call(this);
