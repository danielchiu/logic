// defaults scrollbars to bottom
$(document).ready(function() {
    $("#logbox").scrollTop($("#logbox")[0].scrollHeight);
});

// autoreloads the game and log
$(document).ready(function() {
    setInterval(function() {
        $.get(location.href, function(data) {
            var curLen = $(".action").length;
            var newLen = $(data).find(".action").length;
            if (newLen>curLen) {
                $("#grid").html($(data).find("#reload_grid").html());
                $("#logbox").html($(data).find("#reload_logbox").html());
                $("#above").html($(data).find("#reload_above").html());
                $("#below").html($(data).find("#reload_below").html());
                $("#logbox").scrollTop($("#logbox")[0].scrollHeight);
            }
        });
    }, 5000);
});

// toggles between log and chat
$("#logbox").click(function() {
    $("#log").css("display", "none");
    $("#chat").css("display", "inline");
    $("#chatbox").scrollTop($("#chatbox")[0].scrollHeight);
    $("#chatline").focus();
});
$("#chatbox").click(function() {
    $("#chat").css("display", "none");
    $("#log").css("display", "inline");
    $("#logbox").scrollTop($("#logbox")[0].scrollHeight);
});

// autoreloads chat on an increasing time delay
// scrolls to bottom if scrollbar is close enough to bottom
function reloadchat(data) {
    var bottom = ($("#chatbox")[0].scrollHeight - $("#chatbox")[0].scrollTop <= $("#chatbox")[0].clientHeight + 50)
    $.get(location.href, function(data) {
        var curLen = $(".message").length;
        var newLen = $(data).find(".message").length;
        if (newLen>curLen) {
            $("#chatbox").html($(data).find("#reload_chatbox").html());
            if (bottom) $("#chatbox").scrollTop($("#chatbox")[0].scrollHeight);
            return true;
        }
        return false;
    });

    // change times to client local time
    // TODO with latency this also takes a little bit to update
    $(".message").each(function() {
        $(this).attr("title", (new Date(this.title)).toString());
    });
}

var countdown = 1;
var current = 1;
$(document).ready(function() {
    setInterval(function() {
        current-=1;
        if (current == 0) {
            if (reloadchat()) countdown = 1;
            else if (countdown<8) countdown+=1;
            current = countdown;
        }
    }, 500);
});

// handles the chat input with the enter key
$("#chatline").keypress(function(event) {
    if (event.keyCode == 13) {
        var request = new XMLHttpRequest();
        
        var now = new Date();

        request.open("POST", "?message="+$("#chatline").val()+"&time="+now.toUTCString());
        request.send();

        $("#chatline").val("");
        $("#chatbox").scrollTop($("#chatbox")[0].scrollHeight);
        reloadchat();
        countdown = 1;
    }
});

// clicks cards (only one at a time)
$("#content").on("click", ".card", function() {
    if ($(this).hasClass("clicked_card")) {
        $(this).removeClass("clicked_card");
    } else {
        for (var i=0;i<64;i++) {
            $(".ind"+i).removeClass("clicked_card");
        }
        $(this).addClass("clicked_card");
    }
});

/* helper functions */

// finds the index of a 64-based id in a hand
function south(num) {
    if (57<=num && num<=62) return num-56;
    return false;
}
function east(num) {
    if (num%8==7) return 7-(num-7)/8;
    return false;
}
function north(num) {
    if (1<=num && num<=6) return 7-num;
    return false;
}
function west(num) {
    if (num%8==0) return num/8;
    return false;
}

// uses jquery to find card elements
function getcard(ind) {
    return $(".ind"+ind);
}
function getind(card) {
    for (var i=0;i<64;i++) {
        if (card.hasClass("ind"+i)) return i;
    }
    return -1;
}

function select() {
    if ($(".clicked_card").size()!=1) return false;
    return getind($(".clicked_card"));
}

// finds the number of revealed cards (for corner case with all cards revealed)
function getSouth() {
    var res = 0;
    for (var i=0;i<64;i++) {
        if (south(i) && !getcard(i).hasClass("public")) res+=1;
    }
    return res;
}
function getEast() {
    var res = 0;
    for (var i=0;i<64;i++) {
        if (east(i) && !getcard(i).hasClass("public")) res+=1;
    }
    return res;
}
function getNorth() {
    var res = 0;
    for (var i=0;i<64;i++) {
        if (north(i) && !getcard(i).hasClass("public")) res+=1;
    }
    return res;
}
function getWest() {
    var res = 0;
    for (var i=0;i<64;i++) {
        if (west(i) && !getcard(i).hasClass("public")) res+=1;
    }
    return res;
}

function makeField(from, to) {
    var field = $("<input></input>");
    field.attr("type","hidden");
    field.attr("name",from.toString());
    field.attr("value",to.toString());
    return field;
}

function getLogLen() {
    return makeField("loglen",$(".action").length);
}

// makes sure an input is a valid possible card
function validate(num) {
    if (num=='A' || num=='T' || num=='J' || num=='Q') return true;
    if ("2"<=num && num<="9") return true;
    return false;
}
