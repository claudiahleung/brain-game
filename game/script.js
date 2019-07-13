/* eslint-disable */

const p5BrainGame = new p5(sketch => {
  const UNIT = 10;
  const config = {
    gapDist: NaN,
    gapWidth: NaN,
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
    gapsX: NaN,
    gapsY: NaN,
  };

  const player = state.player;

  sketch.setup = () => {
    sketch.createCanvas(300, 600);
    player.radius = 2 * UNIT
    player.x = sketch.width / 2;
    player.y = sketch.height / 2;
  }

  sketch.draw = () => {
    sketch.drawScene();
    sketch.update();
  };

  sketch.keyPressed = () => {
    if (sketch.keyIsDown(sketch.LEFT_ARROW)) {
        console.log(" left arrow ================", player.speedX);
        player.speedX = config.horizontalSpeed;
        console.log(" left arrow done ================", player.speedX);
    }  else if (sketch.keyIsDown(sketch.RIGHT_ARROW)) {
        console.log(" right arrow ================", player.speedX);
        player.speedX = -1 * config.horizontalSpeed;
        console.log(" right arrow done ================", player.speedX);
    }
  }

  sketch.keyReleased = () => {
    player.speedX = 0;
    console.log("key released==========");
  }

  sketch.update = () => {
    player.x += player.speedX;

    const playerBottomEdge = player.y + player.radius;
    if (playerBottomEdge !== sketch.height){
      player.y += player.speedY;
    }
  };

  sketch.drawScene = () => {
    sketch.background(220);
    sketch.ellipse(player.x, player.y,
      2 * player.radius);
  };
}, 'brain-game-div');
