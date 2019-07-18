$(document).ready(function() {
  console.log("List javascript loaded!");
  var list = document.getElementById('commandBank');
  var trialName;
  //SETS ACTIVE TO ALL OF THEM FOR NOW!
  var active = [1,1,1,1,1,1,1,1];
  //Made global so stop button can clear it
  var collectionTimer = null;
  var currentProtocol;

  //To remove an element from the queue
  $("#commandList").on("click",".remove",function(){
    console.log("here?");
    event.preventDefault();
    $(this).parent().remove();
  });

  //On left, right, or rest button click!
  $(".selection").click(function() {
    var clicked = $(this);
    var duration = $(".timer").val();

    if(clicked.is('.direction-left')){
      //Make list item with left and duration!
      $("#commandList").append($("<div class='list-group-item tinted' data-direction='Left' data-duration='" + duration + "'><i class='fas fa-arrows-alt handle'></i> Left " + duration + "s &nbsp; <a href='#' class='remove'><i class='fas fa-times-circle'></i></a></div>"));
    }
    else if(clicked.is('.direction-right')){
      $("#commandList").append($("<div class='list-group-item tinted' data-direction='Right' data-duration='" + duration + "'><i class='fas fa-arrows-alt handle'></i> Right " + duration + "s &nbsp; <a href='#' class='remove'><i class='fas fa-times-circle'></i></a></div>"));
    }
    else if(clicked.is('.direction-rest')){
      $("#commandList").append($("<div class='list-group-item tinted' data-direction='Rest' data-duration='" + duration + "'><i class='fas fa-arrows-alt handle'></i> Rest " + duration + "s &nbsp; <a href='#' class='remove'><i class='fas fa-times-circle'></i></a></div>"));
    }
    else if (clicked.is('.freq-10')) {
      $("#commandList").append($("<div class='list-group-item tinted' data-direction='10Hz' data-duration='" + duration + "'><i class='fas fa-arrows-alt handle'></i> 10 Hz " + duration + "s &nbsp; <a href='#' class='remove'><i class='fas fa-times-circle'></i></a></div>"));
    }
    else if (clicked.is('.freq-12')) {
      $("#commandList").append($("<div class='list-group-item tinted' data-direction='12Hz' data-duration='" + duration + "'><i class='fas fa-arrows-alt handle'></i> 12 Hz " + duration + "s &nbsp; <a href='#' class='remove'><i class='fas fa-times-circle'></i></a></div>"));
    }
    else if (clicked.is('.freq-15')) {
      $("#commandList").append($("<div class='list-group-item tinted' data-direction='15Hz' data-duration='" + duration + "'><i class='fas fa-arrows-alt handle'></i> 15 Hz " + duration + "s &nbsp; <a href='#' class='remove'><i class='fas fa-times-circle'></i></a></div>"));
    }
    else{

      //Amount of elements in the queue

      //Flashes bright green briefly
      if((count != 0) && !$( "#btn-collect" ).hasClass( "btn-danger" )){ //Non empty list and not already clicked
          trialName = $('#trial-name').val();
          $('#btn-collect').toggleClass('btn-danger');
          $('#btn-collect').html("Stop &nbsp;<i class='fas fa-stop fa-sm text-white'></i>");


          var queue = currentProtocol;
          var count = queue.length;

          /* removing this because queue was moved to Settings page
          var queue = [];
          var count = $("#commandList div").length;
          //For each element in the queue, push their direction and duration
          $('#commandList').children('div').each(function () {
              var itemDuration = $(this).data("duration");
              var itemDirection = $(this).data("direction")
              queue.push([itemDirection, itemDuration]);

            });
          */

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

        // code to save timestamps
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

    }

  });

  // loop button
  $(".loop-btn").click(function() {
    console.log("Loop button clicked")

    // get loop times and current elements in queue
    var times = $("#loopTimes").val();
    var currentList = $("#commandList div");

    for (var i = 0; i < times - 1; i++) {
      for (var j = 0; j < currentList.length; j++) {

        // add elements to queue
        var direction = currentList[j].getAttribute("data-direction");
        var duration = currentList[j].getAttribute("data-duration");
        $("#commandList").append($("<div class='list-group-item tinted' data-direction=" + direction + " data-duration='" + duration + "'><i class='fas fa-arrows-alt handle'></i> " + direction + " " + duration + "s &nbsp; <a href='#' class='remove'><i class='fas fa-times-circle'></i></a></div>"));
      }
    }
  });

  // load button (from Custom Protocol)
  $(".load-custom").click(function() {

    // first clear the current protocol space
    clearList('#currentProtocol');

    var protocol = [];
    $('#commandList').children('div').each(function () {
        var itemDuration = $(this).data("duration");
        var itemDirection = $(this).data("direction")
        protocol.push([itemDirection, itemDuration]);
    });

    socket.emit('protocolChanged', protocol);
  })

  // clear button (from 'Customize Protocol')
  $(".clear-btn").click(function() {
    // clear custom protocol space
    clearList("#commandList");
  });

  // load button (from 'Load Default Protocol')
  $(".load-default").click(function() {

    // first clear current protocol space
    clearList("#currentProtocol");

    // get protocol type
    var protocolName = $(this).attr("protocol-name");

    // send request to server
    socket.emit("requestDefaultProtocol", protocolName);
  })

  // send current protocol to server whenever user refreshes/changes page
  $(window).on("beforeunload", function() {
    var protocol = [];

    $('#currentProtocol').children('div').each(function () {
        var itemDuration = $(this).data("duration");
        var itemDirection = $(this).data("direction")
        protocol.push([itemDirection, itemDuration]);
    });

    socket.emit('protocolChanged', protocol);
  });

});

/*
 * functions
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

// function that clears list (id should be either #currentProtocol or #commandList)
function clearList(id) {
  $(id + " div").each(function() {
    $(this).remove();
  });
}
