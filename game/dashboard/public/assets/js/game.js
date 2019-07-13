/* eslint-disable */
const p5BrainGame = new p5(sketch => {
  const UNIT = 5;
  const config = {
    floorDist: 25 * UNIT,
    gapWidth: 8 * UNIT,
    floorHeight: 3 * UNIT,
    floorSpeed: UNIT / 10,
    bgColor: 220,
    horizontalSpeed: UNIT / 2,
    verticalSpeed: UNIT / 10,
  };

  const state = {
    player: {
      x: NaN,
      y: NaN,
      radius: NaN,
      speedX: 0,
      speedY: config.verticalSpeed,
    },
    floors: [],
  };

  const player = state.player;

  class Floor {
    constructor() {
      this.x = sketch.random(0, sketch.width - config.gapWidth);
      this.y = sketch.height;
    }

    update() {
      this.y -= config.floorSpeed;
    }

    draw() {
      sketch.noStroke();
      sketch.fill(0);
      sketch.rect(0, this.y, sketch.width, config.floorHeight);
      sketch.fill(config.bgColor);
      sketch.stroke(config.bgColor);
      sketch.rect(this.x, this.y, config.gapWidth, config.floorHeight);
    }

    isOutOfBounds() {
      return this.y + config.floorHeight < 0;
    }

    collisionDetection() {

    }
  }

  sketch.reset = () => {
    state.floors = [new Floor()];
    state.player.x = sketch.width / 2;
    state.player.y = sketch.height /2;
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
        player.speedX = config.horizontalSpeed;
    }  else if (sketch.keyIsDown(sketch.LEFT_ARROW)) {
        player.speedX = -config.horizontalSpeed;
    }
  }

  sketch.keyReleased = () => {
    player.speedX = 0;
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

    player.x += player.speedX;

    const playerBottomEdge = player.y + player.radius;
    if (playerBottomEdge < sketch.height){
      player.y += player.speedY;
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