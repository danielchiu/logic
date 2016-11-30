$("#content").on("click", ".card", function() {
    $(this).toggleClass("clicked_card");
});

// autoreloads the game and log
$(document).ready(function() {
    setInterval(function() {
        $.get(location.href, function(data) {
            var curLen = $("#logtitle ~ div").length;
            var newLen = $(data).find("#logtitle ~ div").length;
            if (newLen>curLen) {
                $("#grid").html($(data).find("#reload_grid").html());
                $("#log").html($(data).find("#reload_log").html());
                $("#above").html($(data).find("#reload_above").html());
                $("#below").html($(data).find("#reload_below").html());
            }
        });
    }, 5000);
});

// toggles between log and chat
$("#log").click(function() {
    $("#log").css("display", "none");
    $("#chat").css("display", "inline");
});
$("#chatbox").click(function() {
    $("#chat").css("display", "none");
    $("#log").css("display", "inline");
});

// autoreloads chat on an increasing time delay
var countdown = 8;
var current = 8;
$(document).ready(function() {
    setInterval(function() {
        current-=1;
        if (current == 0) {
            $.get(location.href, function(data) {
                var curLen = $("#chattitle ~ div").length;
                var newLen = $(data).find("#chattitle ~ div").length;
                if (newLen>curLen) {
                    $("#chatbox").html($(data).find("#reload_chatbox").html());
                    countdown = 1;
                } else if (countdown<8) {
                    countdown*=2;
                }
            });
            current = countdown;
        }
    }, 500);
});

// handles the chat input with the enter key
$("#chatline").keypress(function(event) {
    if (event.keyCode == 13) {
        var request = new XMLHttpRequest();
        
        request.open("POST", "?message="+$("#chatline").val());
        request.send();

        $("#chatline").val("");
        $.get(location.href, function(data) {
            $("#chatbox").html($(data).find("#reload_chatbox").html());
        });
        countdown = 1;
    }
});

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
    return makeField("loglen",$("#logtitle ~ div").length);
}

// makes sure an input is a valid possible card
function validate(num) {
    if (num=='A' || num=='T' || num=='J' || num=='Q') return true;
    if ("2"<=num && num<="9") return true;
    return false;
}
