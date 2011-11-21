(function() {
  var GRID_H, GRID_W, IMGPATH, STUB;
  var __hasProp = Object.prototype.hasOwnProperty, __extends = function(child, parent) {
    for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; }
    function ctor() { this.constructor = child; }
    ctor.prototype = parent.prototype;
    child.prototype = new ctor;
    child.__super__ = parent.prototype;
    return child;
  };
  IMGPATH = '/public/img/';
  GRID_W = 32;
  GRID_H = 16;
  STUB = 'prop-';
  this.Prop = (function() {
    function Prop(data) {
      this.id = data.id;
      this.kind = data.kind;
      this.x = data.x;
      this.y = data.y;
      this.left = this.x * GRID_W;
      this.top = this.y * GRID_H;
    }
    Prop.prototype.create = function() {
      if (!this.bgPos) {
        this.bgPos = '0 0';
      }
      return this.$el = $('<div/>', {
        id: STUB + this.id,
        "class": 'prop ' + this.type,
        css: {
          left: this.left - this.width / 2,
          top: this.top - this.height / 2,
          width: this.width,
          height: this.height,
          zIndex: this.top,
          background: 'no-repeat url(' + this.imgurl + ') ' + this.bgPos
        },
        data: {
          prop: this
        }
      });
    };
    return Prop;
  })();
  this.Tree = (function() {
    __extends(Tree, Prop);
    function Tree(data) {
      Tree.__super__.constructor.apply(this, arguments);
      this.height = 300;
      this.width = 300;
      this.type = data.type;
      this.imgurl = IMGPATH + 'sprite_tree.png';
      this.create();
    }
    return Tree;
  })();
  this.Rock = (function() {
    __extends(Rock, Prop);
    function Rock(data) {
      Rock.__super__.constructor.apply(this, arguments);
      this.height = 150;
      this.width = 150;
      this.type = data.type;
      this.imgurl = IMGPATH + 'sprite_rock.png';
      this.create();
    }
    return Rock;
  })();
  this.Tree1 = (function() {
    __extends(Tree1, Tree);
    function Tree1(data) {
      this.bgPos = '0 0';
      Tree1.__super__.constructor.apply(this, arguments);
    }
    return Tree1;
  })();
  this.Tree2 = (function() {
    __extends(Tree2, Tree);
    function Tree2(data) {
      this.bgPos = '-300px 0';
      Tree2.__super__.constructor.apply(this, arguments);
    }
    return Tree2;
  })();
  this.Tree3 = (function() {
    __extends(Tree3, Tree);
    function Tree3(data) {
      this.bgPos = '-600px 0';
      Tree3.__super__.constructor.apply(this, arguments);
    }
    return Tree3;
  })();
  this.Tree4 = (function() {
    __extends(Tree4, Tree);
    function Tree4(data) {
      this.bgPos = '-900px 0';
      Tree4.__super__.constructor.apply(this, arguments);
    }
    return Tree4;
  })();
  this.Rock1 = (function() {
    __extends(Rock1, Rock);
    function Rock1(data) {
      this.bgPos = '0 0';
      Rock1.__super__.constructor.apply(this, arguments);
    }
    return Rock1;
  })();
  this.Rock2 = (function() {
    __extends(Rock2, Rock);
    function Rock2(data) {
      this.bgPos = '-150px 0';
      Rock2.__super__.constructor.apply(this, arguments);
    }
    return Rock2;
  })();
  this.Rock3 = (function() {
    __extends(Rock3, Rock);
    function Rock3(data) {
      this.bgPos = '-300px 0';
      Rock3.__super__.constructor.apply(this, arguments);
    }
    return Rock3;
  })();
  this.Rock4 = (function() {
    __extends(Rock4, Rock);
    function Rock4(data) {
      this.bgPos = '-450px 0';
      Rock4.__super__.constructor.apply(this, arguments);
    }
    return Rock4;
  })();
}).call(this);
