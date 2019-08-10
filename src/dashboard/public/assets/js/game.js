/* eslint-disable */
const p5BrainGame = new p5(sketch => {
  const UNIT = 5;
  const config = {
    floorDist: 25 * UNIT,
    gapWidth: 15 * UNIT,
    floorHeight: 3 * UNIT,
    floorSpeed: UNIT / 3,
    bgColor: 220,
    horizontalSpeed: UNIT,
    verticalSpeed: UNIT,
    
    // added how much to increase the speed of the camera by
    cameraSpeedRamp: 0.3,
    
    // added a way to scroll up the camera so that player stays in focus
    scrollCameraThreshold: parseInt(2/3 * 500),
  };

  const state = {
    player: {
      x: NaN,
      y: NaN,
      radius: NaN,
      vx: 0,
      vy: config.verticalSpeed,
    },
    floors: [],
    
    // removed floorspeed and replaced with cameraVelocity
    // floorSpeed: UNIT / 3,

    // created a variable to store how fast the camera is scrolling upwards
    cameraVelocity: -UNIT / 3,
    
    score: 0,
    
    // cameraY scrolls everything (player & floors) up by its value of pixels 
    cameraY: 0
  };

  const player = state.player;

  class Floor {
    constructor() {
      this.x = sketch.random(0, sketch.width - config.gapWidth);

      // added cameraY
      this.y = sketch.height - state.cameraY; 
      this.passed = false;
    }

    update() {
      // don't need this
      // this.y -= state.floorSpeed;
    }

    draw() {
      sketch.stroke(config.bgColor);
      sketch.fill(0);
      
      // added cameraY
      sketch.rect(0, this.y + state.cameraY, sketch.width, config.floorHeight);
      sketch.fill(config.bgColor);
      sketch.stroke(config.bgColor);
      
      // added cameraY
      sketch.rect(this.x, this.y + state.cameraY, config.gapWidth, config.floorHeight);
      sketch.textSize(30);
      sketch.fill(0);
      sketch.text('Score: '+ state.score, 10, 30);
    }

    isOutOfBounds() {
      // added cameraY
      return this.y + config.floorHeight + state.cameraY < 0;
    }

    collisionHandling() {
      if (player.y + player.radius > this.y &&
        player.y - player.radius < this.y) {
          if (player.x - player.radius < this.x || player.x + player.radius > this.x + config.gapWidth) {
            player.y = this.y - player.radius;
            player.vy = config.verticalSpeed;
          }
          // else if () {}
      }
      if (player.y - player.radius > this.y && !this.passed) {
        this.passed = true;
        state.score += 10;
        state.floorSpeed = state.score / 10;

        // increase speed of camera instead of floor
        state.cameraVelocity -= config.cameraSpeedRamp;
      }
    }
  }

  sketch.reset = () => {
    state.cameraY = 0;
    state.floors = [new Floor()];
    state.player.x = sketch.width / 2;
    state.player.y = sketch.height /2;
    state.score = 0;
    //state.floorSpeed = UNIT / 3

    // replaced floorspeed with cameravelocity
    state.cameraVelocity = -UNIT / 3;
  };


  sketch.setup = () => {
    sketch.createCanvas(500, 500);
    player.radius = 2 * UNIT;
    player.x = sketch.width / 2;
    player.y = sketch.height / 2;
    sketch.reset();
  }

  sketch.draw = () => {
    sketch.drawScene();
    sketch.update();
  };

  sketch.keyPressed = () => {
    if (sketch.keyIsDown(sketch.RIGHT_ARROW)) {
        player.vx = config.horizontalSpeed;
    }  else if (sketch.keyIsDown(sketch.LEFT_ARROW)) {
        player.vx = -config.horizontalSpeed;
    }
  }

  sketch.keyReleased = () => {
    player.vx = 0;
  }

  sketch.moveLeft = () => {
    state.player.x -= UNIT / 5;
  }

  sketch.moveRight = () => {
    state.player.x += UNIT / 5;
  }

  sketch.update = () => {

    // added cameraVelocity to cameraY
    state.cameraY += state.cameraVelocity;
    
    state.floors.forEach(floor => floor.update());
    state.floors.filter(floor => !floor.isOutOfBounds());
    const lastFloor = state.floors[state.floors.length - 1];

    // added cameraY
    if (lastFloor.y + state.cameraY < sketch.height - config.floorDist) {
      state.floors.push(new Floor());
    }

    player.x += player.vx;

    state.floors.forEach(floor => floor.collisionHandling());

    // added cameraY
    if (player.y - player.radius + state.cameraY <= 0) {
      sketch.reset();
    };

    // no longer need this 
    // const playerBottomEdge = player.y + player.radius + state.cameraY;
    // if (playerBottomEdge < sketch.height) {
    //   player.y += player.vy;
    // }

    if (player.x - player.radius <= 0) {
      player.x = player.radius
    }
    if (player.x + player.radius >= sketch.width) {
      player.x = sketch.width - player.radius
    }
    
    // make the player fall vertically
    player.y += player.vy;

    // if player falls below threshold, scrolls up the camera to stay in view
    if (player.y + state.cameraY > config.scrollCameraThreshold) {
      state.cameraY -= 1;
    }
  };

  sketch.drawScene = () => {
    sketch.background(config.bgColor);
    sketch.drawFloors();
    sketch.drawPlayer();
  };

  sketch.drawFloors = () => {
    state.floors.forEach(floor => floor.draw());
  }

  sketch.drawPlayer = () => {
    sketch.noStroke();
    sketch.fill(0);
    sketch.ellipse(player.x, player.y + state.cameraY,
      2 * player.radius);
  };
}, 'brain-game-div');