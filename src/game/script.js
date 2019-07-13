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
    playerX: NaN,
    playerY: NaN,
    playerRadius: NaN,
    gapsX: NaN,
    gapsY: NaN,
  };

  sketch.setup = () => {
    sketch.createCanvas(300, 600);
    gameState.playerRadius = 2 * gameConfig.UNIT
    gameState.playerX = sketch.width / 2;
    gameState.playerY = sketch.height /2;
  }

  sketch.draw = () => {
    sketch.drawScene();
    sketch.update();
  };

  sketch.keyPressed = () => {
    if (sketch.keyCode === sketch.LEFT_ARROW) {
      console.log(" left arrow ================");
    } else if (sketch.keyCode === sketch.RIGHT_ARROW) {
      console.log(" right arrow ================");
    }
  }

  sketch.update = () => {

  };

  sketch.drawScene = () => {
    sketch.background(220);
    sketch.ellipse(gameState.playerX, gameState.playerY,
      2 * gameState.playerRadius);
  };
}, 'brain-game-div');
