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
    Entity.prototype.moveTo = function(data) {
      this.data = data;
      this.$.css({
        left: data.x * 12,
        top: data.y * 12
      });
      if (this.data.target != null) {
        if (!this.$.hasClass('attacking')) {
          return this.$.addClass('attacking');
        }
      } else if (this.$.hasClass('attacking')) {
        return this.$.removeClass('attacking');
      }
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
  this.Player = (function() {
    __extends(Player, Entity);
    function Player() {
      Player.__super__.constructor.apply(this, arguments);
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
      return $('body').html(map);
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
  socket.on('move', function(data) {
    var entity;
    entity = entities[data.id];
    return entity.moveTo(data);
  });
  socket.on('hp', function(hp) {
    if (hp === 0) {
      return console.log('You are dead....');
    } else {
      return console.log('Your HP is', hp);
    }
  });
  socket.on('dead', function(entity) {});
  socket.on('disconnect', function() {
    return console.log('disconnceted');
  });
  $(function() {
    return $('body').on('click', '.tile', function(e) {
      var data;
      e.stopPropagation();
      e.preventDefault();
      data = $(this).data();
      return socket.emit('move', [data.x, data.y]);
    });
  });
}).call(this);
