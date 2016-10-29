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

$("#order").click(function() {
    var form = $("<form></form>");
    form.attr("method","post");
    
    var field = $("<input></input>");
    field.attr("type","hidden");
    field.attr("name","swapped");
    field.attr("value",swapped);
    form.append(field);

    $(document.body).append(form);
    form.submit();
});
