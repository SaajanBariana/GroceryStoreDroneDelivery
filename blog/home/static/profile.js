var dict = {
    'user-name-addr': [1, 0],
    'street-addr': [1,0],
    'city-addr': [1,0],
    'zip-addr': [1,0],
    'state-addr': [1,0],
    'name-cc': [1, 0],
    'zip-cc': [1, 0],
    'number-cc': [1, 0],
    'ccv-cc': [1, 0],
    'exp-cc': [1, 0]
}
var translate = {
    'user-name-addr': 'name',
    'street-addr': 'street',
    'city-addr': 'name',
    'zip-addr': 'zip',
    'state-addr': 'state',
    'name-cc': 'name',
    'zip-cc': 'zip',
    'number-cc': 'ccnumber',
    'ccv-cc': 'ccv',
    'exp-cc': 'exp'
}
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
        var e = a.value + " , " + b.value + " , " + d.value + " , " + c.value;
        createCookie('address', e,1);
    }
    var test = document.getElementById("name-cc");
    if(test.value.length > 0) {
        var f = document.getElementById("zip-cc");
        var g = document.getElementById("number-cc");
        var h = document.getElementById("ccv-cc");
        var i = document.getElementById("exp-cc");
        var j = test.value + "," + f.value + "," + g.value + "," + h.value + "," + i.value;
        createCookie('CreditInfo', j, 1);
    }
}

function loadAddress() {
    var cookies = readCookie('address');
    if (cookies != null) {
        var a = document.getElementsByTagName("ul");
        var b = document.createElement("p");
        b.className = 'userInfo';
        b.innerText = cookies;
        a[2].appendChild(b);
    }
}


function loadNumber() {
    var cookies = readCookie('CreditInfo');
    if (cookies != null) {
        var items = cookies.split(',');
        var a = document.getElementsByTagName("ul");
        var b = document.createElement("p");
        b.className = "userInfo";
        var number = items[2];
        number = number.substring(number.length-4, number.length);
        b.innerText = "**** **** **** " +  number;
        a[3].appendChild(b);
    }
}
function loadProfileInfo() {
    var usr_name = readCookie('username');
    var node = document.getElementById('user-name-addr');
    node.value = usr_name;
    var addressInfo = readCookie('address')
    if (addressInfo != null){
        var elements = addressInfo.split(' , ');
        var temp = elements[0];
        node = document.getElementById('street-addr');
        node.value = temp;
        dict['street-addr'][0] = 0;
        temp = elements[1];
        node = document.getElementById('city-addr');
        node.value = temp;
        dict['city-addr'][0] = 0;
        temp = elements[2];
        node = document.getElementById('state-addr');
        node.value = temp;
        dict['state-addr'][0] = 0;
        temp = elements[3];
        node = document.getElementById('zip-addr');
        node.value = temp;
        dict['zip-addr'][0] = 0;
    }
    var CreditInfo = readCookie('CreditInfo');
    if (CreditInfo != null) {
        var elements = CreditInfo.split(',');
        var temp = elements[0];
        node = document.getElementById('name-cc');
        node.value = temp;
        dict['name-cc'][0] = 0;
        temp = elements[1];
        node = document.getElementById('zip-cc');
        node.value = temp;
        dict['zip-cc'][0] = 0;
        temp = elements[2];
        node = document.getElementById('number-cc');
        node.value = temp;
        dict['number-cc'][0] = 0;
        temp = elements[3];
        node = document.getElementById('ccv-cc');
        node.value = temp;
        dict['ccv-cc'][0] = 0;
        temp = elements[4];
        node = document.getElementById('exp-cc');
        node.value = temp;
        dict['exp-cc'][0] = 0;
    }
}

