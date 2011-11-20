(function() {
  var Entity, Map, entities, socket;
  var __hasProp = Object.prototype.hasOwnProperty, __extends = function(child, parent) {
    for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; }
    function ctor() { this.constructor = child; }
    ctor.prototype = parent.prototype;
    child.prototype = new ctor;
    child.__super__ = parent.prototype;
    return child;
  };
  entities = {};
  Entity = (function() {
    function Entity(data) {
      entities[data.id] = this;
      this.data = data;
      this.zIndex = this.data.id;
    }
    Entity.prototype.render = function() {
      this.$ = $('<div />', {
        id: 'entity' + this.data.id,
        "class": 'entity ' + this.data.kind.toLowerCase(),
        css: {
          left: this.data.x * 12,
          top: this.data.y * 12,
          zIndex: this.zIndex
        }
      });
      return this.$.prependTo('#map');
    };
    Entity.prototype.kill = function() {
      this.$.remove();
      return delete entities[this.data.id];
    };
    Entity.prototype.moveTo = function(x, y) {
      this.data.x = x;
      this.data.y = y;
      return this.$.css({
        left: this.data.x * 12,
        top: this.data.y * 12
      });
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
    }
    return Turret;
  })();
  this.Player = (function() {
    __extends(Player, Entity);
    function Player() {
      Player.__super__.constructor.apply(this, arguments);
      this.zIndex = this.zIndex * 1000;
    }
    return Player;
  })();
  Map = (function() {
    function Map(state) {
      this.state = state;
      $('#map').remove();
    }
    Map.prototype.render = function() {
      var column, map, row, slot, x, y, _ref, _ref2;
      map = $('<div />', {
        id: 'map',
        css: {
          width: 600,
          height: 600
        }
      });
      for (y = 0, _ref = this.state.length; 0 <= _ref ? y < _ref : y > _ref; 0 <= _ref ? y++ : y--) {
        row = this.state[y];
        for (x = 0, _ref2 = row.length; 0 <= _ref2 ? x < _ref2 : x > _ref2; 0 <= _ref2 ? x++ : x--) {
          column = row[x];
          slot = $('<div />', {
            data: {
              x: x,
              y: y
            },
            "class": 'tile'
          });
          if (column === 0) {
            slot.addClass('walkable');
          }
          slot.appendTo(map);
        }
      }
      return $('body').append(map);
    };
    return Map;
  })();
  socket = io.connect("" + location.protocol + "//" + location.host, {
    resource: 'socket',
    query: location.search.slice(1)
  });
  socket.on('connect', function() {
    return console.log('connected');
  });
  socket.on('initialize', function(state) {
    var entity, _i, _len, _ref, _results;
    new Map(state.map).render();
    _ref = state.entities;
    _results = [];
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      entity = _ref[_i];
      entity = new window[entity.kind](entity);
      _results.push(entity.render());
    }
    return _results;
  });
  socket.on('spawn', function(entity) {
    entity = new window[entity.kind](entity);
    return entity.render();
  });
  socket.on('move', function(id, x, y) {
    var entity;
    entity = entities[id];
    return entity.moveTo(x, y);
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
  socket.on('target', function(id, targetId) {
    var entity;
    entity = entities[id];
    if (entity.target != null) {
      entity.$.removeClass('attacking');
    } else if (targetId != null) {
      entity.$.addClass('attacking');
    }
    return entity.target = targetId;
  });
  socket.on('disconnect', function() {
    return console.log('disconnceted');
  });
  $(function() {
    $('body').on('click', '.tile', function(e) {
      var data;
      e.stopPropagation();
      e.preventDefault();
      data = $(this).data();
      return socket.emit('move', [data.x, data.y]);
    });
    return $('#spawn').on('click', function(e) {
      return socket.emit('spawn', []);
    });
  });
}).call(this);
