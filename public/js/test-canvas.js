(function() {
  var Entity, Map, socket;
  var __hasProp = Object.prototype.hasOwnProperty, __extends = function(child, parent) {
    for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; }
    function ctor() { this.constructor = child; }
    ctor.prototype = parent.prototype;
    child.prototype = new ctor;
    child.__super__ = parent.prototype;
    return child;
  };
  window.entities = {};
  Entity = (function() {
    function Entity(data) {
      window.entities[data.id] = this;
      this.data = data;
      this.color = 'gray';
      this.queue = [];
    }
    Entity.prototype.render = function(ctx) {
      var _ref;
      if (this.dead) {
        return;
      }
      if (this.queue.length) {
        _ref = this.queue.shift(), this.data.x = _ref[0], this.data.y = _ref[1];
      }
      ctx.fillStyle = this.data.target != null ? 'red' : this.color;
      return ctx.fillRect(this.data.x * 10, this.data.y * 10, 10, 10);
    };
    Entity.prototype.kill = function() {
      this.dead = true;
      return delete window.entities[this.data.id];
    };
    Entity.prototype.moveTo = function(x, y) {
      return this.queue.push([x, y]);
    };
    return Entity;
  })();
  this.Monster = (function() {
    __extends(Monster, Entity);
    function Monster() {
      Monster.__super__.constructor.apply(this, arguments);
    }
    return Monster;
  })();
  this.Turret = (function() {
    __extends(Turret, Entity);
    function Turret() {
      Turret.__super__.constructor.apply(this, arguments);
      this.color = 'purple';
    }
    return Turret;
  })();
  this.Player = (function() {
    __extends(Player, Entity);
    function Player() {
      Player.__super__.constructor.apply(this, arguments);
      this.color = 'blue';
    }
    return Player;
  })();
  Map = (function() {
    function Map(state) {
      this.state = state;
    }
    Map.prototype.render = function(ctx) {
      var column, row, x, y, _ref, _results;
      _results = [];
      for (y = 0, _ref = this.state.length; 0 <= _ref ? y < _ref : y > _ref; 0 <= _ref ? y++ : y--) {
        row = this.state[y];
        _results.push((function() {
          var _ref2, _results2;
          _results2 = [];
          for (x = 0, _ref2 = row.length; 0 <= _ref2 ? x < _ref2 : x > _ref2; 0 <= _ref2 ? x++ : x--) {
            column = row[x];
            _results2.push(column === 1 ? (ctx.fillStyle = 'black', ctx.fillRect(x * 10, y * 10, 10, 10)) : void 0);
          }
          return _results2;
        })());
      }
      return _results;
    };
    return Map;
  })();
  socket = io.connect("" + location.protocol + "//" + location.host, {
    resource: 'socket'
  });
  socket.on('connect', function() {
    return console.log('connected');
  });
  socket.on('initialize', function(state) {
    var canvas, ctx, entity, map, render, _i, _len, _ref;
    canvas = $('canvas')[0];
    ctx = canvas.getContext('2d');
    window.entities = {};
    map = new Map(state.map);
    _ref = state.entities;
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      entity = _ref[_i];
      new window[entity.kind](entity);
    }
    render = function() {
      var entity, _, _ref2, _results;
      window.webkitRequestAnimationFrame(render);
      ctx.clearRect(0, 0, 600, 600);
      map.render(ctx);
      _ref2 = window.entities;
      _results = [];
      for (_ in _ref2) {
        entity = _ref2[_];
        _results.push(entity.render(ctx));
      }
      return _results;
    };
    return window.webkitRequestAnimationFrame(render);
  });
  socket.on('spawn', function(entity) {
    entity = new window[entity.kind](entity);
    return entity.render($('canvas')[0].getContext('2d'));
  });
  socket.on('move', function(entityId, x, y) {
    var entity;
    entity = entities[entityId];
    return entity.moveTo(x, y);
  });
  socket.on('target', function(id, targetId) {
    var entity;
    entity = entities[id];
    return entity.data.target = targetId;
  });
  socket.on('hp', function(hp) {
    if (hp === 0) {
      return console.log('You are dead....');
    } else {
      return console.log('Your HP is', hp);
    }
  });
  socket.on('death', function(entityId) {
    return entities[entityId].kill();
  });
  socket.on('disconnect', function() {
    return console.log('disconnceted');
  });
  $(function() {
    $('canvas').on('click', function(e) {
      e.stopPropagation();
      e.preventDefault();
      return socket.emit('move', [Math.round(e.offsetX / 10), Math.round(e.offsetY / 10)]);
    });
    return $('#spawn').on('click', function(e) {
      return socket.emit('spawn', []);
    });
  });
}).call(this);
