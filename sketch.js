var song
var fft

function preload() {
  song = loadSound('audio.mp3');
}

function setup() {
  createCanvas(windowWidth, windowHeight);
  fft = new p5.FFT();

  background(50);
  stroke(205);
  nofill();
  textSize(32);
  textAlign(CENTER, CENTER);
  text("Javascript works", width/2, height/2);

}

function draw() {
  var wave = fft.waveform();

  for (var i = 0; i < wave.length; i++) {
    var x = map(i, 0, wave.length, 0, width);
    var y = map(wave[i], -1, 1, 0, height);
    rect(x, y, 10, 10);
  }

}

function mousePressed() {
  if (song.isPlaying()) {
    song.stop();
  } else {
    song.play();
  }
}