
function logout() {
     delete_cookie("username");
    window.location.href = '/home/';

}

  function setCookie(cname, cvalue, exdays) {
        //alert("setting" + cvalue);
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

var delete_cookie = function(name) {
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

function checkCookie() {
  //delete_cookie("username");
    var username = getCookie("username");
    if (username != "") {
        //alert("Welcome " + username);
    } else {
        // username = prompt("Please enter your name:", "");
        // if (username != "" && username != null) {
        //     setCookie("username", username, 365);
        // }
        //alert("No cookies found");
    }
}


function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}
