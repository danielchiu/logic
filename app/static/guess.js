$("#content").on("click", "#guess", function() {
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
    if (!validate(value)) return;
    
    var form = $("<form></form>");
    form.attr("method","post");
    form.append(makeField("type","guess"));
    form.append(makeField("time",(new Date()).toString()));
    
    form.append(makeField("player",player));
    form.append(makeField("index",which));
    form.append(makeField("value",value));

    form.append(getLogLen());

    $(document.body).append(form);
    form.submit();
});
