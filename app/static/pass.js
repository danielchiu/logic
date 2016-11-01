$("#pass").click(function() {
    var ind = select();
    if (!ind || !south(ind)) {
        return;
    }

    var which = south(ind);

    var form = $("<form></form>");
    form.attr("method","post");
    
    var field = $("<input></input>");
    field.attr("type","hidden");
    field.attr("name","card");
    field.attr("value",which);
    form.append(field);

    form.append(getLogLen());

    $(document.body).append(form);
    form.submit();
});
