$(document).ready(function() {
    setInterval(function() {
        $("#content").load(location.href+" #reload_content");
    }, 5000);
});
