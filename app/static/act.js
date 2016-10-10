$("#act").click(function() {
    console.log("clicked");
    for (var i=57;i<=62;i++) {
        var card = $(".ind"+i.toString());
        if (card.hasClass("clicked_card")) {
            console.log("card "+(i-57).toString());
        }
    }
});
