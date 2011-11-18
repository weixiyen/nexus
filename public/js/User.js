(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  this.User = (function() {
    function User(data) {
      this.name = data.name;
      this.map = data.map;
      this.el = $('<div id="user" class="user"><div class="name">' + this.name + '</div></div>').appendTo(this.map.$map);
      this.elName = this.el.find('.name:first');
      this.height = data.height;
      this.width = data.width;
      this.imgpath = data.imgpath;
      this.id = data.id;
      this.anim = data.anim;
      this.spriteQueue = [];
      this.stub = 'user-';
      this.moving = {
        n: false,
        e: false,
        s: false,
        w: false
      };
      this.el.css({
        height: this.height,
        width: this.width,
        background: 'no-repeat url(' + this.imgpath + ')',
        position: 'fixed',
        zIndex: this.map.pos[1]
      });
      this.elName.css({
        left: this.width / 2 - 50,
        top: -10
      });
      this.tag = {
        automove: 'user:path:automove',
        pathloop: 'user:path:loop'
      };
      this.center();
      this.bindWindowResize();
      this.face(data.facing);
    }
    User.prototype.bindWindowResize = function() {
      return $(window).resize(__bind(function() {
        return this.center();
      }, this));
    };
    User.prototype.center = function() {
      var left, top;
      left = $(window).width() / 2 - this.width / 2 + this.map.xOffset + 8;
      top = $(window).height() / 2 - this.height + this.map.yOffset + 8;
      return this.put(left, top);
    };
    User.prototype.put = function(x, y) {
      return this.el.css({
        left: x,
        top: y
      });
    };
    User.prototype.runTo = function(coords) {
      var LOOPID, NODE1, NODE2, path, run, x1, x2, xDivisor, y1, y2, yDivisor;
      LOOPID = this.tag.pathloop;
      NODE1 = 'user:path:node:1';
      NODE2 = 'user:path:node:2';
      $.loop.remove(LOOPID);
      this.stopAll();
      xDivisor = this.map.nodeWidth;
      yDivisor = this.map.nodeHeight;
      x1 = Math.floor(this.map.pos[0] / xDivisor);
      y1 = Math.floor(this.map.pos[1] / yDivisor);
      x2 = Math.floor(coords[0] / xDivisor);
      y2 = Math.floor(coords[1] / yDivisor);
      path = this.map.getPath([x1, y1], [x2, y2]);
      if (path.length < 2) {
        return;
      }
      run = __bind(function() {
        if (path.length < 2) {
          $.loop.remove(LOOPID);
          user.stopAll();
          return;
        }
        global[NODE1] = path.shift();
        global[NODE2] = path[0];
        return this.move(this.map.getDirection(global[NODE1], global[NODE2]));
      }, this);
      global[this.tag.automove] = true;
      run();
      return $.loop.add(LOOPID, function() {
        if (this.map.completedPath(global[NODE1], global[NODE2])) {
          user.stopAll();
          return run();
        }
      });
    };
    User.prototype.keyMove = function(direction) {
      $.loop.remove(this.tag.pathloop);
      if (global[this.tag.automove] === true) {
        user.stopAll();
      }
      global[this.tag.automove] = false;
      return this.move(direction);
    };
    User.prototype.move = function(direction) {
      var xBound, yBound;
      if (this.moving[direction] === true) {
        return;
      } else {
        this.moving[direction] = true;
      }
      xBound = Math.floor(this.width / 2);
      yBound = Math.floor(this.height / 2);
      this.map.panStart(direction, xBound, yBound);
      this.stopAllSprites(direction);
      return this.spriteStart(this.map.getSimpleDirection(direction));
    };
    User.prototype.movingDiagonally = function() {
      var i, k, v, _ref;
      i = 0;
      _ref = this.moving;
      for (k in _ref) {
        v = _ref[k];
        if (v === true) {
          i += 1;
        }
      }
      return i >= 2;
    };
    User.prototype.stop = function(direction) {
      this.moving[direction] = false;
      this.map.panStop(direction);
      return this.spriteStop(direction);
    };
    User.prototype.spriteStart = function(direction) {
      var loopid;
      loopid = this.stub + direction;
      sprite.start(loopid, {
        el: this.el,
        queue: this.anim[direction],
        skip: 3
      });
      return this.spriteQueueAdd(direction);
    };
    User.prototype.spriteStop = function(direction) {
      sprite.stop(this.stub + direction);
      this.spriteQueueRemove(direction);
      if (this.spriteQueue.length) {
        this.spriteStart(this.spriteQueue[0]);
      }
      if (global[this.tag.automove] === false) {
        return this.face(direction);
      }
    };
    User.prototype.spriteQueueAdd = function(direction) {
      if (!this.spriteQueueHas(direction)) {
        return this.spriteQueue.push(direction);
      }
    };
    User.prototype.spriteQueueRemove = function(direction) {
      var index;
      index = this.getSpriteQueueIndex(direction);
      return this.spriteQueue.splice(index, 1);
    };
    User.prototype.getSpriteQueueIndex = function(direction) {
      return $.inArray(direction, this.spriteQueue);
    };
    User.prototype.spriteQueueHas = function(direction) {
      return -1 !== this.getSpriteQueueIndex(direction);
    };
    User.prototype.stopAllSprites = function(direction) {
      var k, v, _ref, _results;
      _ref = this.moving;
      _results = [];
      for (k in _ref) {
        v = _ref[k];
        _results.push(this.moving[k] === true ? sprite.stop(this.stub + k) : void 0);
      }
      return _results;
    };
    User.prototype.stopAll = function() {
      var k, v, _ref, _results;
      _ref = this.moving;
      _results = [];
      for (k in _ref) {
        v = _ref[k];
        _results.push(this.moving[k] === true ? this.stop(k) : void 0);
      }
      return _results;
    };
    User.prototype.teleport = function(xcoord, ycoord) {
      return this.map.goTo(xcoord, ycoord);
    };
    User.prototype.face = function(direction) {
      direction = this.map.getSimpleDirection(direction);
      return this.el.css({
        'background-position': this.anim[direction][1]
      });
    };
    return User;
  })();
}).call(this);
