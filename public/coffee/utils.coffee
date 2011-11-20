@requestAnimFrame = (->
  return window.requestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    window.mozRequestAnimationFrame ||
    window.oRequestAnimationFrame ||
    window.msRequestAnimationFrame ||
    (callback, element) -> window.setTimeout(callback, 1000/60)
)()

@random = (min, max) ->
  return Math.floor(Math.random() * (max - min + 1)) + min