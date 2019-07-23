$(document).ready(function() {
  console.log("List javascript loaded!");
  var trialName;
  //SETS ACTIVE TO ALL OF THEM FOR NOW!
  var active = [1,1,1,1,1,1,1,1];
  //Made global so stop button can clear it
  var collectionTimer = null;
  var currentProtocol = [];

  //On left, right, or rest button click!
  $(".selection").click(function() {
    var clicked = $(this);

    //Amount of elements in the queue

    //Flashes bright green briefly
    if((count != 0) && !$( "#btn-collect" ).hasClass( "btn-danger" )){ //Non empty list and not already clicked
      trialName = $('#trial-name').val();
      $('#btn-collect').toggleClass('btn-danger');
      $('#btn-collect').html("Stop &nbsp;<i class='fas fa-stop fa-sm text-white'></i>");

      var queue = currentProtocol;
      var count = queue.length;

      //Finally emits a collectQueue!
      //Gives the queue array with the direcions/durations and active sensors
      socket.emit("collectQueue", {queue: queue, sensors: active, trialName: trialName});

      let totalTime = 0;
      let times = [];
      /* Creates an array with cumulative times:
          Time 1: 5
          Time 2: 5
          Time 3: 10

          times = [5, 10, 20]
      */
      queue.forEach(function(command){
        totalTime+=command[1];
        times.push(totalTime);
      });


      direction = queue[0][0];
      //This is the direction of the first element
      let durationLeft = times[0] - 0;//Do we need - 0?

      // variable to save timestamps
      var timestamps_cues = [];

      //Sets display to first elements command/time
      console.log('think-' + direction)
      timestamps_cues.push({'time':getTimeValue(), 'cue':direction}) // save first timestamp
      $('#think-' + direction).removeClass('button-off');
      $('#think-' + direction).addClass('button-on');
      $('#collectTime').html(durationLeft + ' s');
      let j = 0;
      let time = 1;

      //Controlling the timer.
      collectionTimer = setInterval(function(){
          if (time < totalTime) {
            if (time >= times[j]){
              //This means we've gotten to the end of element j's duration
              console.log("next command");
              j += 1;
              $('#think-' + direction).removeClass('button-on');
              $('#think-' + direction).addClass('button-off');
              direction = queue[j][0];
              timestamps_cues.push({'time':getTimeValue(), 'cue':direction}) // save timestamp
              $('#think-' + direction).removeClass('button-off');
              $('#think-' + direction).addClass('button-on'); //Setup direction again
              updateQueue();
            }
            //If we're not at end of duration, decrement time
            durationLeft = times[j] - time;

            $('#collectTime').html(durationLeft + ' s');
            time++;
          }
          else {
              timestamps_cues.push({'time':getTimeValue(), 'cue':'end'}) // save timestamp
              socket.emit('incomingTimestamps', timestamps_cues)
              $('#btn-collect').toggleClass('btn-danger');
              $('#btn-collect').html("Collect &nbsp; <i class='fas fa-play fa-sm text-white'></i>");
              $('#think-' + direction).removeClass('button-on');
              $('#think-' + direction).addClass('button-off');
              $('#collectTime').html("&nbsp;");
              clearInterval(collectionTimer);
              updateQueue();
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
   socket.on('currentProtocol', function(protocol) {
     currentProtocol = protocol;
     generateList(currentProtocol);
   })

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

// function that displays current protocol
function generateList(protocol) {
  for (var i = 0; i < protocol.length; i++) {
    var direction = protocol[i][0];
    var duration = protocol[i][1];

    // do not allow user to modify protocol
    $("#currentProtocol").append($("<div class='list-group-item tinted' data-direction=" + direction + " data-duration='" + duration + "'>" + direction + " " + duration + "s &nbsp; </div>"));
  }
}

// removes first element of queue without changing current protocol
function updateQueue() {
  $('#currentProtocol div')[0].remove();
}
