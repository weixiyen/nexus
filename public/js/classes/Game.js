(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  this.Game = (function() {
    var INTERVAL, STUB;
    STUB = 'ent-';
    INTERVAL = 30;
    function Game(options) {
      this.$canvas = options.$canvas;
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
        var entity, entityId, _ref;
        _ref = this.entities;
        for (entityId in _ref) {
          entity = _ref[entityId];
          entity.nextIteration(count);
        }
        return count += 1;
      }, this), INTERVAL);
    };
    Game.prototype.registerLoop = function() {};
    return Game;
  })();
}).call(this);
