$("#reveal").click(function() {
    var which;
    for (var i=57;i<=62;i++) {
        var card = $(".ind"+i);
        if (card.hasClass("clicked_card")) { // TODO make sure only one
            which = i-57;
            console.log("card "+(i-57));
        }
    }
    var form = $("<form></form>");
    form.attr("method","post");
    
    var field = $("<input></input>");
    field.attr("type","hidden");
    field.attr("name","card");
    field.attr("value",which);
    form.append(field);

    $(document.body).append(form);
    form.submit();
});
