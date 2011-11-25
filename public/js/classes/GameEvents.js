
  this.GameEvents = (function() {

    function GameEvents(options) {
      var $document;
      var _this = this;
      $document = $(document);
      this.socket = io.connect("" + location.protocol + "//" + location.host, {
        resource: 'socket',
        query: location.search.slice(1)
      });
      this.events = {};
      this.socket.on('instructions', function(data) {
        var event, instruction, instructions, timestamp, _i, _len, _ref, _results;
        _ref = JSON.parse(data), timestamp = _ref.timestamp, instructions = _ref.instructions;
        _results = [];
        for (_i = 0, _len = instructions.length; _i < _len; _i++) {
          instruction = instructions[_i];
          event = instruction[0], data = instruction[1];
          try {
            _results.push(_this.events[event].apply(_this, data));
          } catch (e) {

          }
        }
        return _results;
      });
    }

    GameEvents.prototype.connect = function(fn) {
      return this.events['connect'] = fn;
    };

    GameEvents.prototype.init = function(fn) {
      return this.socket.on('initialize', fn);
    };

    GameEvents.prototype.spawn = function(fn) {
      return this.events['spawn'] = fn;
    };

    GameEvents.prototype.move = function(fn) {
      return this.events['move'] = fn;
    };

    GameEvents.prototype.death = function(fn) {
      return this.events['death'] = fn;
    };

    GameEvents.prototype.target = function(fn) {
      return this.events['target'] = fn;
    };

    GameEvents.prototype.mpChange = function(fn) {
      return this.events['mp'] = fn;
    };

    GameEvents.prototype.xpChange = function(fn) {
      return this.events['experience'] = fn;
    };

    GameEvents.prototype.levelUp = function(fn) {
      return this.events['level-up'] = fn;
    };

    GameEvents.prototype.nameChange = function(fn) {
      return this.events['name-change'] = fn;
    };

    GameEvents.prototype.damageTaken = function(fn) {
      return this.events['damage-taken'] = fn;
    };

    GameEvents.prototype.setMovementSpeed = function(fn) {
      return this.events['set-movement-speed'] = fn;
    };

    GameEvents.prototype.heal = function(fn) {
      return this.events['heal'] = fn;
    };

    GameEvents.prototype.moveMe = function(x, y) {
      return this.socket.emit('move', [x, y]);
    };

    GameEvents.prototype.userAttack = function(attackType, targetId, mousePosition) {
      return this.socket.emit('attack', attackType, targetId, mousePosition);
    };

    return GameEvents;

  })();
