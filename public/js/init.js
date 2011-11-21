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
  this.interface = new Interface({
    $canvas: $('#interface')
  });
  events.init(function(data) {
    game.reset();
    map.reset();
    map.setup(data.map);
    game.setUserId(data.me);
    game.addEntities(data.entities);
    game.addProps(data.props);
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
  events.nameChange(function(id, name) {
    return game.changeName(id, name);
  });
  events.damageTaken(function(id, amt, isCrit) {
    return game.damageTaken(id, amt, isCrit);
  });
  events.setMovementSpeed(function(id, speed) {
    return game.setMovementSpeed(id, speed);
  });
  events.mpChange(function(id, mp) {
    return game.changeMp(id, mp);
  });
  events.xpChange(function(id, xp) {
    return game.increaseExperience(id, xp);
  });
  events.levelUp(function(id, data) {
    return game.levelUp(id, data);
  });
  events.heal(function(id, amt) {
    return game.heal(id, amt);
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
    if (code >= 49 && code <= 54) {
      captured = true;
      interface.pressAbilityIcon(code - 48);
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
    if (code >= 49 && code <= 54) {
      captured = true;
      game.userAttack(code - 48);
    }
    if (captured === true) {
      e.preventDefault();
      return e.stopPropagation();
    }
  });
  game.$canvas.on('click', '.entity', function(e) {
    var entity;
    entity = $(this).data('entity');
    game.setUserTarget(entity.id);
    return events.userAttack(0, entity.id, [map.getMouseCoords()]);
  });
  $window.on('blur', function() {
    return game.panStopAll();
  });
  $window.on('resize', function(e) {
    interface.reload();
    return map.setClientDimensions();
  });
}).call(this);
