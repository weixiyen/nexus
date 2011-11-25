(function() {
  var GRID_H, GRID_W, IMGPATH, STUB;
  var __hasProp = Object.prototype.hasOwnProperty, __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor; child.__super__ = parent.prototype; return child; };

  IMGPATH = '/public/img/';

  GRID_W = 32;

  GRID_H = 16;

  STUB = 'prop-';

  this.Prop = (function() {

    function Prop(data) {
      this.id = data.id;
      this.elementId = STUB + this.id;
      this.kind = data.kind;
      this.x = data.x;
      this.y = data.y;
      this.left = this.x * GRID_W;
      this.top = this.y * GRID_H;
      this.width = data.sprite.width;
      this.height = data.sprite.height;
      this.imgurl = IMGPATH + data.sprite.src;
    }

    Prop.prototype.create = function() {
      if (!this.bgPos) this.bgPos = '0 0';
      if (!this.topOffset) this.topOffset = 0;
      return this.$el = $('<div/>', {
        id: this.elementId,
        "class": 'prop',
        css: {
          left: this.left - this.width / 2,
          top: this.top - this.height,
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
      this.create();
    }

    return Tree;

  })();

  this.Rock = (function() {

    __extends(Rock, Prop);

    function Rock(data) {
      Rock.__super__.constructor.apply(this, arguments);
      this.create();
    }

    return Rock;

  })();

}).call(this);
