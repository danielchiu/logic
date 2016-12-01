$(document).ready(function() {
    openTab("Overview");
    $(".tab").click(function() {
        openTab($(this).text());
    });
});

function openTab(tab) {
    $(".tabcontent").css("display", "none");
    $("#"+tab).css("display", "block");
    $(".tab").removeClass("active");
    $(".tab:contains("+tab+")").addClass("active");
}
