(function() {
  var events;
  this.$document = $(document);
  this.$window = $(window);
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
    game.setUserId(data.me);
    game.addEntities(data.entities);
    return game.centerOnUser();
  });
  events.spawn(function(entity) {
    return game.addEntity(entity);
  });
  events.move(function(movementData) {
    return game.moveEntity(movementData);
  });
  events.death(function(entityId) {
    return game.removeEntity(entityId);
  });
  $document.keydown(function(e) {
    var code;
    e.preventDefault();
    e.stopPropagation();
    code = e.which;
    if (code === 65) {
      game.panStart('right');
    }
    if (code === 68) {
      game.panStart('left');
    }
    if (code === 87) {
      game.panStart('down');
    }
    if (code === 83) {
      game.panStart('up');
    }
    if (code === 32) {
      return game.centerOnUser();
    }
  });
  $document.keyup(function(e) {
    var code;
    e.preventDefault();
    e.stopPropagation();
    code = e.which;
    if (code === 65) {
      game.panStop('right');
    }
    if (code === 68) {
      game.panStop('left');
    }
    if (code === 87) {
      game.panStop('down');
    }
    if (code === 83) {
      return game.panStop('up');
    }
  });
  $window.blur(function() {
    return game.panStopAll();
  });
}).call(this);
