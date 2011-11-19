(function() {
  var GRID_H, GRID_W, IMGPATH, STEP_X, STEP_Y;
  var __hasProp = Object.prototype.hasOwnProperty, __extends = function(child, parent) {
    for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; }
    function ctor() { this.constructor = child; }
    ctor.prototype = parent.prototype;
    child.prototype = new ctor;
    child.__super__ = parent.prototype;
    return child;
  }, __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  IMGPATH = '/public/img/';
  GRID_W = 64;
  GRID_H = 32;
  STEP_X = 4;
  STEP_Y = 5;
  this.Entity = (function() {
    var STUB;
    STUB = 'ent-';
    function Entity(data) {
      this.id = data.id;
      this.hp = data.hp;
      this.kind = data.kind;
      this.name = data.name;
      this.x = data.x;
      this.y = data.y;
      this.left = this.x * GRID_W;
      this.top = this.y * GRID_H;
      this.target = data.target || null;
    }
    Entity.prototype.isAlive = function() {
      return this.hp > 0;
    };
    Entity.prototype.hasTarget = function() {
      if (this.target) {
        return true;
      } else {
        return false;
      }
    };
    Entity.prototype.create = function() {
      this.$el = $('<div/>', {
        id: STUB + this.id,
        "class": 'entity',
        css: {
          left: this.left,
          top: this.top,
          zIndex: this.top
        }
      });
      this.$elBody = $('<div/>').css({
        height: this.height,
        width: this.width,
        background: 'no-repeat url(' + this.imgurl + ')',
        left: this.width / 2 * -1,
        top: this.height * -1
      });
      return this.$el.append(this.$elBody);
    };
    Entity.prototype.remove = function() {
      return this.$el.remove();
    };
    return Entity;
  })();
  this.MovableEntity = (function() {
    __extends(MovableEntity, Entity);
    function MovableEntity(entity) {
      MovableEntity.__super__.constructor.apply(this, arguments);
      this.speed = entity.speed || Infinity;
      this.moving = false;
      this.endLeft = this.left;
      this.endTop = this.top;
    }
    MovableEntity.prototype.startMoving = function() {
      return game.registerLoopItem('unit:' + this.id + ':move', this.speed, __bind(function() {
        if (!this.moving) {
          return;
        }
        return this._moveTowardsGoal();
      }, this));
    };
    MovableEntity.prototype._moveTowardsGoal = function() {
      var changeX, changeY, nextLeft, nextTop, stopX, stopY;
      stopX = stopY = false;
      changeX = STEP_X;
      changeY = STEP_Y;
      if (this._movingDiagonally()) {
        changeX -= 2;
        changeY -= 1;
      }
      nextLeft = this.left;
      nextTop = this.top;
      if (this.left > this.endLeft) {
        nextLeft -= changeX;
      }
      if (this.left < this.endLeft) {
        nextLeft += changeX;
      }
      if (this.top > this.endTop) {
        nextTop -= changeY;
      }
      if (this.top < this.endTop) {
        nextTop += changeY;
      }
      if (Math.abs(this.left - this.endLeft) <= STEP_X) {
        nextLeft = this.endLeft;
        stopX = true;
      }
      if (Math.abs(this.top - this.endTop) <= STEP_Y) {
        nextTop = this.endTop;
        stopY = true;
      }
      if (stopX && stopY) {
        this.moving = false;
      }
      this.left = nextLeft;
      this.top = nextTop;
      return this.$el.css({
        left: this.left,
        top: this.top,
        zIndex: this.top
      });
    };
    MovableEntity.prototype._movingDiagonally = function() {
      if (this.left !== this.endLeft && this.top !== this.endTop) {
        return true;
      }
      return false;
    };
    return MovableEntity;
  })();
  this.Monster = (function() {
    __extends(Monster, MovableEntity);
    function Monster(entity) {
      Monster.__super__.constructor.apply(this, arguments);
      this.speed = 4;
      this.width = 65;
      this.height = 60;
      this.imgurl = IMGPATH + 'sprite_monster.png';
      this.create();
      this.startMoving();
    }
    Monster.prototype.moveTo = function(x, y) {
      this.moving = true;
      this.endLeft = x * GRID_W;
      return this.endTop = y * GRID_H;
    };
    return Monster;
  })();
  this.Player = (function() {
    __extends(Player, MovableEntity);
    function Player(entity) {
      Player.__super__.constructor.apply(this, arguments);
      this.speed = 3;
      this.width = 40;
      this.height = 64;
      this.imgurl = IMGPATH + 'sprite_user.png';
      this.create();
    }
    Player.prototype.moveTo = function(x, y) {};
    return Player;
  })();
}).call(this);