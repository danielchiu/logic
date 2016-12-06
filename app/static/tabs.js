$(document).ready(function() {
    openTab($(".tab").first());
    $(".tab").click(function() {
        openTab($(this));
    });
});

function openTab(tab) {
    var name = getClass(tab,2);
    
    $(".tab").removeClass("active");
    tab.addClass("active");

    $(".tabcontent").css("display", "none");
    $("#"+name).css("display", "block");
    $(".tabcontent").removeClass("active");
    $("#"+name).addClass("active");
    $(".tabcontent.active .focus").focus();
    if ($(".tabcontent.active .box").length>0) {
        $(".active .box").scrollTop($(".active .box")[0].scrollHeight);
    }
}
