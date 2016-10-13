$("#guess").click(function() {
    console.log("clicked");
    var which;
    var player;
    for (var i=55;i>=15;i-=8) {
        var card = $(".ind"+i);
        if (card.hasClass("clicked_card")) { // TODO make sure only one
            which = (55-i)/8;
            player = 1;
        }
    }
    for (var i=8;i<=48;i+=8) {
        var card = $(".ind"+i);
        if (card.hasClass("clicked_card")) { // TODO make sure only one
            which = (i-8)/8;
            player = 3;
        }
    }
    var form = $("<form></form>");
    form.attr("method","post");
    form.attr("action","/game/"+$("#gamename").text());
    
    var field = $("<input></input>");
    field.attr("type","hidden");
    field.attr("name","card");
    field.attr("value",player.toString()+which);
    form.append(field);

    $(document.body).append(form);
    form.submit();
});
