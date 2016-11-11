var swapped = "";

$(".card").click(function() {
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

function makeField(from, to) {
    var field = $("<input></input>");
    field.attr("type","hidden");
    field.attr("name",from.toString());
    field.attr("value",to.toString());
    return field;
}

function getLogLen() {
    return makeField("loglen",$("#log").children().length-1);
}

$("#order").click(function() {
    var form = $("<form></form>");
    form.attr("method","post");
    form.append(makeField("type","order"));
    
    form.append(makeField("swapped",swapped));

    form.append(getLogLen());

    $(document.body).append(form);
    form.submit();
});
