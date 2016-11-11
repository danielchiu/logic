$("#pass").click(function() {
    var ind = select();
    if (!ind || !south(ind)) {
        return;
    }

    var which = south(ind);

    var form = $("<form></form>");
    form.attr("method","post");
    form.append(makeField("type","pass"));
    
    form.append(makeField("index",which));

    form.append(getLogLen());

    $(document.body).append(form);
    form.submit();
});
