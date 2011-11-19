(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  this.Game = (function() {
    var INTERVAL, PAN_DIST, PAN_SPEED, STUB, UI_HEIGHT;
    STUB = 'ent-';
    INTERVAL = 30;
    PAN_SPEED = 1;
    PAN_DIST = 10;
    UI_HEIGHT = 50;
    function Game(options) {
      this.$canvas = options.$canvas;
      this.loopItems = {};
      this.entities = {};
      this.left = 0;
      this.top = 0;
      this.userId = null;
      this.panning = {
        left: false,
        right: false,
        up: false,
        down: false
      };
      this.beginLoop();
    }
    Game.prototype.reset = function() {
      this.$canvas.empty();
      return this.entities = {};
    };
    Game.prototype.renderOffset = function() {
      var style;
      style = {
        left: this.left,
        top: this.top
      };
      this.$canvas.css(style);
      return map.$canvas.css(style);
    };
    Game.prototype.setUserId = function(entityId) {
      return this.userId = entityId;
    };
    Game.prototype.centerOnUser = function() {
      var me;
      if (!this.entities[STUB + this.userId]) {
        return;
      }
      me = this.entities[STUB + this.userId];
      this.left = -me.left - me.width / 2 + $window.width() / 2;
      this.top = -me.top - me.height / 2 + $window.height() / 2 - UI_HEIGHT;
      return this.renderOffset();
    };
    Game.prototype.addEntities = function(entities) {
      var entity, _i, _len, _results;
      _results = [];
      for (_i = 0, _len = entities.length; _i < _len; _i++) {
        entity = entities[_i];
        _results.push(this.addEntity(entity));
      }
      return _results;
    };
    Game.prototype.addEntity = function(entityData) {
      var entity;
      if (this.entities[STUB + entityData.id]) {
        return;
      }
      entity = null;
      if (entityData.id === this.userId) {
        entity = new User(entityData);
      } else if (window.hasOwnProperty(entityData.kind)) {
        entity = new window[entityData.kind](entityData);
      }
      if (entity === null) {
        return;
      }
      this.entities[STUB + entity.id] = entity;
      return this.addToCanvas(entity.$el);
    };
    Game.prototype.removeEntity = function(entityId) {
      this.entities[STUB + entityId].remove();
      return delete this.entities[STUB + entityId];
    };
    Game.prototype.moveEntity = function(id, x, y) {
      return this.entities[STUB + id].moveTo(x, y);
    };
    Game.prototype.addToCanvas = function($element) {
      return this.$canvas.append($element);
    };
    Game.prototype.beginLoop = function() {
      var count;
      count = 0;
      return setInterval(__bind(function() {
        var loopId, loopItem, _ref;
        if (count === 999999) {
          count = 0;
        }
        _ref = this.loopItems;
        for (loopId in _ref) {
          loopItem = _ref[loopId];
          if (count % loopItem.frequency) {
            continue;
          }
          loopItem.fn(this.loopCount);
        }
        return count += 1;
      }, this), INTERVAL);
    };
    Game.prototype.addLoopItem = function(loopId, frequency, fn) {
      return this.loopItems[loopId] = {
        frequency: frequency,
        fn: fn
      };
    };
    Game.prototype.removeLoopItem = function(loopId) {
      return delete this.loopItems[loopId];
    };
    Game.prototype.panStart = function(dir) {
      if (this.panning[dir]) {
        return;
      }
      this.panning[dir] = true;
      return this.addLoopItem('pan:' + dir, PAN_SPEED, __bind(function() {
        return this.pan(dir);
      }, this));
    };
    Game.prototype.panStop = function(dir) {
      this.panning[dir] = false;
      return this.removeLoopItem('pan:' + dir);
    };
    Game.prototype.panStopAll = function() {
      var dir, value, _ref, _results;
      _ref = this.panning;
      _results = [];
      for (dir in _ref) {
        value = _ref[dir];
        _results.push(this.panning[dir] === true ? this.panStop(dir) : void 0);
      }
      return _results;
    };
    Game.prototype.pan = function(dir) {
      var style;
      style = {
        left: this.left,
        top: this.top
      };
      if (dir === 'left') {
        style.left -= PAN_DIST;
      } else if (dir === 'right') {
        style.left += PAN_DIST;
      } else if (dir === 'up') {
        style.top -= PAN_DIST;
      } else if (dir === 'down') {
        style.top += PAN_DIST;
      }
      this.left = style.left;
      this.top = style.top;
      return this.renderOffset();
    };
    return Game;
  })();
}).call(this);
