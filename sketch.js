var song
var fft

function preload() {
  song = loadSound('Blackstripe - Boobs.mp3')
}

function setup() {
  createCanvas(windowWidth, windowHeight)
  fft = new p5.FFT()

}

function draw() {
  background(50)
  stroke(225)
  noFill()

  var wave = fft.waveform()

  beginShape()
  for (var x = 0; x < width; x++) {
    var index = floor(map(x, 0, width, 0, wave.length))
    var y = wave[index]* 300 + height/2
    vertex(x, y)
  }
  endShape()

}

function mousePressed() {
  if (song.isPlaying()) {
    song.pause()
    noLoop()
  } else {
    song.play()
    loop()
  }
}