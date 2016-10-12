$("#pass").click(function() {
    console.log("clicked");
    var which;
    for (var i=57;i<=62;i++) {
        var card = $(".ind"+i.toString());
        if (card.hasClass("clicked_card")) {
            which = i-57;
            console.log("card "+(i-57).toString());
        }
    }
    var form = $("<form></form>");
    form.attr("method","post");
    form.attr("action","/game/"+$("#gamename").text());
    
    var field = $("<input></input>");
    field.attr("type","hidden");
    field.attr("name","card");
    field.attr("value",which);
    form.append(field);

    $(document.body).append(form);
    form.submit();
});
