(function() {
  this.util = {
    random: function(min, max) {
      return Math.floor(Math.random() * (max - min + 1)) + min;
    }
  };
}).call(this);
