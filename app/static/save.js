$("#content").on("click", "#save", function() {
    var request = new XMLHttpRequest();
    request.open("POST", "?type=savenote&note="+$("#notes .box").val().replace(/\n/g,"%0A"));
    request.send();
});
