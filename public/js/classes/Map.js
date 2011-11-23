(function() {
  var BUFFER, GRID_H, GRID_W, RENDER_INTERVAL, TILE_H, TILE_W;
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  GRID_W = 32;
  GRID_H = 16;
  TILE_W = 302;
  TILE_H = 176;
  BUFFER = 1;
  RENDER_INTERVAL = 8;
  this.Map = (function() {
    function Map(options) {
      this.render = __bind(this.render, this);      this.$canvas = options.$canvas;
      this.mouseOffsetX = 0;
      this.mouseOffsetY = 0;
      this.visibleTiles = {};
      this.cachedFragments = {};
      this.cachedProps = {};
      this.setClientDimensions();
    }
    Map.prototype.startRenderLoop = function() {
      return game.addLoopItem('map:render', RENDER_INTERVAL, this.render);
    };
    Map.prototype.stopRenderLoop = function() {
      return game.removeLoopItem('map:render');
    };
    Map.prototype.reset = function() {
      this.$canvas.empty();
      return this.visibleTiles = {};
    };
    Map.prototype.setup = function(graph) {
      this.graph = graph;
      this.setDimensions(graph[0].length, graph.length);
      this.listenToEvents();
      return this.setUpTiles();
    };
    Map.prototype.renderGraph = function() {
      var blocks, x, xMax, y, yMax;
      blocks = [];
      yMax = this.graph.length;
      xMax = this.graph[0].length;
      for (y = 0; 0 <= yMax ? y < yMax : y > yMax; 0 <= yMax ? y++ : y--) {
        for (x = 0; 0 <= xMax ? x < xMax : x > xMax; 0 <= xMax ? x++ : x--) {
          if (this.graph[y][x] === 2) {
            blocks.push(this.getCollisionBlock(x, y));
          }
        }
      }
      game.$canvas.find('.collision-block').remove().append.apply(game.$canvas, blocks);
      console.log(blocks.length + ' blocks rendered');
      return null;
    };
    Map.prototype.getCollisionBlock = function(x, y) {
      return $('<div/>', {
        "class": 'collision-block',
        css: {
          left: x * GRID_W,
          top: y * GRID_H,
          width: GRID_W,
          height: GRID_H,
          background: 'rgba(0,0,0,0.7)',
          position: 'absolute',
          zIndex: y * GRID_H + 1000
        }
      });
    };
    Map.prototype.setDimensions = function(x, y) {
      this.width = GRID_W * x;
      this.height = GRID_H * y;
      return this.$canvas.css({
        width: this.width,
        height: this.height
      });
    };
    Map.prototype.listenToEvents = function() {
      this.$canvas.on('click', __bind(function(e) {
        game.moveUser(this.getMouseX(), this.getMouseY());
        if (window.DEBUG === true) {
          return console.log(Math.round(this.mouseOffsetX / GRID_W), Math.round(this.mouseOffsetY / GRID_H));
        }
      }, this));
      return this.$canvas.on('mousemove', __bind(function(e) {
        this.mouseOffsetX = e.pageX - this.left;
        return this.mouseOffsetY = e.pageY - this.top;
      }, this));
    };
    Map.prototype.getMouseX = function() {
      return Math.round(this.mouseOffsetX / GRID_W);
    };
    Map.prototype.getMouseY = function() {
      return Math.round(this.mouseOffsetY / GRID_H);
    };
    Map.prototype.getMouseCoords = function() {
      return [this.getMouseX(), this.getMouseY()];
    };
    Map.prototype.renderOffset = function(style) {
      this.left = style.left;
      this.top = style.top;
      return this.$canvas.css(style);
    };
    Map.prototype.setUpTiles = function() {
      var path, txy, x, y, _results;
      this.tiles = [];
      _results = [];
      for (y = 0; y < 20; y++) {
        this.tiles[y] = [];
        _results.push((function() {
          var _results2;
          _results2 = [];
          for (x = 0; x < 20; x++) {
            path = ['/public/img/map/', y, '_', x, '.jpg'].join('');
            this.tiles[y][x] = path;
            txy = 't-' + x + '-' + y;
            _results2.push(this.cachedFragments[txy] = this.getTileFragment(x, y, path));
          }
          return _results2;
        }).call(this));
      }
      return _results;
    };
    Map.prototype.associatePropsToTiles = function() {
      var id, prop, txy, x, y, _ref, _results;
      _ref = game.props;
      _results = [];
      for (id in _ref) {
        prop = _ref[id];
        x = Math.floor(prop.left / TILE_W);
        y = Math.floor(prop.top / TILE_H);
        txy = 't-' + x + '-' + y;
        _results.push(this.cachedProps[txy] ? this.cachedProps[txy].push(prop) : this.cachedProps[txy] = [prop]);
      }
      return _results;
    };
    Map.prototype.setClientDimensions = function() {
      this.clientX = $window.width();
      return this.clientY = $window.height();
    };
    Map.prototype.addToCanvas = function($element) {
      return this.$canvas.append($element);
    };
    Map.prototype.render = function() {
      var $propsToRender, $tilesToRender, id, imgpath, left, leftEnd, pieces, prop, propPurgeIds, props, purgeIds, stub, top, topEnd, txy, x, x1, x2, y, y1, y2, _i, _j, _len, _len2, _ref, _ref2;
      left = Math.abs(this.left);
      top = Math.abs(this.top);
      leftEnd = left + this.clientX;
      topEnd = top + this.clientY;
      x1 = Math.floor(left / TILE_W) - BUFFER;
      y1 = Math.floor(top / TILE_H) - BUFFER;
      x2 = Math.ceil(leftEnd / TILE_W) + BUFFER;
      y2 = Math.ceil(topEnd / TILE_H) + BUFFER;
      purgeIds = [];
      propPurgeIds = [];
      _ref = this.visibleTiles;
      for (id in _ref) {
        stub = _ref[id];
        pieces = stub.split('-');
        x = pieces[1];
        y = pieces[2];
        if ((x > 0 && y > 0) && ((x < x1) || (x > x2) || (y < y1) || (y > y2))) {
          purgeIds.push('#' + stub);
          delete this.visibleTiles[id];
          if (!(props = this.cachedProps[id])) {
            continue;
          }
          for (_i = 0, _len = props.length; _i < _len; _i++) {
            prop = props[_i];
            propPurgeIds.push('#' + prop.elementId);
          }
        }
      }
      $tilesToRender = [];
      $propsToRender = [];
      for (y = y1; y1 <= y2 ? y < y2 : y > y2; y1 <= y2 ? y++ : y--) {
        for (x = x1; x1 <= x2 ? x < x2 : x > x2; x1 <= x2 ? x++ : x--) {
          txy = 't-' + x + '-' + y;
          if (!(imgpath = (_ref2 = this.tiles[y]) != null ? _ref2[x] : void 0)) {
            continue;
          }
          if (this.visibleTiles[txy]) {
            continue;
          }
          this.visibleTiles[txy] = txy;
          $tilesToRender.push(this.cachedFragments[txy]);
          if (!(props = this.cachedProps[txy])) {
            continue;
          }
          for (_j = 0, _len2 = props.length; _j < _len2; _j++) {
            prop = props[_j];
            $propsToRender.push(prop.$el);
          }
        }
      }
      if ($tilesToRender.length > 0) {
        this.$canvas.append.apply(this.$canvas, $tilesToRender);
      }
      if (purgeIds.length > 0) {
        this.$canvas.find(purgeIds.join(',')).remove();
      }
      if ($propsToRender.length > 0) {
        game.$canvas.append.apply(game.$canvas, $propsToRender);
      }
      if (propPurgeIds.length > 0) {
        game.$canvas.find(propPurgeIds.join(',')).remove();
      }
      return null;
    };
    Map.prototype.getTileFragment = function(x, y, imgpath) {
      var html, left, top;
      left = x * TILE_W;
      top = y * TILE_H;
      html = "<div id=\"t-" + x + "-" + y + "\" style=\"background:url(" + imgpath + ") no-repeat;top:" + top + "px;left:" + left + "px;width:" + TILE_W + "px;height:" + TILE_H + "px;position:absolute;\"></div>";
      return $(html);
    };
    return Map;
  })();
}).call(this);