$(document).ready(function(){
                  $("input").each(function() {
                                  var elem = $(this);
                                  var flag = 1;
                                  var id = elem[0].id;
                                  var translation = translate[id];
                                  var submitBtn = document.getElementsByClassName('btn-primary');
                                  // Save current value of element
                                  elem.data('oldVal', elem.val());

                                  // Look for changes in the value
                                  elem.bind("propertychange change click keyup input paste", function(event){
                                            // If value has changed...
                                            if (elem.data('oldVal') != elem.val()) {
                                            // Updated stored value
                                            elem.data('oldVal', elem.val());

                                            // Do action
                                            if(id == 'user-name-addr' || id == 'name-cc' || id == 'city-addr') {
                                            flag = checkValue(translation, elem[0].value);
                                            }
                                            else if(id == 'street-addr') {
                                            flag = checkValue(translation, elem[0].value);
                                            }
                                            else if (id == 'zip-addr' || id == 'zip-cc') {
                                            flag = checkValue(translation, elem[0].value);
                                            }
                                            else if (id == 'state-addr') {
                                            flag = checkValue(translation, elem[0].value);
                                            }
                                            else if (id == 'number-cc') {
                                            if (elem[0].value.length == 16) {
                                            if (!valid_credit_card(elem[0].value)) {
                                            flag = 1;
                                            }
                                            else {
                                                flag = 0;
                                            }
                                            }
                                            }
                                            else if (id =='ccv-cc') {
                                            flag = checkValue(translation, elem[0].value);
                                            }
                                            else if (id == 'exp-cc'){
                                            flag = checkValue(translation, elem[0].value);
                                            }
                                            }
                                            if (flag == 1) {
                                            submitBtn[1].disabled = true;
                                            submitBtn[1].style.backgroundColor = '#beddff';
                                            submitBtn[1].style.borderColor = '#beddff';
                                            elem[0].style.border = '2px solid red';
                                            dict[id][0] = 1;
                                            if(dict[id][1] == 0) {
                                            errorMessage(translation, elem.parent()[0], 1);
                                            dict[id][1] = 1;
                                            }
                                            }
                                            else {
                                            if (dict[id][1] == 1) {
                                            errorMessage(translation, elem.parent()[0], 0);
                                            dict[id][1] = 0;
                                            }
                                            dict[id][0] = 0;
                                            elem[0].style.border = "";
                                            }
                                            var isComplete = 0;
                                            for (let key in dict) {
                                            let val = dict[key][0];
                                            if (val == 1) {
                                            isComplete = 1;
                                            }
                                            }
                                            if (isComplete == 0) {
                                            submitBtn[1].disabled = false;
                                            submitBtn[1].style.backgroundColor = '#007bff';
                                            submitBtn[1].style.borderColor = '#007bff';
                                            }
                                            });
                                  });
                  });

function errorMessage(input, id, type) {
    if (type == 1) {
        var p = document.createElement('p');
        p.className = 'errorText';
        p.id = 'child';
        p.align = 'left';
        if (input == 'street') {
            p.innerText = 'Please enter a valid street address. Format: #### Name Street.';
        }
        else if (input == 'name') {
            p.innerText = 'That is not a real name';
        }
        else if (input == 'state') {
            p.innerText = 'Format: CA, NV, etc...';
        }
        else if (input == 'zip') {
            p.innerText = 'Please enter a valid zip code. Format: 11111';
        }
        else if (input == 'ccnumber') {
            p.innerText = 'Please enter a valid credit card number.';
        }
        else if (input == 'ccv') {
            p.innerText = 'CCV only contains 3 digit numbers';
        }
        else if (input == 'exp'){
            p.innerText = 'Format: MMYYYY \n Card Expired';
        }
        id.appendChild(p);
    }
    else {
        if(input == 'exp') {
            var child = id.children[3];
            id.removeChild(child);
        }
        else {
            var child = id.children[2];
            id.removeChild(child);
        }
    }
}

function checkValue(input, value) {
    var flag = 0;
    if (input == "state"){
        if (/^[A-Za-z]{2}$/.test(value) == false) {
            flag = 1;
        }
    }
    else if (input == 'name') {
        if (/\d/.test(value) == true) {
            flag = 1;
        }
    }
    else if (input == 'zip') {
        if (/^[0-9]{5}?$/.test(value) == false) {
            flag = 1;
        }
    }
    else if (input == 'exp') {
        var d = new Date();
        if (/^(0[1-9]|1[0-2])\d{4}$/.test(value) == false) {
            flag = 1;
        }
        else if (value.substring(2,value.length) < d.getFullYear()){
            flag = 1;
        }
        else {
            if(value.substring(2,value.length) == d.getFullYear()) {
                if(value.substring(0,2) < d.getMonth()) {
                    flag = 1;
                }
            }
        }
    }
    else if (input == 'ccv') {
        if (/^[0-9]{3}?$/.test(value) == false) {
            flag = 1;
        }
    }
    else if (input == 'street') {
        if (/^\s*\S+(?:\s+\S+){2}/.test(value) == false) {
            flag = 1;
        }
    }
    return flag;
}

function valid_credit_card(value) {
    // accept only digits, dashes or spaces
    if (/[^0-9-\s]+/.test(value)) return false;

    // The Luhn Algorithm. It's so pretty.
    var nCheck = 0, nDigit = 0, bEven = false;
    value = value.replace(/\D/g, "");

    for (var n = value.length - 1; n >= 0; n--) {
        var cDigit = value.charAt(n),
        nDigit = parseInt(cDigit, 10);

        if (bEven) {
            if ((nDigit *= 2) > 9) nDigit -= 9;
        }

        nCheck += nDigit;
        bEven = !bEven;
    }

    return (nCheck % 10) == 0;
}
