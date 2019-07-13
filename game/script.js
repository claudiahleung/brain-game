/* eslint-disable */
const p5BrainGame = new p5(sketch => {
  let gameConfig = {
    gapDist: NaN,
    gapWidth: NaN,
    UNIT: 10,
  };

  let gameState = {
    player: {
      x: NaN,
      y: NaN,
      radius: NaN
    },
    // player.x: NaN,
    // player.y: NaN,
    // player.radius: NaN,
    gapsX: NaN,
    gapsY: NaN,
  };

  sketch.setup = () => {
    sketch.createCanvas(300, 600);
    gameState.player.radius = 2 * gameConfig.UNIT
    gameState.player.x = sketch.width / 2;
    gameState.player.y = sketch.height /2;
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
    gameState.player.x -= gameConfig.UNIT / 5;
  }

  sketch.moveRight = () => {
    gameState.player.x += gameConfig.UNIT / 5;
  }

  sketch.update = () => {

  };

  sketch.drawScene = () => {
    sketch.background(220);
    sketch.ellipse(gameState.player.x, gameState.player.y,
      2 * gameState.player.radius);
  };
}, 'brain-game-div');
