$("#call").click(function() {
    var ind = select();
    if (!ind || south(ind) || getcard(ind).hasClass("public")) {
        return;
    }

    var which, player;
    if (east(ind)) {
        which = east(ind);
        player = 1;
    }
    if (north(ind)) {
        which = north(ind);
        player = 2;
    }
    if (west(ind)) {
        which = west(ind);
        player = 3;
    }

    var value = $("#value").val();
    if (!validate(value)) return;
    
    var form = $("<form></form>");
    form.attr("method","post");
    
    var field = $("<input></input>");
    field.attr("type","hidden");
    field.attr("name","card");
    field.attr("value",player.toString()+which+value);
    form.append(field);

    form.append(getLogLen());

    $(document.body).append(form);
    form.submit();
});
