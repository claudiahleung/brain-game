const ssvepDiv = document.querySelector('#ssvep-div');

function startSSVEPSession(command, freq) {
  console.log(command, 'has started', freq);
  ssvepDiv.style.display = 'block';

  let myp5 = new p5(sketch => {
    let x = 0;
    let dots = [
      {
        angle: sketch.PI / 2,
        frequency: 10,
      },
      {
        angle: sketch.PI / 2 + 2 * sketch.PI / 3,
        frequency: 12,
      },
      {
        angle: sketch.PI / 2 + 4 * sketch.PI / 3,
        frequency: 15,
      }
    ]

    let totalDuration = 1000 * command[1];

    let resetTime;

    // sketch.width contains the width of the canvas
    // same thing with sketch.height
    sketch.setup = () => {
      sketch.createCanvas(window.innerWidth, window.innerHeight);
      resetTime = sketch.millis();
    };

    sketch.draw = () => {
      sketch.background('black');
      sketch.translate(sketch.width / 2, sketch.height / 2);

      dots.forEach(({angle, frequency}) => {
        let radius = sketch.min(sketch.width, sketch.height) * 0.3;
        let numFrames = 60 / frequency;

        if (command[0] == 'RestSSVEP' || command[0] == 'Cue' ||
            sketch.frameCount % numFrames < numFrames / 2) {
          sketch.fill('white')
          sketch.noStroke();
          let x = radius * sketch.cos(angle);
          let y = radius * -sketch.sin(angle);

          sketch.ellipse(x, y, radius / 3);
          sketch.stroke('red');
          sketch.strokeWeight(10);
          sketch.noFill();
          if (frequency == freq) {
            sketch.ellipse(x, y, radius / 3);
          }
        }
      });

      if (hasEnded()) {
        console.log(command, 'has ended');
        sketch.noLoop();
        ssvepDiv.style.display = 'none';
        sketch.remove();
      }
    };

    sketch.windowResized = () => {
      sketch.resizeCanvas(window.innerWidth, window.innerHeight);
    }

    let epsilon = 70; // avoid race conditions lol ._.
    let hasEnded = () => sketch.millis() - resetTime + epsilon> totalDuration;
  }, 'ssvep-div');
}
