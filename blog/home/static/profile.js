var address = 0;
var addrSet = [];
var credit = 0;
var ccNumber = [];

function createCookie(name,value,days)
{
    if (days)
    {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 *1000));
        var expires = "; expires=" + date.toGMTString();
    }
    else
    {
        var expires = "";
    }
    document.cookie = name + "=" + value + expires + "; path=/";
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') {
            c = c.substring(1,c.length);
        }
        if (c.indexOf(nameEQ) == 0) {
            return c.substring(nameEQ.length,c.length);
        }
    }
    return null;
}
function getEmail() {
    var a = readCookie('email');
    var b = document.getElementById('usrEmail');
    b.innerText = a;
}
function getUsername() {
    var a = readCookie('name');
    var b = document.getElementById('usrInfo');
    b.innerText = a;
}
function setCookie() {
    var test = document.getElementById("user-name-addr");
    if(test.value.length >0) {
      var a = document.getElementById("street-addr");
      var b = document.getElementById("city-addr");
      var c = document.getElementById("zip-addr");
      var d = document.getElementById("state-addr");
      var e = a.value + ", " + b.value + ", " + d.value + ", " + c.value;
      createCookie('address', e,1);
      //createAddressSet('address' + address);
    }
    var test = document.getElementById("name-cc");
    if(test.value.length > 0) {
        var f = document.getElementById("number-cc");
        createCookie('card', f.value, 1);
        //createCreditSet('card' + credit);
    }
}

/*function createAddressSet(cookie) {
    var a = readCookie('addressSet');
    if (a == null) {
        createCookie('addressSet', cookie, 1);
    }
    else{
        createCookie('addressSet', "", -1);
        b = a + "/" + cookie;
        createCookie('addressSet', b, 1);
    }
}

function createCreditSet(cookie) {
    var a = readCookie('creditSet');
    if (a == null) {
        createCookie('creditSet', cookie, 1);
    }
    else{
        createCookie('creditSet', "", -1);
        b = a + "/" + cookie;
        createCookie('creditSet', b, 1);
    }
}*/

/*
function loadCookieSet() {
    var a = readCookie('addressSet');
    if(a!=null) {
        b = a.split("/");
        for (var i = 0; i < b.length ; i++) {
            addrSet[i] = b[i];
            address += 1;
        }

    }
    var c = readCookie('creditSet');
    if(c!=null) {
        d = c.split("/");
        for (var i = 0; i < d.length; i++) {
            ccNumber[i] = d[i];
            credit += 1;
        }
    }
}
*/

function loadAddress() {
    var a = document.getElementsByTagName("ul");
    var b = document.createElement("p");
    b.className = 'userInfo';
    b.innerText = readCookie('address');
    a[2].appendChild(b);
/*    for (var i = 0; i < address; i++) {
        var b = document.createElement("p");
        b.className = 'userInfo';
        b.innerText = readCookie(addrSet[i]);
        a[2].appendChild(b);
    }*/
}



function loadNumber() {
    var a = document.getElementsByTagName("ul");
    var b = document.createElement("p");
    b.className = "userInfo";
    var number = readCookie('card');
    number = number.substring(number.length-4, number.length);
    b.innerText = "**** **** **** " +  number;
    a[3].appendChild(b);


/*    for (var i = 0; i < credit; i++) {
        var b = document.createElement("p");
        b.className = 'userInfo';
        var number = readCookie(addrSet[i]);
        number = number.substring(number.length-4,number.length);
        b.innerText = "**** **** **** " + number;
        a[3].appendChild(b);
    }*/
}