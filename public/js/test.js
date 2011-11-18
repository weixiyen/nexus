(function() {
  var socket;
  socket = io.connect('http://localhost:8888', {
    resource: 'socket'
  });
  socket.on('connect', function() {
    return console.log('connected');
  });
  socket.on('game:init', function(state) {
    var column, entity, row, slot, x, y, _i, _len, _ref, _ref2, _ref3, _results;
    for (x = 0, _ref = state.map.length; 0 <= _ref ? x < _ref : x > _ref; 0 <= _ref ? x++ : x--) {
      row = state.map[x];
      for (y = 0, _ref2 = row.length; 0 <= _ref2 ? y < _ref2 : y > _ref2; 0 <= _ref2 ? y++ : y--) {
        column = row[y];
        slot = $('<div />', {
          id: "" + x + "-" + y,
          css: {
            width: 10,
            height: 10,
            display: 'inline-block',
            border: '1px solid black'
          }
        });
        if (column === 1) {
          slot.css('background-color', 'black');
        }
        slot.appendTo('body');
      }
      $('<br />').appendTo('body');
    }
    _ref3 = state.entities;
    _results = [];
    for (_i = 0, _len = _ref3.length; _i < _len; _i++) {
      entity = _ref3[_i];
      _results.push($("#" + entity.x + "-" + entity.y).addClass("entity-" + entity.id).css('background-color', 'green'));
    }
    return _results;
  });
  socket.on('move', function(entity) {
    $(".entity-" + entity.id).removeClass("entity-" + entity.id).css('background-color', 'white');
    return $("#" + entity.x + "-" + entity.y).css('background-color', 'green').addClass("entity-" + entity.id);
  });
  socket.on('dead', function(entity) {
    return $(".entity-" + entity.id).removeClass("entity-" + entity.id).css('background-color', 'white');
  });
  socket.on('log', function(message) {
    return console.log(message);
  });
  socket.on('message', function(message) {
    return console.log(message);
  });
  socket.on('disconnect', function() {
    return console.log('disconnceted');
  });
}).call(this);
