$(document).ready(function() {
  console.log("List javascript loaded!");
  var list = document.getElementById('commandBank');
  var trialName;
  //SETS ACTIVE TO ALL OF THEM FOR NOW!
  var active = [1,1,1,1,1,1,1,1];
  //Made global so stop button can clear it
  var collectionTimer = null;

  // load default elements in Custom Protocol


  //To remove an element from the queue
  $(".remove").on("click",function(){
    console.log("here?");
    event.preventDefault();
    $(this).parent().remove();
  });

  // add element to queue
  $(".add-mu").click(function() {
    var clicked = $(this);
    var duration = $("#timeMu").val();
    var direction = clicked.data("direction");

    $("#listMu").append($("<div class='list-group-item tinted' data-direction=" + direction + " data-duration='" + duration + "'><i class='fas fa-arrows-alt handle'></i> " + direction + " " + duration + "s &nbsp; <a href='#' class='remove'><i class='fas fa-times-circle'></i></a></div>"));
  })

  $(".add-ssvep").click(function() {
    var xlixked = $(this);
    var timeRest = int($("#timeRest").val());
    var timeCue = int($("#timeCue").val());
    var timeStim = int($("#timeStim").val());
    var times = [timeRest, timeCue, timeStim];
    var duration = times[0] + "-" + times[1] + "-" + times[2];
    var freq = int($(this).data("freq"));

    $("#listSSVEP").append($("<div class='list-group-item tinted' data-freq=" + freq + " data-times='" + JSON.stringify(times) + "'><i class='fas fa-arrows-alt handle'></i> " + freq + "Hz " + duration + "s &nbsp; <a href='#' class='remove'><i class='fas fa-times-circle'></i></a></div>"));
  })

  /*
   * Protocol Management
   */

   // update current protocol
   socket.on('currentProtocol', function(protocol) {
     generateList(protocol);
   })

   // load button (from 'Load Default Protocol')
   $(".load-default").click(function() {

     // first clear current protocol space
     clearList("#currentProtocol");

     // get protocol type
     var protocolName = $(this).attr("protocol-name");

     // send request to server
     socket.emit("requestDefaultProtocol", protocolName);
   })

  // loop button
  $(".loop-mu").click(function() {
    console.log("Loop mu")

    // get loop times and current elements in queue
    var times = $("#loopTimesMu").val();
    var currentList = $("#listMu div");

    for (var i = 0; i < times - 1; i++) {
      // add element to queue
      currentList.each(function() {
        $("#listMu").append($(this).clone());
      });
    }
  });

  // loop button
  $(".loop-ssvep").click(function() {
    console.log("Loop SSVEP")

    // get loop times and current elements in queue
    var times = $("#loopTimesSSVEP").val();
    var currentList = $("#listSSVEP div");

    for (var i = 0; i < times - 1; i++) {
      // add element to queue
      currentList.each(function() {
        $("#listSSVEP").append($(this).clone());
      });
    }
  });

  // load button (from Custom Protocol)
  $(".load-custom").click(function() {

    // first clear the current protocol space
    clearList('#currentProtocol');

    var protocol = [];

    // add mu cues
    $('#listMu').children('div').each(function () {
        var itemDuration = $(this).data("duration");
        var itemDirection = $(this).data("direction")
        protocol.push([itemDirection, itemDuration, "mu"]);
    });

    // add SSVEP cues
    $('#listSSVEP').children('div').each(function () {
        var itemFreq = $(this).data("freq")
        var itemTimes = $(this).data("times");
        protocol.push([itemFreq, itemTimes, "ssvep"]);
    });

    socket.emit('protocolChanged', protocol);
  })

  // clear mu button (from 'Customize Protocol')
  $(".clear-mu").click(function() {
    // clear custom protocol space
    clearList("#listMu");
  });

  // clear SSVEP button (from 'Customize Protocol')
  $(".clear-ssvep").click(function() {
    // clear custom protocol space
    clearList("#listSSVEP");
  });

});

/*
 * Functions
 */

// function that displays current protocol
function generateList(protocol) {
  for (var i = 0; i < protocol.length; i++) {
    var type = protocol[i][2];

    if (type == "mu") {
      var direction = protocol[i][0];
      var duration = protocol[i][1];

      // do not allow user to modify protocol
      $("#currentProtocol").append($("<div class='list-group-item tinted' data-direction=" + direction + " data-duration='" + duration + "'>" + direction + " " + duration + "s &nbsp; </div>"));
    }
    else if (type == "ssvep") {
      var freq = protocol[i][0];
      var times = protocol[i][1];
      var duration = times[0] + "-" + times[1] + "-" + times[2];

      // do not allow user to modify protocol
      $("#currentProtocol").append($("<div class='list-group-item tinted' data-freq=" + freq + " data-times='" + times + "'> " + freq + "Hz " + duration + "s &nbsp; </div>"));
    }
  }
}

// function that clears list (id should be either #currentProtocol or #commandList)
function clearList(id) {
  $(id + " div").each(function() {
    $(this).remove();
  });
}

function int(str) {
  return parseInt(str, 10);
}
