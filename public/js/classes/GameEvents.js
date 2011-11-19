(function() {
  var __slice = Array.prototype.slice;
  this.GameEvents = (function() {
    function GameEvents(options) {
      var $document;
      $document = $(document);
      this.socket = io.connect("" + location.protocol + "//" + location.host, {
        resource: 'socket'
      });
    }
    GameEvents.prototype.connect = function(fn) {
      return this.socket.on('connect', function() {
        return fn();
      });
    };
    GameEvents.prototype.init = function(fn) {
      return this.socket.on('initialize', function(data) {
        return fn(data);
      });
    };
    GameEvents.prototype.spawn = function(fn) {
      return this.socket.on('spawn', function(data) {
        return fn(data);
      });
    };
    GameEvents.prototype.move = function(fn) {
      return this.socket.on('move', function() {
        var data;
        data = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
        return fn(data[0], data[1], data[2]);
      });
    };
    GameEvents.prototype.death = function(fn) {
      return this.socket.on('death', function(data) {
        return fn(data);
      });
    };
    return GameEvents;
  })();
}).call(this);
