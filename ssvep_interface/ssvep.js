let myp5 = new p5(sketch => {
  let x = 0;

  // sketch.width contains the width of the canvas
  // same thing with sketch.height
  sketch.setup = () => {
    sketch.createCanvas(600, 400);
  };

  sketch.draw = () => {
    sketch.background(5);
    sketch.fill('white')
    sketch.ellipse(100,100,60);
    sketch.ellipse(200,50,60);
    sketch.ellipse(300,100,60);
    sketch.ellipse(200,300,60);

  };
}, 'ssvep-div');
