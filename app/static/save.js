$("#content").on("click", "#save", function() {
    var request = new XMLHttpRequest();
    request.open("POST", "?type=savenote&note="+$("#notes .box").val());
    request.send();
});
