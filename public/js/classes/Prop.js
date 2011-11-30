(function() {
  var GRID_H, GRID_W, IMGPATH, STUB;
  IMGPATH = '/public/img/';
  GRID_W = 32;
  GRID_H = 16;
  STUB = 'prop-';
  this.Prop = (function() {
    function Prop(data) {
      this.id = data.id;
      this.elementId = STUB + this.id;
      this.kind = data.kind;
      this.x = data.components.position.x;
      this.y = data.components.position.y;
      this.left = this.x * GRID_W;
      this.top = this.y * GRID_H;
      this.width = data.components.sprite.width;
      this.height = data.components.sprite.height;
      this.imgurl = IMGPATH + data.components.sprite.src;
      this.create();
    }
    Prop.prototype.create = function() {
      if (!this.bgPos) {
        this.bgPos = '0 0';
      }
      if (!this.topOffset) {
        this.topOffset = 0;
      }
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
}).call(this);
