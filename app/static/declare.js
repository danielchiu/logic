$("#content").on("click", "#declare", function() {
    if (!confirm("Are you sure you want to declare?")) {
        return;
    }
    var form = $("<form></form>");
    form.attr("method","post");
    form.append(makeField("type","declare"));

    form.append(getLogLen());

    $(document.body).append(form);
    form.submit();
});
