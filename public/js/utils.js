(function() {
  this.requestAnimFrame = (function() {
    return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame || function(callback, element) {
      return window.setTimeout(callback, 1000 / 60);
    };
  })();
  this.random = function(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  };
}).call(this);
