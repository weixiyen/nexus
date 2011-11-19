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
    return code = e.which;
  });
}).call(this);
