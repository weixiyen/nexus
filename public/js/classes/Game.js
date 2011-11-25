(function() {
  var __slice = Array.prototype.slice;

  this.Game = (function() {
    var PAN_DIST, PAN_SPEED, PROP, STUB, UI_HEIGHT;

    STUB = 'ent-';

    PROP = 'prop-';

    PAN_SPEED = 1;

    PAN_DIST = 15;

    UI_HEIGHT = 50;

    function Game(options) {
      this.loopItems = {};
      this.entities = {};
      this.props = {};
      this.left = 0;
      this.top = 0;
      this.userId = null;
      this.targetedEntity = null;
      this.debug = false;
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
      var _this = this;
      this.loopCount = 0;
      gameLoop = function() {
        var loopId, loopItem, _ref;
        requestAnimFrame(gameLoop);
        if (_this.loopCount === 999999) _this.loopCount = 0;
        _ref = _this.loopItems;
        for (loopId in _ref) {
          loopItem = _ref[loopId];
          if (_this.loopCount % loopItem.frequency) continue;
          loopItem.fn(_this.loopCount);
        }
        return _this.loopCount += 1;
      };
      return gameLoop();
    };

    Game.prototype.reset = function() {
      this.entities = {};
      return this.props = {};
    };

    Game.prototype.renderOffset = function() {
      var style;
      style = {
        left: this.left,
        top: this.top
      };
      return map.renderOffset(style);
    };

    Game.prototype.setUserId = function(entityId) {
      return this.userId = entityId;
    };

    Game.prototype.userExists = function() {
      return this.entitiesExist(this.userId);
    };

    Game.prototype.centerOnUser = function() {
      var me;
      if (!this.userExists()) {
        this.centerOnMap();
        this.userDied();
        return;
      }
      me = this.entities[STUB + this.userId];
      this.left = -me.left + me.width / 2 + $window.width() / 2;
      this.top = -me.top + me.height / 2 + $window.height() / 2 - UI_HEIGHT;
      return this.renderOffset();
    };

    Game.prototype.centerOnMap = function() {
      this.left = -Math.round(map.width / 2);
      this.top = -Math.round(map.height / 2);
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
      var entity, isUser;
      isUser = false;
      if (this.entitiesExist(entityData.id)) return;
      entity = null;
      if (entityData.id === this.userId) {
        isUser = true;
        entity = new User(entityData);
      } else if (window.hasOwnProperty(entityData.kind)) {
        entity = new window[entityData.kind](entityData);
      }
      if (entity === null) return;
      if (entity.hasTarget()) entity.aggro(entity.target);
      this.entities[STUB + entity.id] = entity;
      this.addToMap(entity.$el);
      if (isUser) return this.userLoaded();
    };

    Game.prototype.getEntity = function(id) {
      if (!this.entitiesExist(id)) return null;
      return this.entities[STUB + id];
    };

    Game.prototype.getUser = function() {
      return this.getEntity(this.userId);
    };

    Game.prototype.userLoaded = function() {
      this.centerOnUser();
      return interface.reloadUser();
    };

    Game.prototype.addProps = function(props) {
      var prop, _i, _len;
      for (_i = 0, _len = props.length; _i < _len; _i++) {
        prop = props[_i];
        this.addProp(prop);
      }
      return map.associatePropsToTiles();
    };

    Game.prototype.addProp = function(propData) {
      var prop;
      if (this.propsExist(propData.id)) return;
      prop = null;
      if (window.hasOwnProperty(propData.kind)) {
        prop = new window[propData.kind](propData);
      }
      if (prop === null) return;
      return this.props[PROP + propData.id] = prop;
    };

    Game.prototype.removeEntity = function(entityId) {
      this.entities[STUB + entityId].remove();
      delete this.entities[STUB + entityId];
      if (this.isUserId(entityId)) return this.userDied();
    };

    Game.prototype.userDied = function() {
      return interface.showUserDeath();
    };

    Game.prototype.moveEntity = function(id, x, y) {
      if (!this.entitiesExist(id)) return;
      return this.entities[STUB + id].moveTo(x, y);
    };

    Game.prototype.target = function(aggressorId, targetId) {
      var entity;
      if (!this.entitiesExist(aggressorId)) return;
      entity = this.entities[STUB + aggressorId];
      if (targetId === null) {
        entity.deaggro();
        return;
      }
      return entity.aggro(targetId);
    };

    Game.prototype.changeName = function(id, name) {
      if (!this.entitiesExist(id)) return;
      return this.entities[STUB + id].changeName(name);
    };

    Game.prototype.damageTaken = function(id, amt, isCrit) {
      if (!this.entitiesExist(id)) return;
      return this.entities[STUB + id].takeDamage(amt, isCrit);
    };

    Game.prototype.heal = function(id, amt) {
      if (!this.entitiesExist(id)) return;
      return this.entities[STUB + id].heal(amt);
    };

    Game.prototype.changeMp = function(id, mp) {
      if (!this.entitiesExist(id)) return;
      return this.entities[STUB + id].changeMp(mp);
    };

    Game.prototype.setMovementSpeed = function(id, speed) {
      if (!this.entitiesExist(id)) return;
      return this.entities[STUB + id].setMovementSpeed(speed);
    };

    Game.prototype.entitiesExist = function() {
      var id, ids, _i, _len;
      ids = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
      for (_i = 0, _len = ids.length; _i < _len; _i++) {
        id = ids[_i];
        if (!this.entities[STUB + id]) return false;
      }
      return true;
    };

    Game.prototype.propsExist = function() {
      var id, ids, _i, _len;
      ids = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
      for (_i = 0, _len = ids.length; _i < _len; _i++) {
        id = ids[_i];
        if (!this.props[PROP + id]) return false;
      }
      return true;
    };

    Game.prototype.setUserTarget = function(targetId) {
      game.removeCurrentUserTarget();
      if (!this.userExists()) return;
      if (!this.entitiesExist(targetId)) return;
      this.getUser().setTarget(targetId);
      this.targetedEntity = this.getEntity(targetId);
      return this.targetedEntity.userTargeted();
    };

    Game.prototype.removeCurrentUserTarget = function() {
      if (this.targetedEntity) this.targetedEntity.removeUserTarget();
      return this.targetedEntity = null;
    };

    Game.prototype.moveUser = function(x, y) {
      events.moveMe(x, y);
      return this.removeCurrentUserTarget();
    };

    Game.prototype.userAttack = function(attackType) {
      var mouseCoords, targetId;
      if (!this.userExists()) return;
      targetId = this.getUser().getTarget();
      mouseCoords = map.getMouseCoords();
      events.userAttack(attackType, targetId, mouseCoords);
      return interface.releaseAbilityIcon(attackType);
    };

    Game.prototype.addToMap = function($element) {
      return map.$canvas.append($element);
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
      if (!this.entitiesExist(id)) return;
      return this.entities[STUB + id].increaseExperience(amt);
    };

    Game.prototype.levelUp = function(id, data) {
      if (!this.entitiesExist(id)) return;
      return this.entities[STUB + id].levelUp(data);
    };

    Game.prototype.panStart = function(dir) {
      var _this = this;
      if (this.panning[dir]) return;
      this.panning[dir] = true;
      return this.addLoopItem('pan:' + dir, PAN_SPEED, function() {
        return _this.pan(dir);
      });
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
        if (this.panning[dir] === true) {
          _results.push(this.panStop(dir));
        } else {
          _results.push(void 0);
        }
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
