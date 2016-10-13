$("#declare").click(function() {
    console.log("clicked");
    var form = $("<form></form>");
    form.attr("method","post");
    form.attr("action","/game/"+$("#gamename").text());
    
    var field = $("<input></input>");
    field.attr("type","hidden");
    field.attr("name","declare");
    field.attr("value",true);
    form.append(field);

    $(document.body).append(form);
    form.submit();
});
