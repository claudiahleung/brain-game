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
      radius: NaN,
      speedX: 0,
    },
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
    if (sketch.keyIsDown(sketch.LEFT_ARROW)) {
        console.log(" left arrow ================", gameState.player.speedX);
        gameState.player.speedX = -0.5 * gameConfig.UNIT;
        console.log(" left arrow done ================", gameState.player.speedX);
    }  else if (sketch.keyIsDown(sketch.RIGHT_ARROW)) {
        console.log(" right arrow ================", gameState.player.speedX);
        gameState.player.speedX = 0.5 * gameConfig.UNIT;
        console.log(" right arrow done ================", gameState.player.speedX);
    }
  }

  sketch.keyReleased = () => {
    gameState.player.speedX = 0;
    console.log("key released==========");
  }

  sketch.update = () => {
    gameState.player.x += gameState.player.speedX;
  };

  sketch.drawScene = () => {
    sketch.background(220);
    sketch.ellipse(gameState.player.x, gameState.player.y,
      2 * gameState.player.radius);
  };
}, 'brain-game-div');
