(function() {
  var $document, events;
  this.game = new Game({
    $canvas: $('#game')
  });
  this.map = new Map({
    $canvas: $('#map')
  });
  events = new GameEvents({
    game: game,
    map: map
  });
  events.init(function(data) {
    game.reset();
    map.reset();
    return game.addEntities(data.entities);
  });
  events.spawn(function(entity) {
    return console.log('mob spawned', entity);
  });
  events.move(function(movementData) {
    return game.moveEntity(movementData);
  });
  events.death(function(entityId) {
    return game.removeEntity(entityId);
  });
  $document = $(document);
  $document.keydown(function(e) {
    var code;
    e.preventDefault();
    e.stopPropagation();
    code = e.which;
    if (code === 65) {
      game.panStart('left');
    }
    if (code === 68) {
      game.panStart('right');
    }
    if (code === 87) {
      game.panStart('up');
    }
    if (code === 83) {
      return game.panStart('down');
    }
  });
  $document.keyup(function(e) {
    var code;
    e.preventDefault();
    e.stopPropagation();
    code = e.which;
    if (code === 65) {
      game.panStop('left');
    }
    if (code === 68) {
      game.panStop('right');
    }
    if (code === 87) {
      game.panStop('up');
    }
    if (code === 83) {
      return game.panStop('down');
    }
  });
  $(window).blur(function() {
    return game.panStopAll();
  });
}).call(this);
