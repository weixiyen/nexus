(function() {
  this.$document = $(document);
  this.$window = $(window);
  this.game = new Game({
    $canvas: $('#game')
  });
  this.map = new Map({
    $canvas: $('#map')
  });
  this.events = new GameEvents({
    game: game,
    map: map
  });
  events.init(function(data) {
    game.reset();
    map.reset();
    map.setup(data.map);
    game.setUserId(data.me);
    game.addEntities(data.entities);
    return game.centerOnUser();
  });
  events.spawn(function(entity) {
    return game.addEntity(entity);
  });
  events.move(function(id, x, y) {
    return game.moveEntity(id, x, y);
  });
  events.death(function(entityId) {
    return game.removeEntity(entityId);
  });
  events.target(function(aggressorId, targetId) {
    return game.target(aggressorId, targetId);
  });
  $document.on('keydown', function(e) {
    var captured, code;
    captured = false;
    code = e.which;
    if (code === 65) {
      captured = true;
      game.panStart('right');
    }
    if (code === 68) {
      captured = true;
      game.panStart('left');
    }
    if (code === 87) {
      captured = true;
      game.panStart('down');
    }
    if (code === 83) {
      captured = true;
      game.panStart('up');
    }
    if (code === 32) {
      captured = true;
      game.centerOnUser();
    }
    if (captured === true) {
      e.preventDefault();
      return e.stopPropagation();
    }
  });
  $document.on('keyup', function(e) {
    var captured, code;
    captured = false;
    code = e.which;
    if (code === 65) {
      captured = true;
      game.panStop('right');
    }
    if (code === 68) {
      captured = true;
      game.panStop('left');
    }
    if (code === 87) {
      captured = true;
      game.panStop('down');
    }
    if (code === 83) {
      captured = true;
      game.panStop('up');
    }
    if (captured === true) {
      e.preventDefault();
      return e.stopPropagation();
    }
  });
  $window.on('blur', function() {
    return game.panStopAll();
  });
}).call(this);
