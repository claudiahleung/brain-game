$(document).ready(function() {
  console.log("List javascript loaded!");
  var trialName;
  //SETS ACTIVE TO ALL OF THEM FOR NOW!
  var active = [1,1,1,1,1,1,1,1];
  //Made global so stop button can clear it
  var collectionTimer = null;

  initializeCustomProtocol();

  socket.on("protocol", function(options) {
    var action = options["action"];
    switch(action) {
      case "sendProtocol":
        // display new protocol
        protocol = options["protocol"];
        for (var i = 0; i < protocol.length; i++) {
          addElement(protocol[i], "#currentProtocol", false);
        }
        break;
      case "sendShuffleValues":
        shuffle = options["shuffle"];
        $("#shuffleDefaultSSVEP").prop("checked", shuffle["default"]);
        $("#shuffleCustomSSVEP").prop("checked", shuffle["custom"]);
        break;
    }
  });

  // checkbox for default protocols
  $('#shuffleDefaultSSVEP').change(function() {
    socket.emit("protocol", {"action":"updateShuffleValue", "type":"default", "value":this.checked});
  });

  // checkbox for custom protocol
  $('#shuffleCustomSSVEP').change(function() {
    socket.emit("protocol", {"action":"updateShuffleValue", "type":"custom", "value":this.checked});
  });

  // load button (from 'Load Default Protocol')
  $(".load-default").click(function() {

    // first clear current protocol space
    clearList("#currentProtocol");

    // get protocol name
    var protocolName = $(this).attr("protocol-name");

    // send request to server
    socket.emit("protocol", {"action":"requestProtocol", "protocolName":protocolName});
  })

  // add element to custom mu protocol
  $(".add-mu").click(function() {
    var duration = $("#timeMu").val();
    var direction = $(this).data("direction");

    addElement([direction, duration, "mu"], "#listMu", true);
  })

  // add element to custom SSVEP protocol
  $(".add-ssvep").click(function() {
    var timeRest = int($("#timeRest").val());
    var timeCue = int($("#timeCue").val());
    var timeStim = int($("#timeStim").val());
    var freq = int($(this).data("freq"));

    addElement([freq, [timeRest, timeCue, timeStim], "ssvep"], "#listSSVEP", true);
  })

  // remove an element from custom mu/SSVEP protocol
  $(".command-list").on("click", ".remove", function(){
    console.log("here?");
    event.preventDefault();
    $(this).parent().remove();
  });

  // loop button for custom mu protocol
  $(".loop-mu").click(function() {
    console.log("Loop mu");

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

  // loop button for custom SSVEP protocol
  $(".loop-ssvep").click(function() {
    console.log("Loop SSVEP");

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

    // clear the current protocol space
    clearList('#currentProtocol');

    var protocol = [];

    // add mu cues
    $('#listMu').children('div').each(function () {
        var itemDuration = $(this).data("duration");
        var itemDirection = $(this).data("direction")
        var element = [itemDirection, itemDuration, "mu"];

        protocol.push(element);
    });

    // add SSVEP cues
    $('#listSSVEP').children('div').each(function () {
        var itemFreq = $(this).data("freq");
        var itemTimes = $(this).data("times");
        var element = [itemFreq, itemTimes, "ssvep"];

        protocol.push(element);
    });

    socket.emit("protocol", {"action":"changeProtocol", "protocol":protocol});
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

// loads default elements in Custom Protocol and sets default settings in Create Custom Protocol
function initializeCustomProtocol() {
  // load default elements in Custom Protocol
  var directionsMu = ['Rest', 'Left', 'Right'];
  var durationMu = 20;
  var frequenciesSSVEP = [10, 12, 15];
  var timesSSVEP = [1,2,5];

  // mu elements
  for (var i = 0; i < directionsMu.length; i++) {
    addElement([directionsMu[i], durationMu, "mu"], "#listMu", true);
  }
  // SSVEP elements
  for (var i = 0; i < directionsMu.length; i++) {
    addElement([frequenciesSSVEP[i], timesSSVEP, "ssvep"], "#listSSVEP", true);
  }

  // set default settings in Create Custom Protocol
  $("#timeMu").val(durationMu);
  $("#loopTimesMu").val(3);
  $("#timeRest").val(timesSSVEP[0]);
  $("#timeCue").val(timesSSVEP[1]);
  $("#timeStim").val(timesSSVEP[2]);
  $("#loopTimesSSVEP").val(5);
}

// adds protocol element to list
function addElement(element, id, changeable) {
  // element must be of form [label, time, type]
  var type = element[2];

  if (type == "mu") {
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
      $(id).append($("<div class='list-group-item tinted' data-freq=" + freq + " data-times='" + JSON.stringify(times) + "'> " + freq + "Hz " + duration + "s &nbsp; </div>"));
    }
  } else {
    console.log("invalid type");
  }
}

// clears list (id should be either #currentProtocol or #listMu or #listSSVEP)
function clearList(id) {
  $(id + " div").each(function() {
    $(this).remove();
  });
}

// casts string to int in base 10
function int(str) {
  return parseInt(str, 10);
}
