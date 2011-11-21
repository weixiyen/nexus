(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; }, __slice = Array.prototype.slice;
  this.GameEvents = (function() {
    function GameEvents(options) {
      var $document;
      $document = $(document);
      this.socket = io.connect("" + location.protocol + "//" + location.host, {
        resource: 'socket',
        query: location.search.slice(1)
      });
      this.events = {};
      this.socket.on('instructions', __bind(function(instructions) {
        var data, event, instruction, _i, _len, _results;
        instructions = JSON.parse(instructions);
        _results = [];
        for (_i = 0, _len = instructions.length; _i < _len; _i++) {
          instruction = instructions[_i];
          event = instruction[0], data = instruction[1];
          _results.push((function() {
            try {
              return this.events[event].apply(this, data);
            } catch (e) {
              return console.log(event, data);
            }
          }).call(this));
        }
        return _results;
      }, this));
    }
    GameEvents.prototype.connect = function(fn) {
      return this.events['connect'] = function() {
        return fn();
      };
    };
    GameEvents.prototype.init = function(fn) {
      return this.socket.on('initialize', function(data) {
        return fn(data);
      });
    };
    GameEvents.prototype.spawn = function(fn) {
      return this.events['spawn'] = function(data) {
        return fn(data);
      };
    };
    GameEvents.prototype.move = function(fn) {
      return this.events['move'] = function() {
        var data;
        data = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
        return fn(data[0], data[1], data[2]);
      };
    };
    GameEvents.prototype.death = function(fn) {
      return this.events['death'] = function(data) {
        return fn(data);
      };
    };
    GameEvents.prototype.target = function(fn) {
      return this.events['target'] = function(aggressorId, targetId) {
        return fn(aggressorId, targetId);
      };
    };
    GameEvents.prototype.mpChange = function(fn) {
      return this.events['mp'] = function(id, mp) {
        return fn(id, mp);
      };
    };
    GameEvents.prototype.nameChange = function(fn) {
      return this.events['name-change'] = function(id, name) {
        return fn(id, name);
      };
    };
    GameEvents.prototype.damageTaken = function(fn) {
      return this.events['damage-taken'] = function(id, amt, isCritical) {
        return fn(id, amt, isCritical);
      };
    };
    GameEvents.prototype.setMovementSpeed = function(fn) {
      return this.events['set-movement-speed'] = function(id, speed) {
        return fn(id, speed);
      };
    };
    GameEvents.prototype.moveMe = function(x, y) {
      return this.socket.emit('move', [x, y]);
    };
    GameEvents.prototype.userAttack = function(attackType, targetId, mousePosition) {
      return this.socket.emit('attack', attackType, targetId, mousePosition);
    };
    return GameEvents;
  })();
}).call(this);
