(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; }, __slice = Array.prototype.slice;
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
      var entity, isUser, _ref, _ref2, _ref3, _ref4;
      if (entityData.components.death != null) {
        return;
      }
      if (entityData.archetype === 'Character') {
        entityData.kind = 'PlayerEntity';
      }
      if (entityData.archetype === 'Minion') {
        entityData.kind = 'Minion';
      }
      if ((_ref = entityData.archetype) === 'Turret' || _ref === 'TurretPink') {
        entityData.kind = 'Tower';
      }
      if ((_ref2 = entityData.archetype) === 'Nexus' || _ref2 === 'NexusPink') {
        entityData.kind = 'Nexus';
      }
      if ((_ref3 = entityData.archetype) === 'Projectile' || _ref3 === 'ProjectilePink') {
        entityData.kind = 'TowerAttack';
      }
      if ((_ref4 = entityData.archetype) === 'Tree' || _ref4 === 'Rock') {
        entityData.kind = 'Prop';
      }
      isUser = false;
      if (this.entitiesExist(entityData.id)) {
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
      if (entity.kind !== 'Prop' && entity.hasTarget()) {
        entity.aggro(entity.target);
      }
      this.entities[STUB + entity.id] = entity;
      this.addToMap(entity.$el);
      if (isUser) {
        return this.userLoaded();
      }
    };
    Game.prototype.getEntity = function(id) {
      if (!this.entitiesExist(id)) {
        return null;
      }
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
      if (this.propsExist(propData.id)) {
        return;
      }
      prop = null;
      if (window.hasOwnProperty(propData.kind)) {
        prop = new window[propData.kind](propData);
      }
      if (prop === null) {
        return;
      }
      return this.props[PROP + propData.id] = prop;
    };
    Game.prototype.removeEntity = function(entityId) {
      this.entities[STUB + entityId].remove();
      delete this.entities[STUB + entityId];
      if (this.isUserId(entityId)) {
        return this.userDied();
      }
    };
    Game.prototype.userDied = function() {
      return interface.showUserDeath();
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
    Game.prototype.heal = function(id, amt) {
      if (!this.entitiesExist(id)) {
        return;
      }
      return this.entities[STUB + id].heal(amt);
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
    Game.prototype.propsExist = function() {
      var id, ids, _i, _len;
      ids = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
      for (_i = 0, _len = ids.length; _i < _len; _i++) {
        id = ids[_i];
        if (!this.props[PROP + id]) {
          return false;
        }
      }
      return true;
    };
    Game.prototype.setUserTarget = function(targetId) {
      game.removeCurrentUserTarget();
      if (!this.userExists()) {
        return;
      }
      if (!this.entitiesExist(targetId)) {
        return;
      }
      this.getUser().setTarget(targetId);
      this.targetedEntity = this.getEntity(targetId);
      return this.targetedEntity.userTargeted();
    };
    Game.prototype.removeCurrentUserTarget = function() {
      if (this.targetedEntity) {
        this.targetedEntity.removeUserTarget();
      }
      return this.targetedEntity = null;
    };
    Game.prototype.moveUser = function(x, y) {
      events.moveMe(x, y);
      return this.removeCurrentUserTarget();
    };
    Game.prototype.userAttack = function(attackType) {
      var mouseCoords, targetId;
      if (!this.userExists()) {
        return;
      }
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
