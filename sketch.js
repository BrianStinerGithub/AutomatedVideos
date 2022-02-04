// var song
var songs = []
var fft
var particles = []
var backgroundimage
var focus
var s

function preload() {

  for(var i = 0; i < 20; i++) {
    songs.push(loadSound('audio/audio'+(i+1)+'.mp3'))
    console.log(songs[i].duration())
  }
  
  img = loadImage('picture/image.png')
}

function setup() {
  createCanvas(1920, 1080)
  fft = new p5.FFT()
  imageMode(CENTER)
  angleMode(DEGREES)

  focus = {x: 250, y: 250}
  s=1

  //backgroundimage = new AnimatedImage(img)
}

function draw() {

  // This controls starting and stopping the clip recording between songs
  console.log(frameCount, floor(songs[s].duration() * 24))
  if (!songs[s].isPlaying() && frameCount > 10) {
    console.log("-----------------end of song----------------")
    capturer.stop()
    capturer.save()
    frameCount = 1
    s++
  } 
  if( frameCount === 1 ) {
    console.log("-----------------start of song----------------")
    capturer.start()
    songs[s].play()
  }

  // setup the drawing environment
  background(50)
  stroke(225)
  strokeWeight(2)
  noFill()
  translate(width/2 +focus.x, height/2 +focus.y)

  // extract frequency data
  fft.analyze()
  low = fft.getEnergy(1, 120)
  mid = fft.getEnergy(80, 220)
  high = fft.getEnergy(160, 255)
  wave = fft.waveform()

  // bass animated image
  push()
  if( low > 220 ) {
    image(img, -focus.x, -focus.y, width -220 +low, height -220 +low)
  } else {
    image(img, -focus.x, -focus.y, width, height)
  }
  pop()

  
  // background.update(low)
  // background.display()
  
  
  // Waveform circle animation
  for (var q = -1; q <= 2; q += 2) {                            
    beginShape()
    for (var i = 0; i < 180; i+=0.5) {
      var index = floor(map(i, 0, 180, 0, wave.length - 1))

      var r = map(wave[index], -1, 1, 150, 350)
      
      var x = r * sin(i) * q
      var y = r * cos(i)
      vertex(x, y)
    }
    endShape()
  }

  var p = new Particle()
  particles.push(p)

  for (var i = particles.length -1; i >= 0; i--) {
    if (!particles[i].edges()) {
      particles[i].update(mid)
      particles[i].show(high>220)
    } else {
      particles.splice(i, 1)
    }
  }

  capturer.capture(document.getElementById('defaultCanvas0'))
}

function mousePressed() {
  if (songs[s].isPlaying()) {
    songs[s].pause()
    noLoop()
  } else {
    songs[s].play()
    loop()
  }
}




class Particle {
  constructor() {
    this.pos = p5.Vector.random2D().mult(250)
    this.vel = createVector(0, 0)
    this.acc = this.pos.copy().mult(random(.0001, .00001))
    this.w = random(2, 6)
  }
  update(value) {
    this.vel.add(this.acc)
    this.pos.add(this.vel.mult(value*.0048))
  }
  edges() {
    if (this.pos.x > width/2 +focus.x || this.pos.x < -width/2 -focus.x || this.pos.y > height/2 +focus.y || this.pos.y < -height/2 -focus.y) {
      return true
    }return false
  }
  show(cond) {
    noStroke()
    if(cond){
      fill(180, 180, 180)
    } else {
      fill(255, 255, 255)
    }
    ellipse(this.pos.x, this.pos.y, this.w)
  }
}

class AnimatedImage {
  constructor(img) {
    this.img = img
    this.w = this.img.width
    this.h = this.img.height
    this.pos = createVector(width / 2, height / 2)
    this.vel = createVector(0, 0)
    this.acc = createVector(0, 0)

  }
  update(low) {
    this.w = 1920 + low/10
    this.h = 1080 + low/10

    if (low>220) {
      this.acc.add(createVector(random(-1, 1), random(-1, 1)))
    }

    this.acc.add(createVector(width / 2, height / 2))
    this.vel.add(this.acc)
    this.pos.add(this.vel)

  }
  display() {
    image(this.img, 0, 0, this.w, this.h)
  }

}

function timetoframes(seconds, fps = 24) {
  return seconds * fps
}