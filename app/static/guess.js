$("#guess").click(function() {
    var ind = select();
    if (!ind || south(ind) || north(ind)) {
        return;
    }
    if ((getEast() || getWest()) && getcard(ind).hasClass("public")) {
        return;
    }

    var which, player;
    if (east(ind)) {
        which = east(ind);
        player = 1;
    }
    if (west(ind)) {
        which = west(ind);
        player = 3;
    }

    var value = $("#value").val();
    
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
