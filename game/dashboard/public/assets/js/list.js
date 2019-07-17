$(document).ready(function() {
  console.log("List javascript loaded!");
  var list = document.getElementById('commandBank');
  var trialName;
  //SETS ACTIVE TO ALL OF THEM FOR NOW!
  var active = [1,1,1,1,1,1,1,1];
  //Made global so stop button can clear it
  var collectionTimer = null;
  //var loop = false;

  /** removing previous loop code
  $('#customControlValidation1').change(function() {
      if(this.checked) {
          $(this).prop('checked', true);
          loop = true;
      }
      else{
          $(this).prop('checked', false);
          loop = false;
      }
  });
  */

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
    else{

      // var loop = $("#loop").prop("checked") //returns true or false!
      //if 'else', must be collect!

      //Amount of elements in the queue

      //Flashes bright green briefly
      if((count != 0) && !$( "#btn-collect" ).hasClass( "btn-danger" )){ //Non empty list and not already clicked
          var queue = [];
          var count = $("#commandList div").length;
          trialName = $('#trial-name').val();
          $('#btn-collect').toggleClass('btn-danger');
          $('#btn-collect').html("Stop &nbsp;<i class='fas fa-stop fa-sm text-white'></i>");
          //For each element in the queue, push their direction and duration
          $('#commandList').children('div').each(function () {
              var itemDuration = $(this).data("duration");
              var itemDirection = $(this).data("direction")
              queue.push([itemDirection, itemDuration]);
        });

        // if(loop){
        //   queue.push(["loop", 0]);
        // }

        //Finally emits a collectQueue!

        //Gives the queue array with the direcions/durations and active sensors
        socket.emit("collectQueue", {queue: queue, sensors: active, trialName: trialName});//, loop: loop});

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

  // loop button implementation
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

  /* copied from server.js */
  /* Gets the current time */
  function getTimeValue() {
    var dateBuffer = new Date();
    var Time = dateBuffer.getTime();
    //Milliseconds since 1 January 1970
    return Time;
  }

});
