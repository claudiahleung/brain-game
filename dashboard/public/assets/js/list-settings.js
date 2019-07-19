$(document).ready(function() {
  console.log("List javascript loaded!");
  var list = document.getElementById('commandBank');
  var trialName;
  //SETS ACTIVE TO ALL OF THEM FOR NOW!
  var active = [1,1,1,1,1,1,1,1];
  //Made global so stop button can clear it
  var collectionTimer = null;
  var currentProtocol = [];

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
  });

  /*
   * Protocol Management
   */

   socket.on('currentProtocol', function(protocol) {
     currentProtocol = protocol;
     generateList(currentProtocol);
   })

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
 * Functions
 */

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
