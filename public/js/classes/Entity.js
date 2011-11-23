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
      this.mp = data.mp;
      this.kind = data.kind;
      this.name = data.name;
      this.level = data.level;
      this.stats = data.stats;
      this.experience = data.experience;
      this.width = data.sprite.width;
      this.height = data.sprite.height;
      this.imgurl = IMGPATH + data.sprite.src;
      this.x = data.x;
      this.y = data.y;
      this.left = this.x * GRID_W;
      this.top = this.y * GRID_H;
      this.sprite = null;
      this.suppressInfo = false;
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
    Entity.prototype.userTargeted = function() {
      var imgurl;
      imgurl = IMGPATH + 'target_arrow.png';
      this.$targetArrow = $('<div/>').css({
        background: 'url(' + imgurl + ') no-repeat',
        height: 10,
        width: 10,
        position: 'absolute',
        left: this.width / 2 - 5,
        top: -35
      });
      this.$el.addClass('targeted');
      return this.$elBody.prepend(this.$targetArrow);
    };
    Entity.prototype.removeUserTarget = function() {
      this.$el.removeClass('targeted');
      return this.$targetArrow.remove();
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
      this.$elBody = $('<div/>', {
        "class": 'body',
        css: {
          height: this.height,
          width: this.width,
          background: 'no-repeat url(' + this.imgurl + ')',
          left: -Math.ceil(this.width / 2),
          top: -this.height,
          position: 'absolute'
        }
      });
      if (!this.suppressInfo) {
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
        this.$elBody.append(this.$elName, this.$elBar);
      }
      this.$el.append(this.$elBody);
      return this.setHp(this.hp);
    };
    Entity.prototype.setTarget = function(targetId) {
      return this.target = targetId;
    };
    Entity.prototype.getTarget = function() {
      return this.target;
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
      this.$elName.html(name);
      if (game.isUserId(this.id)) {
        return interface.setName(this.name);
      }
    };
    Entity.prototype.heal = function(amt) {
      return this.setHp(this.hp + amt);
    };
    Entity.prototype.takeDamage = function(amt, isCrit) {
      this.setHp(this.hp - amt);
      return this.gotHitEffect(isCrit);
    };
    Entity.prototype.setMovementSpeed = function(speed) {
      game.removeLoopItem('unit:' + this.id + ':move');
      this.speed = speed;
      return this.startMoving();
    };
    Entity.prototype.setHp = function(hp) {
      var perc;
      this.hp = hp;
      perc = Math.ceil(this.hp / this.stats.hp * 100);
      this.$elHp.css({
        width: perc + '%'
      });
      if (game.isUserId(this.id)) {
        return interface.setHp(perc);
      }
    };
    Entity.prototype.changeMp = function(amt) {
      return this.setMp(this.mp + amt);
    };
    Entity.prototype.setMp = function(mp) {
      var perc;
      this.mp = mp;
      perc = Math.ceil(this.mp / this.stats.mp * 100);
      if (!game.isUserId(this.id)) {
        return;
      }
      interface.setMp(perc);
      return interface.renderAbilityIconsByMp(this.mp);
    };
    Entity.prototype.increaseExperience = function(amt) {
      var perc;
      this.experience.have += amt;
      perc = Math.ceil(this.experience.have / this.experience.need * 100);
      if (!game.isUserId(this.id)) {
        return;
      }
      return interface.setXp(perc);
    };
    Entity.prototype.levelUp = function(data) {
      this.stats = data.stats;
      this.experience = data.experience;
      this.increaseExperience(0);
      this.setHp(data.hp);
      this.setMp(data.mp);
      return this.setLevel(data.level);
    };
    Entity.prototype.setLevel = function(level) {
      this.level = level;
      if (game.isUserId(this.id)) {
        return interface.setLevel(this.level);
      }
    };
    Entity.prototype.gotHitEffect = function(isCrit) {
      var $explosion, bgPos, imgurl, stub;
      if (this.suppressInfo === true) {
        return;
      }
      bgPos = '0 0';
      if (!isCrit) {
        bgPos = '-66px 0';
      }
      imgurl = IMGPATH + 'sprite_explosion_red.png';
      $explosion = $('<div/>').css({
        background: 'url(' + imgurl + ') no-repeat ' + bgPos,
        height: 66,
        width: 66,
        position: 'absolute',
        left: this.width / 2 - 33,
        top: 0,
        zIndex: 100
      });
      this.$elBody.prepend($explosion);
      stub = 'dmg:effect:' + this.id;
      return game.addLoopItem(stub, 5, function() {
        $explosion.remove();
        return game.removeLoopItem(stub);
      });
    };
    return Entity;
  })();
  this.MovableEntity = (function() {
    __extends(MovableEntity, Entity);
    function MovableEntity(entity) {
      MovableEntity.__super__.constructor.apply(this, arguments);
      this.speed = entity.movement_speed || 1;
      this.moving = false;
      this.endLeft = this.left;
      this.endTop = this.top;
      this.curDir = null;
    }
    MovableEntity.prototype.startMoving = function() {
      this.sprite = new Sprite({
        id: this.id,
        el: this.$elBody,
        skip: this.animationSkip
      });
      this.faceRandomDirection();
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
      if (this._movingDiagonally()) {
        changeX -= 2;
        changeY -= 1;
      }
      nextLeft = this.left;
      nextTop = this.top;
      if (this.top > this.endTop) {
        nextTop -= changeY;
        this.direction = 'n';
      }
      if (this.top < this.endTop) {
        nextTop += changeY;
        this.direction = 's';
      }
      if (this.left > this.endLeft) {
        nextLeft -= changeX;
        if (this.direction !== null) {
          this.direction += 'w';
        } else {
          this.direction = 'w';
        }
      }
      if (this.left < this.endLeft) {
        nextLeft += changeX;
        if (this.direction !== null) {
          this.direction += 'e';
        } else {
          this.direction = 'e';
        }
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
      var prevDir, skip;
      prevDir = this.curDir;
      if (this.curDir === this.direction) {
        return;
      }
      this.sprite.stop(this.id);
      this.curDir = this.direction;
      if (this.curDir === null) {
        return this.standFacing(prevDir);
      }
      skip = this.animationSkip;
      if (this.curDir === 'down' || this.curDir === 'up') {
        skip = Math.round(skip / 1.5);
      }
      return this.sprite.start(this.anim[this.curDir], skip);
    };
    MovableEntity.prototype.moveTo = function(x, y) {
      this.moving = true;
      this.endLeft = x * GRID_W - Math.round(this.width / 2) + Math.round(GRID_W / 2);
      return this.endTop = y * GRID_H - Math.round(this.height / 2) + GRID_H * 2;
    };
    MovableEntity.prototype.standFacing = function(direction) {
      return this.sprite.set(this.anim[direction][0]);
    };
    MovableEntity.prototype.faceRandomDirection = function() {
      var dirList, direction;
      dirList = ['n', 'e', 's', 'w', 'nw', 'ne', 'sw', 'se'];
      direction = dirList[random(0, 7)];
      return this.standFacing(direction);
    };
    return MovableEntity;
  })();
  this.Tower = (function() {
    __extends(Tower, Entity);
    function Tower(entity) {
      Tower.__super__.constructor.apply(this, arguments);
      this.create();
    }
    return Tower;
  })();
  this.Nexus = (function() {
    __extends(Nexus, Entity);
    function Nexus(entity) {
      Nexus.__super__.constructor.apply(this, arguments);
      this.create();
    }
    return Nexus;
  })();
  this.Minion = (function() {
    __extends(Minion, MovableEntity);
    function Minion(entity) {
      Minion.__super__.constructor.apply(this, arguments);
      this.animationSkip = 8;
      this.anim = {
        n: ["-50px 0", "-716px 0", "-776px 0", "-836px 0", "-896px 0", "-956px 0", "-1016px 0"],
        s: ["-207px 0", "-1766px 0", "-1824px 0", "-1883px 0", "-1941px 0", "-1999px 0", "-2058px 0"],
        w: ["-360px 0", "-2752px 0", "-2803px 0", "-2859px 0", "-2910px 0", "-2959px 0", "-3009px 0"],
        e: ["0 0", "-410px 0", "-461px 0", "-517px 0", "-568px 0", "-617px 0", "-667px 0"],
        ne: ["-107px 0", "-1076px 0", "-1132px 0", "-1184px 0", "-1239px 0", "-1299px 0", "-1362px 0"],
        se: ["-264px 0", "-2116px 0", "-2171px 0", "-2231px 0", "-2286px 0", "-2335px 0", "-2384px 0"],
        nw: ["-157px 0", "-1421px 0", "-1477px 0", "-1529px 0", "-1584px 0", "-1644px 0", "-1707px 0"],
        sw: ["-312px 0", "-2434px 0", "-2489px 0", "-2549px 0", "-2604px 0", "-2653px 0", "-2702px 0"]
      };
      this.create();
      this.startMoving();
    }
    return Minion;
  })();
  this.PlayerEntity = (function() {
    __extends(PlayerEntity, MovableEntity);
    function PlayerEntity(entity) {
      PlayerEntity.__super__.constructor.apply(this, arguments);
      this.type = 'user';
      this.animationSkip = 4;
      this.anim = {
        n: ["-63px 0", "-482px 0", "-515px 0", "-548px 0", "-581px 0", "-614px 0", "-647px 0"],
        s: ["-155px 0", "-1090px 0", "-1122px 0", "-1155px 0", "-1188px 0", "-1220px 0", "-1253px 0"],
        w: ["-253px 0", "-1696px 0", "-1733px 0", "-1766px 0", "-1797px 0", "-1833px 0", "-1865px 0"],
        e: ["0 0", "-282px 0", "-319px 0", "-352px 0", "-383px 0", "-419px 0", "-451px 0"],
        ne: ["-97px 0", "-680px 0", "-717px 0", "-749px 0", "-783px 0", "-821px 0", "-853px 0"],
        se: ["-189px 0", "-1286px 0", "-1322px 0", "-1355px 0", "-1389px 0", "-1425px 0", "-1459px 0"],
        nw: ["-126px 0", "-885px 0", "-922px 0", "-954px 0", "-988px 0", "-1026px 0", "-1058px 0"],
        sw: ["-221px 0", "-1491px 0", "-1527px 0", "-1560px 0", "-1594px 0", "-1630px 0", "-1664px 0"]
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
      this.animationSkip = 4;
      this.anim = {
        n: ["-63px 0", "-482px 0", "-515px 0", "-548px 0", "-581px 0", "-614px 0", "-647px 0"],
        s: ["-155px 0", "-1090px 0", "-1122px 0", "-1155px 0", "-1188px 0", "-1220px 0", "-1253px 0"],
        w: ["-253px 0", "-1696px 0", "-1733px 0", "-1766px 0", "-1797px 0", "-1833px 0", "-1865px 0"],
        e: ["0 0", "-282px 0", "-319px 0", "-352px 0", "-383px 0", "-419px 0", "-451px 0"],
        ne: ["-97px 0", "-680px 0", "-717px 0", "-749px 0", "-783px 0", "-821px 0", "-853px 0"],
        se: ["-189px 0", "-1286px 0", "-1322px 0", "-1355px 0", "-1389px 0", "-1425px 0", "-1459px 0"],
        nw: ["-126px 0", "-885px 0", "-922px 0", "-954px 0", "-988px 0", "-1026px 0", "-1058px 0"],
        sw: ["-221px 0", "-1491px 0", "-1527px 0", "-1560px 0", "-1594px 0", "-1630px 0", "-1664px 0"]
      };
      this.create();
      this.startMoving();
      this.setupInterface();
    }
    User.prototype.setupInterface = function() {
      this.increaseExperience(0);
      this.setLevel(this.level);
      return this.changeName(this.name);
    };
    return User;
  })();
  this.TowerAttack = (function() {
    __extends(TowerAttack, MovableEntity);
    function TowerAttack(entity) {
      TowerAttack.__super__.constructor.apply(this, arguments);
      this.animationSkip = 2;
      this.width = 33;
      this.height = 33;
      this.imgurl = IMGPATH + 'sprite_bolt_red.png';
      this.suppressInfo = true;
      this.anim = {
        n: ["0 -198px", "-33px -198px", "-66px -198px"],
        s: ["0 -66px", "-33px -66px", "-66px -66px"],
        w: ["0 0", "-33px 0", "-66px 0"],
        e: ["0 -132px", "-33px -132px", "-66px -132px"],
        ne: ["0 -165px", "-33px -165px", "-66px -165px"],
        se: ["0 -99px", "-33px -99px", "-66px -99px"],
        nw: ["0 -231px", "-33px -231px", "-66px -231px"],
        sw: ["0 -33px", "-33px -33px", "-66px -33px"]
      };
      this.create();
      this.startMoving();
    }
    TowerAttack.prototype.setHp = function() {
      return null;
    };
    TowerAttack.prototype.aggro = function() {
      return null;
    };
    return TowerAttack;
  })();
  /*
  class @User extends MovableEntity
    constructor: (entity)->
      super
      @type = 'user'
      @width = 40
      @height = 64
      @imgurl = IMGPATH + 'sprite_user.png'
      @animationSkip = 8
      @anim =
        w: [
          "0 0",
          "-50px 0",
          "-100px 0"
          ]
        n: [
          "-150px 0",
          "-200px 0",
          "-250px 0"
          ]
        s: [
          "-300px 0",
          "-350px 0",
          "-400px 0"
          ]
        e: [
          "-450px 0",
          "-500px 0",
          "-550px 0"
          ]
  
      @create()
      @startMoving()
  
  */
}).call(this);
