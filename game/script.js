/* eslint-disable */
const p5BrainGame = new p5(sketch => {
  const UNIT = 10;
  let gameConfig = {
    floorDist: 15 * UNIT,
    gapWidth: 8 * UNIT,
    floorHeight: 3 * UNIT,
    floorSpeed: UNIT / 10,
    bgColor: 220,
  };

  let gameState = {
    player: {
      x: NaN,
      y: NaN,
      radius: NaN
    },
    floors: [],
  };

  class Floor {
    constructor() {
      this.x = sketch.random(0, sketch.width - gameConfig.gapWidth);
      this.y = sketch.height;
    }

    update() {
      this.y -= gameConfig.floorSpeed;
    }

    draw() {
      sketch.fill(0);
      sketch.rect(0, this.y, sketch.width, gameConfig.floorHeight);
      sketch.fill(gameConfig.bgColor);
      sketch.rect(this.x, this.y, gameConfig.gapWidth, gameConfig.floorHeight);
    }
  }

  sketch.reset = () => {
    gameState.floors = [new Floor()];
    gameState.player.x = sketch.width / 2;
    gameState.player.y = sketch.height /2;
  }

  sketch.setup = () => {
    sketch.createCanvas(300, 600);
    sketch.noStroke();
    gameState.player.radius = 2 * UNIT;
    sketch.reset();
  }

  sketch.draw = () => {
    sketch.drawScene();
    sketch.update();
  };

  sketch.keyPressed = () => {
    if (sketch.keyCode === sketch.LEFT_ARROW) {
      console.log(" left arrow ================", gameState.player.x);
      sketch.moveLeft();
      console.log(" left arrow done ================", gameState.player.x);
    } else if (sketch.keyCode === sketch.RIGHT_ARROW) {
      console.log(" right arrow ================", gameState.player.x);
      sketch.moveRight();
      console.log(" right arrow done ================", gameState.player.x);
    }
  }

  sketch.moveLeft = () => {
    gameState.player.x -= UNIT / 5;
  }

  sketch.moveRight = () => {
    gameState.player.x += UNIT / 5;
  }

  sketch.update = () => {
    gameState.floors.forEach(floor => floor.update());
    const lastFloor = gameState.floors[gameState.floors.length - 1];

    if (lastFloor.y < sketch.height - gameConfig.floorDist) {
      gameState.floors.push(new Floor());
    }
  };

  sketch.drawScene = () => {
    sketch.background(gameConfig.bgColor);
    sketch.drawFloors();
    sketch.drawPlayer();
  };

  sketch.drawFloors = () => {
    gameState.floors.forEach(floor => floor.draw());
  }

  sketch.drawPlayer = () => {
    sketch.fill(0);
    sketch.ellipse(gameState.player.x, gameState.player.y,
      2 * gameState.player.radius);
  }
}, 'brain-game-div');
