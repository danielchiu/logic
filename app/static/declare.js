$("#declare").click(function() {
    var form = $("<form></form>");
    form.attr("method","post");
    
    var field = $("<input></input>");
    field.attr("type","hidden");
    field.attr("name","card");
    field.attr("value","declare");
    form.append(field);

    form.append(getLogLen());

    $(document.body).append(form);
    form.submit();
});
