// autoreloads the gamelist
$(document).ready(function() {
    setInterval(function() {
        $("#gamelist").load(location.href+" #reload_gamelist");
    }, 5000);
});
