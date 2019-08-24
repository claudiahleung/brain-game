$(document).ready(function() {
  console.log("List javascript loaded!");
  var trialName;
  //SETS ACTIVE TO ALL OF THEM FOR NOW!
  var active = [1,1,1,1,1,1,1,1];
  //Made global so stop button can clear it
  var collectionTimer = null;
  var currentProtocol = [];

  // when the Collect button is clicked
  $(".selection").click(function() {
    var clicked = $(this);

    //Amount of elements in the queue

    //Flashes bright green briefly
    if((count != 0) && !$( "#btn-collect" ).hasClass( "btn-danger" )){ //Non empty list and not already clicked
      trialName = $('#trial-name').val();
      $('#btn-collect').toggleClass('btn-danger');
      $('#btn-collect').html("Stop &nbsp;<i class='fas fa-stop fa-sm text-white'></i>");

      // set up queue variable
      var queue = [];
      for (var i = 0; i < currentProtocol.length; i++) {
        if (currentProtocol[i][2] == "mu") {
          queue.push(currentProtocol[i]); // leave element as is
        }
        // unwrap SSVEP elements
        else if (currentProtocol[i][2] == "ssvep") {
          queue.push(["RestSSVEP", currentProtocol[i][1][0], "ssvep"]);
          queue.push(["Cue", currentProtocol[i][1][1], "ssvep"]);
          queue.push([currentProtocol[i][0] + "Hz", currentProtocol[i][1][2], "ssvep"]); // stimulus frequency and duration
        }
      }

      var count = queue.length;

      //Finally emits a collectQueue!
      //Gives the queue array with the direcions/durations and active sensors
      socket.emit("collectQueue", {queue: queue, sensors: active, trialName: trialName});

      let totalTime = 0;
      let times = [];
      let freq;
      /* Creates an array with cumulative times:
          Time 1: 5
          Time 2: 5
          Time 3: 10

          times = [5, 10, 20]
          */
      queue.forEach(function(command){
        if (command[2] == "mu") {
          totalTime+=command[1];
          times.push(totalTime);
        } if (command[2] === "ssvep") {
          totalTime += command[1];
          times.push(totalTime);
        }
      });

      direction = queue[0][0];
      //This is the direction of the first element
      let durationLeft = times[0] - 0;//Do we need - 0?
      console.log('start', durationLeft);
      console.log(times);

      // variable to save timestamps
      var timestamps_cues = [];

      let j = 0;
      let commandCounter = 0;
      let time = 1;

      // this function performs the next action in the queue
      const doNextCommand = function(first) {
        if (!first) {
          if (queue[commandCounter][2] === "mu") {
            $('#think-' + direction).removeClass('button-on');
            $('#think-' + direction).addClass('button-off');
            updateQueue();
          }
          if (queue[commandCounter][2] === "ssvep") {
            // check if last of current element in list
            if (queue[commandCounter][0].substr(-1) === "z") {
              updateQueue();
            }
          }
          commandCounter++;
        }
        direction = queue[commandCounter][0];
        console.log('next command');
        console.log('think-' + direction);
        // save first timestamp
        timestamps_cues.push({'time':getTimeValue(), 'cue':direction})
        if (queue[commandCounter][2] === "mu") {
          $('#think-' + direction).removeClass('button-off');
          $('#think-' + direction).addClass('button-on');
          $('#collectTime').html(durationLeft + ' s');
        } if (queue[commandCounter][2] === "ssvep") {
          startSSVEPSession(queue[commandCounter],
            commandCounter + 1 < queue.length ?
              parseInt(queue[commandCounter + 1][0]) : NaN);
        }
      }

      // startSSVEPSession(); // REMOVE; for debuging, must remove later!
      console.log('before collectionTime'); //REMOVE
      doNextCommand(true);

      //Controlling the timer.
      collectionTimer = setInterval(function(){
        console.log(times);
        console.log(commandCounter, time, durationLeft);
        if (time < totalTime) {
          if (time >= times[commandCounter]){
            doNextCommand(false);
          }
          // If we're not at end of duration, decrement time
          durationLeft = times[commandCounter] - time;

          $('#collectTime').html(durationLeft + ' s');
          time++;
        }
        else {
          timestamps_cues.push({'time':getTimeValue(), 'cue':'end'}) // save timestamp
          socket.emit('incomingTimestamps', timestamps_cues);
          $('#btn-collect').toggleClass('btn-danger');
          $('#btn-collect').html("Collect &nbsp; <i class='fas fa-play fa-sm text-white'></i>");
          $('#think-' + direction).removeClass('button-on');
          $('#think-' + direction).addClass('button-off');
          $('#collectTime').html("&nbsp;");
          clearInterval(collectionTimer);
          console.log('stop');

          updateQueue();
          socket.emit("protocol", {"action":"requestProtocol", "protocolName":"current"});

        }
      }, 1000);

    }
    else if($('#btn-collect').hasClass('btn-danger')){
      console.log("danger danger");
      clearInterval(collectionTimer);
      socket.emit("stop");
      $('#btn-collect').toggleClass('btn-danger');
      $('#btn-collect').html("Collect &nbsp; <i class='fas fa-play fa-sm text-white'></i>");
      $('#think-' + direction).removeClass('button-on');
      $('#think-' + direction).addClass('button-off');
      $('#collectTime').html("&nbsp");
    }
    else{
      console.log("Empty list nice try!");
    }
  });

  // display current protocol
  socket.on("protocol", function(options) {
    var action = options["action"];
    switch(action) {
      case "sendProtocol":
        protocol = options["protocol"];
        for (var i = 0; i < protocol.length; i++) {
          addElement(protocol[i], "#currentProtocol", false);
        }
        currentProtocol = protocol;
        break;
    }
  });
});

/*
 * Functions
 */

/* Gets the current time (copied from server.js) */
function getTimeValue() {
  var dateBuffer = new Date();
  var Time = dateBuffer.getTime();
  //Milliseconds since 1 January 1970
  return Time;
}

// Adds protocol element to list
function addElement(element, id, changeable) {
  // element must be of form [label, time, type]
  var type = element[2];

  if (type === "mu") {
    var direction = element[0];
    var duration = element[1];

    if (changeable) {
      $(id).append($("<div class='list-group-item tinted' data-direction=" + direction + " data-duration='" + duration + "'><i class='fas fa-arrows-alt handle'></i> " + direction + " " + duration + "s &nbsp; <a href='#' class='remove'><i class='fas fa-times-circle'></i></a></div>"));
    } else {
      $(id).append($("<div class='list-group-item tinted' data-direction=" + direction + " data-duration='" + duration + "'>" + direction + " " + duration + "s &nbsp; </div>"));
    }
  } else if (type == "ssvep") {
    var freq = element[0];
    var times = element[1];
    var duration = times[0] + "-" + times[1] + "-" + times[2];

    if (changeable) {
      $(id).append($("<div class='list-group-item tinted' data-freq=" + freq + " data-times='" + JSON.stringify(times) + "'><i class='fas fa-arrows-alt handle'></i> " + freq + "Hz " + duration + "s &nbsp; <a href='#' class='remove'><i class='fas fa-times-circle'></i></a></div>"));
    } else {
      $(id).append($("<div class='list-group-item tinted' data-freq=" + freq + " data-times='" + times + "'> " + freq + "Hz " + duration + "s &nbsp; </div>"));
    }
  } else {
    console.log("invalid type");
  }
}

// removes first element of queue without changing current protocol
function updateQueue() {
  $('#currentProtocol div')[0].remove();
}
