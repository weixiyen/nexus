(function() {
  var events, game, map;
  game = new Game({
    $canvas: $('#game')
  });
  map = new Map({
    $canvas: $('#map')
  });
  events = new GameEvents;
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
}).call(this);
