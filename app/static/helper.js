// get time/date out of a Date object
function getTime(date) {
    var min = "";
    var hr = "12";
    var mr = "am";
    if (date.getHours()>11) mr = "pm";
    if (date.getHours()%12!=0) hr = date.getHours()%12;
    if (date.getMinutes()<10) min = "0";
    return hr+":"+min+date.getMinutes()+mr;
}
function getDate(date) {
    return (date.getMonth()+1)+"/"+date.getDate();
}

// finds the index of a 64-based id in a hand
function south(num) {
    if (57<=num && num<=62) return num-56;
    return false;
}
function east(num) {
    if (num%8==7) return 7-(num-7)/8;
    return false;
}
function north(num) {
    if (1<=num && num<=6) return 7-num;
    return false;
}
function west(num) {
    if (num%8==0) return num/8;
    return false;
}

// uses jquery to find card elements
function getcard(ind) {
    return $(".ind"+ind);
}
function getind(card) {
    for (var i=0;i<64;i++) {
        if (card.hasClass("ind"+i)) return i;
    }
    return -1;
}

function select() {
    if ($(".clicked_card").size()!=1) return false;
    return getind($(".clicked_card"));
}

// finds the number of revealed cards (for corner case with all cards revealed)
function getSouth() {
    var res = 0;
    for (var i=0;i<64;i++) {
        if (south(i) && !getcard(i).hasClass("public")) res+=1;
    }
    return res;
}
function getEast() {
    var res = 0;
    for (var i=0;i<64;i++) {
        if (east(i) && !getcard(i).hasClass("public")) res+=1;
    }
    return res;
}
function getNorth() {
    var res = 0;
    for (var i=0;i<64;i++) {
        if (north(i) && !getcard(i).hasClass("public")) res+=1;
    }
    return res;
}
function getWest() {
    var res = 0;
    for (var i=0;i<64;i++) {
        if (west(i) && !getcard(i).hasClass("public")) res+=1;
    }
    return res;
}

function makeField(from, to) {
    var field = $("<input></input>");
    field.attr("type","hidden");
    field.attr("name",from.toString());
    field.attr("value",to.toString());
    return field;
}

function getLogLen() {
    return makeField("loglen",$(".action").length);
}

// makes sure an input is a valid possible card
function validate(num) {
    if (num=='A' || num=='T' || num=='J' || num=='Q') return true;
    if ("2"<=num && num<="9") return true;
    return false;
}

// return kth class of an element
function getClass(element, k) {
    return element.attr("class").split(" ")[k-1];
}
