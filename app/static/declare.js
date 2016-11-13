$("#content").on("click", "#declare", function() {
    var form = $("<form></form>");
    form.attr("method","post");
    form.append(makeField("type","declare"));

    form.append(getLogLen());

    $(document.body).append(form);
    form.submit();
});
