(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  this.Map = (function() {
    function Map(options) {
      this.change = options.change;
      this.$map = options.$map;
      this.$tileMap = options.$tileMap;
      this.tileWidth = options.tileWidth;
      this.tileHeight = options.tileHeight;
      this.halfTileWidth = Math.floor(options.tileWidth / 2);
      this.halfTileHeight = Math.floor(options.tileHeight / 2);
      this.nodeWidth = this.halfTileWidth;
      this.nodeHeight = this.halfTileHeight;
      this.tileMap = options.tileMap;
      this.viewableTiles = {};
      this.collisionTypes = options.collisionTypes;
      this.dir = {
        N: 'n',
        E: 'e',
        S: 's',
        W: 'w'
      };
      this.NPC = options.NPC;
      this.Player = options.Player;
      this.npcs = {};
      this.players = {};
      this.unitStub = 'unit-';
      this.pos = [options.xcoord, options.ycoord];
      this.xOffset = 0;
      this.yOffset = -1 * Math.ceil(settings.partyBox.height / 2.5);
      this.tileEagerloadDepth = 6;
      this.isPointInPoly = $.polygon.isPointWithin;
      this.recenter();
      this.bindWindowResize();
      this.startUIGenerator();
      this.generateCollisionGraph(this.tileMap);
    }
    Map.prototype.accessible = function(xcoord, ycoord) {
      var bad, badPolygons, badTiles, c, coord, e, n, polygon, s, tileType, w, _i, _j, _k, _len, _len2, _len3, _ref;
      c = [xcoord, ycoord];
      n = [xcoord, ycoord - this.nodeHeight];
      e = [xcoord + this.nodeWidth, ycoord];
      w = [xcoord - this.nodeWidth, ycoord];
      s = [xcoord, ycoord + this.nodeHeight];
      badTiles = [];
      _ref = [c, n, e, w, s];
      for (_i = 0, _len = _ref.length; _i < _len; _i++) {
        coord = _ref[_i];
        tileType = this.getTileType(coord[0], coord[1]);
        if (-1 !== this.collisionTypes.indexOf(tileType)) {
          badTiles.push(coord);
        }
      }
      badPolygons = [];
      for (_j = 0, _len2 = badTiles.length; _j < _len2; _j++) {
        coord = badTiles[_j];
        badPolygons.push(this.getPolygon(coord));
      }
      for (_k = 0, _len3 = badPolygons.length; _k < _len3; _k++) {
        polygon = badPolygons[_k];
        bad = this.isPointInPoly(polygon, {
          x: xcoord,
          y: ycoord
        });
        if (bad === true) {
          return false;
        }
        break;
      }
      return true;
    };
    Map.prototype.bindWindowResize = function() {
      return $(window).resize(__bind(function() {
        return this.recenter();
      }, this));
    };
    Map.prototype.getPolygon = function(coord) {
      var e, n, nh, nw, s, w, x, y;
      nw = this.nodeWidth;
      nh = this.nodeHeight;
      x = Math.floor(coord[0] / nw) * nw + (nw / 2);
      y = Math.floor(coord[1] / nh) * nh + (nh / 2);
      n = {
        x: x,
        y: y - nh
      };
      e = {
        x: x + nw,
        y: y
      };
      s = {
        x: x,
        y: y + nh
      };
      w = {
        x: x - nw,
        y: y
      };
      return [n, e, s, w];
    };
    Map.prototype.addNpc = function(data) {
      var tag;
      tag = this.unitStub + data.id;
      data.el = $('<div id="' + tag + '" class="unit"></div>');
      this.npcs[data.id] = new this.NPC(data);
      return this.$map.append(this.npcs[data.id].el);
    };
    Map.prototype.addPlayer = function(data) {
      var tag;
      tag = this.unitStub + data.id;
      data.el = $('<div id="' + tag + '" class="unit"></div>');
      this.npcs[data.id] = new this.NPC(data);
      return this.$map.append(this.npcs[data.id].el);
    };
    Map.prototype.addUnits = function(arrData) {
      var addHtml, data, _i, _len, _results;
      addHtml = [];
      if (false === arrData instanceof Array) {
        arrData = [arrData];
      }
      _results = [];
      for (_i = 0, _len = arrData.length; _i < _len; _i++) {
        data = arrData[_i];
        _results.push(!(this.npcs[data.id] != null) && !this.players[data.id] ? (data.type === 'npc' ? this.addNpc(data) : void 0, data.type === 'player' ? this.addPlayer(data) : void 0) : void 0);
      }
      return _results;
    };
    Map.prototype.canShift = function(direction, xBound, yBound) {
      var newXcoord, newYcoord;
      newXcoord = this.pos[0];
      newYcoord = this.pos[1];
      xBound = this.change;
      yBound = this.change;
      if (direction === this.dir.W) {
        newXcoord -= xBound;
      } else if (direction === this.dir.E) {
        newXcoord += xBound;
      } else if (direction === this.dir.N) {
        newYcoord -= yBound;
      } else if (direction === this.dir.S) {
        newYcoord += yBound;
      }
      return this.accessible(newXcoord, newYcoord);
    };
    Map.prototype.completedPath = function(node1, node2, coords) {
      var direction;
      if (!(coords != null)) {
        coords = [this.pos[0], this.pos[1]];
      }
      direction = this.getSimpleDirection(this.getDirection(node1, node2));
      if (direction === this.dir.W && coords[0] <= node2[0]) {
        return true;
      } else if (direction === this.dir.E && coords[0] >= node2[0]) {
        return true;
      } else if (direction === this.dir.N && coords[1] <= node2[1]) {
        return true;
      } else if (direction === this.dir.S && coords[1] >= node2[1]) {
        return true;
      }
      return false;
    };
    Map.prototype.generateCollisionGraph = function(tiles) {
      var collisionMap, createRow, createTile, getAccessible, len, row, x, y, _i, _len;
      collisionMap = [];
      x = y = 0;
      len = tiles[0].length;
      getAccessible = __bind(function(type) {
        if (-1 === this.collisionTypes.indexOf(type)) {
          return 0;
        } else {
          return 1;
        }
      }, this);
      createRow = function(row) {
        var tile, _i, _len;
        collisionMap.push([]);
        for (_i = 0, _len = row.length; _i < _len; _i++) {
          tile = row[_i];
          createTile(tile);
        }
        return y += 1;
      };
      createTile = function(tile) {
        collisionMap[y][x] = getAccessible(tile);
        x += 1;
        if (x === len) {
          return x = 0;
        }
      };
      for (_i = 0, _len = tiles.length; _i < _len; _i++) {
        row = tiles[_i];
        createRow(row);
      }
      return this.collisionGraph = $.astar.graph(collisionMap);
    };
    Map.prototype.generateUI = function() {
      var addHtml, bottomRightCoord, nodeHeight, nodeWidth, purgeIds, tileEagerloadDepth, tiles, topLeftCoord, x1, x2, x2max, y1, y2, y2max;
      tileEagerloadDepth = this.tileEagerloadDepth;
      nodeWidth = this.nodeWidth;
      nodeHeight = this.nodeHeight;
      x2max = this.tileMap[0].length;
      y2max = this.tileMap.length;
      x1 = this.pos[0] - this.viewportHalfWidth;
      y1 = this.pos[1] - this.viewportHalfHeight;
      x2 = this.pos[0] + this.viewportHalfWidth;
      y2 = this.pos[1] + this.viewportHalfHeight;
      x1 = Math.floor(x1 / nodeWidth) - tileEagerloadDepth;
      y1 = Math.floor(y1 / nodeHeight) - tileEagerloadDepth;
      x2 = Math.floor(x2 / nodeWidth) + tileEagerloadDepth;
      y2 = Math.floor(y2 / nodeHeight) + tileEagerloadDepth;
      x1 = x1 < 0 ? 0 : x1;
      y1 = y1 < 0 ? 0 : y1;
      x2 = x2 > x2max ? x2max : x2;
      y2 = y2 > y2max ? y2max : y2;
      topLeftCoord = [x1, y1];
      bottomRightCoord = [x2, y2];
      tiles = this.getTilesToAddAndRemove(topLeftCoord, bottomRightCoord);
      addHtml = tiles[0];
      purgeIds = tiles[1];
      this.$tileMap.append(addHtml.join(''));
      return $(purgeIds.join(',')).remove();
    };
    Map.prototype.getCoordsByPos = function(left, top) {
      var xcoord, ycoord;
      xcoord = Math.floor(left / this.nodeWidth);
      ycoord = Math.floor(top / this.nodeHeight);
      return [xcoord, ycoord];
    };
    Map.prototype.getDirection = function(from, to) {
      var direction;
      direction = '';
      if (from[1] > to[1]) {
        direction += this.dir.N;
      } else if (from[1] < to[1]) {
        direction += this.dir.S;
      }
      if (from[0] > to[0]) {
        direction += this.dir.W;
      } else if (from[0] < to[0]) {
        direction += this.dir.E;
      }
      return direction;
    };
    Map.prototype.getSimpleDirection = function(direction) {
      if (direction.length === 2) {
        return direction.substr(0, 1);
      } else {
        return direction;
      }
    };
    Map.prototype.getPath = function(start, end) {
      var a, b, node, nodeHeight, nodeWidth, nodepath, path, x, y, _i, _len;
      try {
        a = this.collisionGraph.nodes[start[1]][start[0]];
        b = this.collisionGraph.nodes[end[1]][end[0]];
        path = $.astar.search(this.collisionGraph.nodes, a, b);
        nodepath = [];
        nodeWidth = this.nodeWidth;
        nodeHeight = this.nodeHeight;
        for (_i = 0, _len = path.length; _i < _len; _i++) {
          node = path[_i];
          x = node[0] * nodeWidth;
          y = node[1] * nodeHeight;
          nodepath.push([x, y]);
          return nodepath;
        }
      } catch (error) {
        return [];
      }
    };
    Map.prototype.getTilesToAddAndRemove = function(topLeftCoord, bottomRightCoord) {
      var addHtml, k, left, newViewableTiles, nodeHeight, nodeWidth, purgeIds, stub, tile, tileHeight, tileWidth, top, v, x, x1, x2, y, y1, y2, _ref;
      x1 = topLeftCoord[0];
      y1 = topLeftCoord[1];
      x2 = bottomRightCoord[0];
      y2 = bottomRightCoord[1];
      nodeWidth = this.nodeWidth;
      nodeHeight = this.nodeHeight;
      tileWidth = this.tileWidth;
      tileHeight = this.tileHeight;
      addHtml = [];
      purgeIds = [];
      newViewableTiles = {};
      y = y1;
      while (y < y2) {
        x = x1;
        while (x < x2) {
          if ((0 === y % 2 && 0 === x % 2) || (0 !== y % 2 && 0 !== x % 2)) {
            stub = 't_' + x + '_' + y;
            tile = this.tileMap[y][x];
            newViewableTiles[stub] = tile;
            if (!(this.viewableTiles[stub] != null)) {
              this.viewableTiles[stub] = tile;
              left = (x * nodeWidth - nodeWidth / 2) + 'px';
              top = (y * nodeHeight - nodeHeight / 2) + 'px';
              addHtml.push('<div id="' + stub + '" class="tile type-' + tile + '" style="z-index:' + y + ';left:' + left + ';top:' + top + ';width:' + tileWidth + 'px;height:' + tileHeight + 'px;"></div>');
            }
          }
          x++;
        }
        y++;
      }
      _ref = this.viewableTiles;
      for (k in _ref) {
        v = _ref[k];
        if (!(newViewableTiles[k] != null)) {
          delete this.viewableTiles[k];
          purgeIds.push('#' + k);
        }
      }
      return [addHtml, purgeIds];
    };
    Map.prototype.getTileType = function(xcoord, ycoord) {
      var x, y;
      x = Math.floor(xcoord / this.nodeWidth);
      y = Math.floor(ycoord / this.nodeHeight);
      if (void 0 === this.tileMap[y] || void 0 === this.tileMap[y][x]) {
        return false;
      }
      return this.tileMap[y][x];
    };
    Map.prototype.goTo = function(xcoord, ycoord) {
      this.setCoords(xcoord, ycoord);
      return this.$map.css({
        left: this.left + this.xOffset,
        top: this.top + this.yOffset
      });
    };
    Map.prototype.panStart = function(direction, xBound, yBound) {
      var loopId;
      if (xBound == null) {
        xBound = 0;
      }
      if (yBound == null) {
        yBound = 0;
      }
      loopId = 'pan_map_' + direction;
      return $.loop.add(loopId, __bind(function() {
        if (this.canShift(direction, xBound, yBound)) {
          this.$map.css(this.shift(direction));
          return user.el.css({
            zIndex: this.pos[1]
          });
        }
      }, this));
    };
    Map.prototype.panStop = function(direction) {
      return $.loop.remove('pan_map_' + direction);
    };
    Map.prototype.recenter = function() {
      this.setViewportInfo();
      return this.goTo(this.pos[0], this.pos[1]);
    };
    Map.prototype.setCoords = function(xcoord, ycoord) {
      this.pos[0] = xcoord;
      this.pos[1] = ycoord;
      this.left = xcoord * -1 + this.viewportHalfWidth;
      return this.top = ycoord * -1 + this.viewportHalfHeight;
    };
    Map.prototype.setViewportInfo = function() {
      this.viewportWidth = $(window).width();
      this.viewportHeight = $(window).height();
      this.viewportHalfWidth = parseInt(this.viewportWidth / 2, 10);
      return this.viewportHalfHeight = parseInt(this.viewportHeight / 2, 10);
    };
    Map.prototype.shift = function(direction) {
      var change, changeX, pos;
      change = this.change;
      changeX = change + 1;
      if (user.movingDiagonally()) {
        change -= 2;
        changeX -= 1;
      }
      if (direction === this.dir.W) {
        this.pos[0] -= changeX;
        this.left += changeX;
      } else if (direction === this.dir.E) {
        this.pos[0] += changeX;
        this.left -= changeX;
      } else if (direction === this.dir.N) {
        this.pos[1] -= change;
        this.top += change;
      } else if (direction === this.dir.S) {
        this.pos[1] += change;
        this.top -= change;
      }
      pos = {
        left: this.left + this.xOffset,
        top: this.top + this.yOffset
      };
      return pos;
    };
    Map.prototype.removeUnit = function(id) {
      delete this.npcs[id];
      delete this.players[id];
      return $('#' + this.unitStub + id).remove();
    };
    Map.prototype.startUIGenerator = function() {
      this.generateUI();
      return $.loop.add('map:ui:generator', 20, __bind(function() {
        return this.generateUI();
      }, this));
    };
    return Map;
  })();
}).call(this);
