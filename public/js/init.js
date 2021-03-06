(function() {
  this.$document = $(document);
  this.$window = $(window);
  this.game = new Game;
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
    game.centerOnUser();
    return map.startRenderLoop();
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
  $document.on('contextmenu', function(e) {
    return e.preventDefault();
  });
  map.$canvas.on('click', '.entity', function(e) {
    var entity;
    e.stopPropagation();
    e.preventDefault();
    entity = $(this).data('entity');
    return game.setUserTarget(entity.id);
  });
  map.$canvas.on('dblclick', '.entity', function(e) {
    var entity;
    e.preventDefault();
    e.stopPropagation();
    entity = $(this).data('entity');
    game.setUserTarget(entity.id);
    return events.userAttack(0, entity.id, [map.getMouseCoords()]);
  });
  map.$canvas.on('contextmenu', '.entity', function(e) {
    e.preventDefault();
    e.stopPropagation();
    return $(this).trigger('dblclick');
  });
  $window.on('blur', function() {
    return game.panStopAll();
  });
  $window.on('resize', function(e) {
    interface.reload();
    return map.setClientDimensions();
  });
  $document.disableSelection();
}).call(this);
