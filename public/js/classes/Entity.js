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
  GRID_W = 32;
  GRID_H = 16;
  STEP_X = 5;
  STEP_Y = 3;
  this.Entity = (function() {
    var STUB;
    STUB = 'ent-';
    function Entity(data) {
      this.id = data.id;
      this.hp = data.hp;
      this.kind = data.kind;
      this.name = data.name;
      this.stats = data.stats;
      this.x = data.x;
      this.y = data.y;
      this.left = this.x * GRID_W;
      this.top = this.y * GRID_H;
      this.sprite = null;
      this.target = data.target || null;
      this.type = 'unit';
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
        "class": 'entity ' + this.type,
        css: {
          left: this.left,
          top: this.top,
          zIndex: this.top
        },
        data: {
          entity: this
        }
      });
      this.$elBody = $('<div/>').css({
        height: this.height,
        width: this.width,
        background: 'no-repeat url(' + this.imgurl + ')',
        left: this.width / 2 * -1,
        top: this.height * -1
      });
      this.$elName = $('<div/>', {
        "class": 'name',
        css: {
          left: this.width / 2 - 50,
          top: -25
        }
      });
      this.$elName.html(this.name);
      this.$elBar = $('<div/>', {
        "class": 'bar br2',
        css: {
          left: this.width / 2 - 25,
          top: -10
        }
      });
      this.$elHp = $('<div/>', {
        "class": 'hp br2'
      });
      this.$elBar.append(this.$elHp);
      this.$el.append(this.$elName, this.$elBar, this.$elBody);
      return this.setHp(this.hp);
    };
    Entity.prototype.remove = function() {
      return this.$el.remove();
    };
    Entity.prototype.setCoords = function() {
      this.x = Math.floor(this.left / GRID_W);
      return this.y = Math.floor(this.top / GRID_H);
    };
    Entity.prototype.aggro = function(id) {
      this.target = id;
      return this.$elName.addClass('red');
    };
    Entity.prototype.deaggro = function() {
      this.target = null;
      return this.$elName.removeClass('red');
    };
    Entity.prototype.changeName = function(name) {
      this.name = name;
      return this.$elName.html(name);
    };
    Entity.prototype.takeDamage = function(amt, isCrit) {
      return this.setHp(this.hp - amt);
    };
    Entity.prototype.setHp = function(hp) {
      var perc;
      this.hp = hp;
      perc = Math.ceil(this.hp / this.stats.hp * 100) + '%';
      return this.$elHp.css({
        width: perc
      });
    };
    return Entity;
  })();
  this.MovableEntity = (function() {
    __extends(MovableEntity, Entity);
    function MovableEntity(entity) {
      MovableEntity.__super__.constructor.apply(this, arguments);
      this.speed = entity.stats.movement_speed || 1;
      this.moving = false;
      this.endLeft = this.left;
      this.endTop = this.top;
      this.curDir = null;
    }
    MovableEntity.prototype.startMoving = function() {
      return game.addLoopItem('unit:' + this.id + ':move', this.speed, __bind(function() {
        if (!this.moving) {
          return;
        }
        return this._moveTowardsGoal();
      }, this));
    };
    MovableEntity.prototype._moveTowardsGoal = function() {
      var changeX, changeY, nextLeft, nextTop, stopX, stopY;
      stopX = stopY = false;
      this.direction = null;
      changeX = STEP_X;
      changeY = STEP_Y;
      /*
          if @_movingDiagonally()
            changeX -= 2
            changeY -= 1
          */
      nextLeft = this.left;
      nextTop = this.top;
      if (this.top > this.endTop) {
        nextTop -= changeY;
        this.direction = 'up';
      }
      if (this.top < this.endTop) {
        nextTop += changeY;
        this.direction = 'down';
      }
      if (this.left > this.endLeft) {
        nextLeft -= changeX;
        this.direction = 'left';
      }
      if (this.left < this.endLeft) {
        nextLeft += changeX;
        this.direction = 'right';
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
        this.direction = null;
      }
      this.left = nextLeft;
      this.top = nextTop;
      this.$el.css({
        left: this.left,
        top: this.top,
        zIndex: this.top
      });
      return this.walk();
    };
    MovableEntity.prototype._movingDiagonally = function() {
      if (this.left !== this.endLeft && this.top !== this.endTop) {
        return true;
      }
      return false;
    };
    MovableEntity.prototype.walk = function() {
      var skip;
      if (this.curDir === this.direction) {
        return;
      }
      if (this.sprite) {
        this.sprite.stop(this.id);
      } else {
        this.sprite = new Sprite({
          id: this.id,
          el: this.$elBody,
          skip: this.animationSkip
        });
      }
      this.curDir = this.direction;
      if (this.curDir === null) {
        return;
      }
      skip = this.animationSkip;
      if (this.curDir === 'down' || this.curDir === 'up') {
        skip = Math.round(skip / 1.5);
      }
      return this.sprite.start(this.anim[this.curDir], skip);
    };
    MovableEntity.prototype.moveTo = function(x, y) {
      this.moving = true;
      this.endLeft = x * GRID_W - Math.floor(this.width / 2);
      return this.endTop = y * GRID_H - Math.floor(this.height / 2);
    };
    return MovableEntity;
  })();
  this.Turret = (function() {
    __extends(Turret, Entity);
    function Turret(entity) {
      Turret.__super__.constructor.apply(this, arguments);
      this.width = 96;
      this.height = 96;
      this.imgurl = IMGPATH + 'turret.png';
      this.create();
    }
    return Turret;
  })();
  this.Lizard = (function() {
    __extends(Lizard, MovableEntity);
    function Lizard(entity) {
      Lizard.__super__.constructor.apply(this, arguments);
      this.width = 65;
      this.height = 60;
      this.animationSkip = 10;
      this.imgurl = IMGPATH + 'sprite_monster.png';
      this.anim = {
        down: ["0 0", "-65px 0", "-130px 0"],
        up: ["-195px 0", "-260px 0", "-325px 0"],
        left: ["-390px 0", "-455px 0", "-520px 0"],
        right: ["-585px 0", "-650px 0", "-715px 0"]
      };
      this.create();
      this.startMoving();
    }
    return Lizard;
  })();
  this.PlayerEntity = (function() {
    __extends(PlayerEntity, MovableEntity);
    function PlayerEntity(entity) {
      PlayerEntity.__super__.constructor.apply(this, arguments);
      this.type = 'player';
      this.width = 40;
      this.height = 64;
      this.imgurl = IMGPATH + 'sprite_user.png';
      this.animationSkip = 8;
      this.anim = {
        left: ["0 0", "-50px 0", "-100px 0"],
        up: ["-150px 0", "-200px 0", "-250px 0"],
        down: ["-300px 0", "-350px 0", "-400px 0"],
        right: ["-450px 0", "-500px 0", "-550px 0"]
      };
      this.create();
      this.startMoving();
    }
    return PlayerEntity;
  })();
  this.User = (function() {
    __extends(User, MovableEntity);
    function User(entity) {
      User.__super__.constructor.apply(this, arguments);
      this.type = 'user';
      this.width = 40;
      this.height = 64;
      this.imgurl = IMGPATH + 'sprite_user.png';
      this.animationSkip = 8;
      this.anim = {
        left: ["0 0", "-50px 0", "-100px 0"],
        up: ["-150px 0", "-200px 0", "-250px 0"],
        down: ["-300px 0", "-350px 0", "-400px 0"],
        right: ["-450px 0", "-500px 0", "-550px 0"]
      };
      this.create();
      this.startMoving();
    }
    return User;
  })();
}).call(this);
