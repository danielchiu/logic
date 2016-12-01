// handles reordering cards by clicking on an equal
var swapped = "";

$("#content").on("click", ".ocard", function() {
    if ($(this).hasClass("unknown")) return;
    var card;
    for (var i=57;i<=62;i++) {
        if ($(this).hasClass("ind"+i)) card = i;
    }
    if (card>57 && $(this).text()==$(".ind"+(card-1)).text()) {
        var other = $(".ind"+(card-1));
        $(this).insertBefore($(".ind"+(card-1)));
        $(this).addClass("ind"+(card-1));
        $(this).removeClass("ind"+card);
        other.addClass("ind"+card);
        other.removeClass("ind"+(card-1));
        swapped+=$(this).text().trim();
    }
    if (card<62 && $(this).text()==$(".ind"+(card+1)).text()) {
        var other = $(".ind"+(card+1));
        $(this).insertAfter($(".ind"+(card+1)));
        $(this).addClass("ind"+(card+1));
        $(this).removeClass("ind"+card);
        other.addClass("ind"+card);
        other.removeClass("ind"+(card+1));
        swapped+=$(this).text().trim();
    }
});

$("#content").on("click", "#order", function() {
    var form = $("<form></form>");
    form.attr("method","post");
    form.append(makeField("type","order"));
    form.append(makeField("time",(new Date()).toString()));
    
    form.append(makeField("swapped",swapped));

    form.append(getLogLen());

    $(document.body).append(form);
    form.submit();
});
