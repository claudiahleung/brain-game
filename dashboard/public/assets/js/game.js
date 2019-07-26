/* eslint-disable */
const p5BrainGame = new p5(sketch => {
  const UNIT = 5;
  const config = {
    floorDist: 25 * UNIT,
    gapWidth: 15 * UNIT,
    floorHeight: 3 * UNIT,
    floorSpeed: UNIT / 6,
    bgColor: 'pink',
    horizontalSpeed: UNIT / 2,
    verticalSpeed: UNIT / 3,
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
    score: 0,
  };

  const player = state.player;

  class Floor {
    constructor() {
      this.x = sketch.random(0, sketch.width - config.gapWidth);
      this.y = sketch.height;
      this.passed = false;
    }

    update() {
      this.y -= config.floorSpeed;
    }

    draw() {
      sketch.stroke(config.bgColor);
      sketch.fill(0);
      sketch.rect(0, this.y, sketch.width, config.floorHeight);
      sketch.fill(config.bgColor);
      sketch.stroke(config.bgColor);
      sketch.rect(this.x, this.y, config.gapWidth, config.floorHeight);
      sketch.textSize(30);
      sketch.fill(0);
      sketch.text('Score: '+state.score, 10, 30);
    }

    isOutOfBounds() {
      return this.y + config.floorHeight < 0;
    }

    collisionHandling() {
      if (player.y + player.radius > this.y &&
        player.y - player.radius < this.y) {
          if (player.x - player.radius < this.x || player.x + player.radius > this.x + config.gapWidth) {
            player.y = this.y - player.radius;
          }
          // else if () {}
      }
      if (player.y - player.radius > this.y && !this.passed) {
        this.passed = true;
        state.score += 10;
      }
    }
  }

  sketch.reset = () => {
    state.floors = [new Floor()];
    state.player.x = sketch.width / 2;
    state.player.y = sketch.height /2;
    state.score = 0;
  };


  sketch.setup = () => {
    sketch.createCanvas(500, 500);
    player.radius = 2 * UNIT
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
    state.floors.forEach(floor => floor.update());
    state.floors.filter(floor => !floor.isOutOfBounds());
    const lastFloor = state.floors[state.floors.length - 1];

    if (lastFloor.y < sketch.height - config.floorDist) {
      state.floors.push(new Floor());
    }

    player.x += player.vx;

    state.floors.forEach(floor => floor.collisionHandling());

    if (player.y - player.radius <= 0) {
      sketch.reset();
    };

    const playerBottomEdge = player.y + player.radius;
    if (playerBottomEdge < sketch.height){
      player.y += player.vy;
    }
    if (player.x - player.radius <= 0) {
      player.x = player.radius
    }
    if (player.x + player.radius >= sketch.width) {
      player.x = sketch.width - player.radius
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
    sketch.ellipse(player.x, player.y,
      2 * player.radius);
  };
}, 'brain-game-div');
