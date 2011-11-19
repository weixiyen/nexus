(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  this.Game = (function() {
    var INTERVAL, STUB;
    STUB = 'ent-';
    INTERVAL = 30;
    function Game(options) {
      this.$canvas = options.$canvas;
      this.loopItems = {};
      this.entities = {};
      this.beginLoop();
    }
    Game.prototype.reset = function() {
      this.$canvas.empty();
      return this.entities = {};
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
      entity = null;
      if (window.hasOwnProperty(entityData.kind)) {
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
    Game.prototype.moveEntity = function(moveData) {
      var id, x, y;
      id = moveData.id;
      x = moveData.x;
      y = moveData.y;
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
    Game.prototype.registerLoopItem = function(loopId, frequency, fn) {
      return this.loopItems[loopId] = {
        frequency: frequency,
        fn: fn
      };
    };
    Game.prototype.removeLoopItem = function(loopId) {
      return delete loopItems[loopId];
    };
    return Game;
  })();
}).call(this);
