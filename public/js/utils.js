(function() {
  this.requestAnimFrame = (function() {
    return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame || function(callback, element) {
      return window.setTimeout(callback, 1000 / 60);
    };
  })();
  this.random = function(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  };
  /*
  @scaleImage = (path, percentage, callback=100) ->
  
    if typeof percentage == 'function'
      [callback, percentage] = [percentage, callback]
  
    img = new Image()
    canvas = document.createElement("canvas")
    ctx = canvas.getContext("2d");
    canvasCopy = document.createElement("canvas")
    copyContext = canvasCopy.getContext("2d")
  
    maxWidth = 100
    maxHeight = 100
  
    img.onload = ->
  
      ratio = 1;
  
      if img.width > maxWidth
        ratio = maxWidth / img.width
      else if(img.height > maxHeight)
        ratio = maxHeight / img.height
  
      canvasCopy.width = img.width
      canvasCopy.height = img.height
      copyContext.drawImage(img, 0, 0)
  
      canvas.width = img.width * ratio
      canvas.height = img.height * ratio
      ctx.drawImage(canvasCopy, 0, 0, canvasCopy.width, canvasCopy.height, 0, 0, canvas.width, canvas.height)
  
  
    img.src = path
  */
}).call(this);
