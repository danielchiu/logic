$("#declare").click(function() {
    console.log("clicked");
    var form = $("<form></form>");
    form.attr("method","post");
    form.attr("action","{{ url_for(\"game\", name = "+$("#gamename").text()+") }}");
    
    var field = $("<input></input>");
    field.attr("type","hidden");
    field.attr("name","card");
    field.attr("value","declare");
    form.append(field);

    $(document.body).append(form);
    form.submit();
});
