$("#call").click(function() {
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
    for (var i=6;i>=1;i--) {
        var card = $(".ind"+i);
        if (card.hasClass("clicked_card")) { // TODO make sure only one
            which = 6-i;
            player = 2;
        }
    }
    for (var i=8;i<=48;i+=8) {
        var card = $(".ind"+i);
        if (card.hasClass("clicked_card")) { // TODO make sure only one
            which = (i-8)/8;
            player = 3;
        }
    }
    var value = $("#value").val();
    
    var form = $("<form></form>");
    form.attr("method","post");
    form.attr("action","{{ url_for(\"game\", name = "+$("#gamename").text()+") }}");
    
    var field = $("<input></input>");
    field.attr("type","hidden");
    field.attr("name","card");
    field.attr("value",player.toString()+which+value);
    form.append(field);

    $(document.body).append(form);
    form.submit();
});
