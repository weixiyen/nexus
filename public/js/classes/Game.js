(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; }, __slice = Array.prototype.slice;
  this.Game = (function() {
    var PAN_DIST, PAN_SPEED, STUB, UI_HEIGHT;
    STUB = 'ent-';
    PAN_SPEED = 1;
    PAN_DIST = 15;
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
    Game.prototype.isUserId = function(id) {
      return id === this.userId;
    };
    Game.prototype.beginLoop = function() {
      var gameLoop;
      this.loopCount = 0;
      gameLoop = __bind(function() {
        var loopId, loopItem, _ref;
        requestAnimFrame(gameLoop);
        if (this.loopCount === 999999) {
          this.loopCount = 0;
        }
        _ref = this.loopItems;
        for (loopId in _ref) {
          loopItem = _ref[loopId];
          if (this.loopCount % loopItem.frequency) {
            continue;
          }
          loopItem.fn(this.loopCount);
        }
        return this.loopCount += 1;
      }, this);
      return gameLoop();
    };
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
      return map.renderOffset(style);
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
      this.renderOffset();
      return map.render();
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
      var entity, isUser;
      isUser = false;
      if (this.entities[STUB + entityData.id]) {
        return;
      }
      entity = null;
      if (entityData.id === this.userId) {
        isUser = true;
        entity = new User(entityData);
      } else if (window.hasOwnProperty(entityData.kind)) {
        entity = new window[entityData.kind](entityData);
      }
      if (entity === null) {
        return;
      }
      if (entity.hasTarget()) {
        entity.aggro(entity.target);
      }
      this.entities[STUB + entity.id] = entity;
      this.addToCanvas(entity.$el);
      if (isUser) {
        return this.centerOnUser();
      }
    };
    Game.prototype.removeEntity = function(entityId) {
      this.entities[STUB + entityId].remove();
      return delete this.entities[STUB + entityId];
    };
    Game.prototype.moveEntity = function(id, x, y) {
      if (!this.entitiesExist(id)) {
        return;
      }
      return this.entities[STUB + id].moveTo(x, y);
    };
    Game.prototype.target = function(aggressorId, targetId) {
      var entity;
      if (!this.entitiesExist(aggressorId)) {
        return;
      }
      entity = this.entities[STUB + aggressorId];
      if (targetId === null) {
        entity.deaggro();
        return;
      }
      return entity.aggro(targetId);
    };
    Game.prototype.changeName = function(id, name) {
      if (!this.entitiesExist(id)) {
        return;
      }
      return this.entities[STUB + id].changeName(name);
    };
    Game.prototype.damageTaken = function(id, amt, isCrit) {
      if (!this.entitiesExist(id)) {
        return;
      }
      return this.entities[STUB + id].takeDamage(amt, isCrit);
    };
    Game.prototype.changeMp = function(id, mp) {
      if (!this.entitiesExist(id)) {
        return;
      }
      return this.entities[STUB + id].changeMp(mp);
    };
    Game.prototype.setMovementSpeed = function(id, speed) {
      if (!this.entitiesExist(id)) {
        return;
      }
      return this.entities[STUB + id].setMovementSpeed(speed);
    };
    Game.prototype.entitiesExist = function() {
      var id, ids, _i, _len;
      ids = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
      for (_i = 0, _len = ids.length; _i < _len; _i++) {
        id = ids[_i];
        if (!this.entities[STUB + id]) {
          return false;
        }
      }
      return true;
    };
    Game.prototype.userAttack = function(attackType) {
      var mouseCoords, targetId;
      if (!this.entitiesExist(this.userId)) {
        return;
      }
      targetId = this.entities[STUB + this.userId].getTarget();
      mouseCoords = map.getMouseCoords();
      return events.userAttack(attackType, targetId, mouseCoords);
    };
    Game.prototype.setUserTarget = function(targetId) {
      if (!this.entitiesExist(this.userId)) {
        return;
      }
      return this.entities[STUB + this.userId].setTarget(targetId);
    };
    Game.prototype.addToCanvas = function($element) {
      return this.$canvas.append($element);
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
    Game.prototype.increaseExperience = function(id, amt) {
      if (!this.entitiesExist(id)) {
        return;
      }
      return this.entities[STUB + id].increaseExperience(amt);
    };
    Game.prototype.levelUp = function(id, data) {
      if (!this.entitiesExist(id)) {
        return;
      }
      return this.entities[STUB + id].levelUp(data);
    };
    Game.prototype.panStart = function(dir) {
      if (this.panning[dir]) {
        return;
      }
      this.panning[dir] = true;
      this.addLoopItem('pan:' + dir, PAN_SPEED, __bind(function() {
        return this.pan(dir);
      }, this));
      return map.startRenderLoop();
    };
    Game.prototype.panStop = function(dir) {
      this.panning[dir] = false;
      this.removeLoopItem('pan:' + dir);
      return map.stopRenderLoop();
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
