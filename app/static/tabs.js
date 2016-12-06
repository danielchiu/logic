$(document).ready(function() {
    openTab(getClass($(".tab").first(),2));
    $(".tab").click(function() {
        openTab(getClass($(this),2));
    });
});

function openTab(tab) {
    $(".tabcontent").css("display", "none");
    $("#"+tab).css("display", "block");
    $(".tab").removeClass("active");
    $("#"+tab).addClass("active");
    $(".active .focus").focus();
    $(".active .box").scrollTop($(".active .box")[0].scrollHeight);
}
