(function() {
  var socket;
  socket = io.connect("" + location.protocol + "//" + location.host, {
    resource: 'socket'
  });
  socket.on('connect', function() {
    return console.log('connected');
  });
  socket.on('initialize', function(state) {
    var column, entity, row, slot, x, y, _i, _len, _ref, _ref2, _ref3, _results;
    $('body').empty();
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
      _results.push($("#" + entity.x + "-" + entity.y).addClass("entity-" + entity.id).css('background-color', 'gray'));
    }
    return _results;
  });
  socket.on('move', function(entity) {
    var color;
    color = entity.target != null ? 'red' : 'gray';
    $(".entity-" + entity.id).removeClass("entity-" + entity.id).css('background-color', 'white');
    return $("#" + entity.x + "-" + entity.y).css('background-color', color).addClass("entity-" + entity.id);
  });
  socket.on('dead', function(entity) {
    return $(".entity-" + entity.id).removeClass("entity-" + entity.id).css('background-color', 'white');
  });
  socket.on('disconnect', function() {
    return console.log('disconnceted');
  });
}).call(this);
