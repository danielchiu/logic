// defaults scrollbars to bottom
$(document).ready(function() {
    $("#log .box").scrollTop($("#log .box")[0].scrollHeight);
});

// change times to client local time
var lastdate = "";
var lasttime = "";
function fixTimes(section) {
    lastdate = "";
    $(section+" .datestamp").each(function() {
        var when = new Date($(this).text());
        if (getDate(when)==lastdate) {
            $(this).remove();
        } else {
            $(this).text(getDate(when));
        }
        lastdate = getDate(when);
    });
    lastdate = "";
    lasttime = "";
    $(section+" .timestamp").each(function() {
        var when = new Date($(this).text());
        if (getTime(when)==lasttime && getDate(when)==lastdate) {
            $(this).remove();
        } else {
            $(this).text(getTime(when));
        }
        lastdate = getDate(when);
        lasttime = getTime(when);
    });
}
$(document).ready(function() {
    fixTimes("#log");
    fixTimes("#chat");
});

// autoreloads the game and log
$(document).ready(function() {
    setInterval(function() {
        $.get(location.href, function(data) {
            var curLen = $(".action").length;
            var newLen = $(data).find(".action").length;
            if (newLen>curLen) {
                $("#grid").html($(data).find("#reload_grid").html());
                $("#log .box").html($(data).find("#log .reload_box").html());
                $("#above").html($(data).find("#reload_above").html());
                $("#below").html($(data).find("#reload_below").html());
                $("#log .box").scrollTop($("#log .box")[0].scrollHeight);
                fixTimes("#log");
            }
        });
    }, 5000);
});

// autoreloads chat on an increasing time delay
// scrolls to bottom if scrollbar is close enough to bottom
function reloadchat(data) {
    var bottom = ($("#chat .box")[0].scrollHeight - $("#chat .box")[0].scrollTop <= $("#chat .box")[0].clientHeight + 50)
    $.get(location.href, function(data) {
        var curLen = $(".message").length;
        var newLen = $(data).find(".message").length;
        if (newLen>curLen) {
            $("#chat .box").html($(data).find("#chat .reload_box").html());
            if (bottom) $("#chat .box").scrollTop($("#chat .box")[0].scrollHeight);
            fixTimes("#chat");
            return true;
        }
        return false;
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

        request.open("POST", "?type=chat&message="+$("#chatline").val()+"&time="+now.toUTCString());
        request.send();
        
        if (getDate(now)!=lastdate) {
            var fakedate = "<div class=\"datestamp\">";
            fakedate+=getDate(now);
            fakedate+="</div>";
            $("#chat .box").append(fakedate);
        }
        var fakemessage = "<div class=\"fakemessage\">";
        fakemessage+="<div class=\"textstamp\">"+$("#username").text()+": "+$("#chatline").val()+"</div>"
        if (getDate(now)!=lastdate || getTime(now)!=lasttime) {
            var faketime ="<div class=\"timestamp\">";
            faketime+=getTime(now);
            faketime+="</div>";
            fakemessage+=faketime;
        }
        lastdate = getDate(now);
        lasttime = getTime(now);
        fakemessage+="</div>";
        $("#chat .box").append(fakemessage);

        $("#chatline").val("");
        $("#chat .box").scrollTop($("#chat .box")[0].scrollHeight);
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
