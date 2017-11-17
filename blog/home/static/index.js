var password;

/* dictionary:
    html id: [is it completed flag : is there error message flag]
 */
var dict = {
    Username_login: [1, 0],
    user_name: [1,0],
    password_login: [1,0],
    password_repeat: [1,0]
}
/*$(".info-item .btn").click(function(){
  $(".container").toggleClass("log-in");
  
  
});

//THis is old line 
// $(".container-form .btn").click(function(){
//  // $(".container").addClass("active");

// });

// This function trigger after click on "login" button
function login() {
  //alert("Hi login");
  var x = document.getElementById('Username_login');
  //var y = x.getElementsByName('Username');
  // console.log(x[0]);
  // console.log(document.getElementsByName("form-item log-in .Username_login")[0].value);

  console.log(x.value);
  //console.log(y);

  var username = x.value;
  
  $.ajax({
        url: 'login_register_request/',
        data: {
          'username': username
        },
        dataType: 'json',
        success: function (data) {
          if (data.is_taken) {
            alert("A user with this username already exists.");
          }
        },
        error: function (data) {
          if (data.is_taken) {
            alert("A user with this username already exists.");
          }
        }
      });

  
};



// This function trigger after click on "Sign up" button
function sign_up() {
  alert("Hi sign_up");
  
};*/

function buttonCreate() {
    var a = $(".container");
    document.getElementById('login-form').style.display="none";
    document.getElementById('signup-form').style.display="block";
}
function buttonLogin() {
    var a = $(".container");
    document.getElementById('signup-form').style.display="none";
    document.getElementById('login-form').style.display="block";
}
function checkValue(input, value) {
    var flag = 0;
    if (input == "pass") {
        if (/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}/.test(value) ==  false) {
            flag = 1;
        }
    }
    else if (input == "email"){
        if (/^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(value) == false) {
            flag = 1;
        }
    }
    else {
        if (/\d/.test(value) == true) {
            flag = 1;
        }
    }
    return flag;
}
function errorMessage(input, id, type) {
    if (type == 1) {
        var p = document.createElement('p');
        p.className = 'errorText';
        p.id = 'child';
        p.align = 'left';
        if (input == 'email') {
            p.innerText = 'Please enter a valid email address. Use letters (a-z), numbers, and the following characters: + - _ @ . only';
        }
        else if (input == 'user') {
            p.innerText = 'That is not a real name';
        }
        else if (input == 'pass') {
            p.innerText = 'Use at least one lowercase letter, one uppercase letter, one numeral, one special character, and 8 characters';
        }
        else if (input == 'repeat') {
            p.innerText = 'Password does not match';
        }
        id.appendChild(p);
    }
    else {
        var child = id.children[1];
        id.removeChild(child);
    }
}

$("input").each(function() {
    var elem = $(this);
    var flag = 0;
    var id = elem[0].id;
    var value;
    var parent = elem.parent().parent().parent();
    var submitBtn = document.getElementById("create-send");
    // Save current value of element
    elem.data('oldVal', elem.val());

    // Look for changes in the value
    elem.bind("propertychange change click keyup input paste", function(event){
        // If value has changed...
        if (elem.data('oldVal') != elem.val()) {
            // Updated stored value
            elem.data('oldVal', elem.val());

            // Do action
            if(parent[0].id == 'signup-form') {
                if (id == 'Username_login') {
                    value = 'email';
                    flag = checkValue('email', elem[0].value);
                }
                else if (id == 'user_name') {
                    value = 'user';
                    flag = checkValue('user', elem[0].value);
                }
                else if (id =='password_login') {
                    value = 'pass';
                    flag = checkValue('pass', elem[0].value);
                }
                else if (id == 'password_repeat') {
                    if (password != elem[0].value) {
                        value = 'repeat';
                        flag = 1;
                    }
                    else {
                        flag = 0;
                    }
                }

                if (flag == 1) {
                    submitBtn.disabled = true;
                    submitBtn.style.backgroundColor = '#A56A6A';
                    elem[0].style.border = '2px solid red';
                    dict[id][0] = 1;
                    if (dict[id][1] == 0){
                        errorMessage(value, elem.parent()[0], 1);
                        dict[id][1] = 1;
                    }
                    if (id == 'password_login') {
                      password = "";
                    }
                }
                else {
                    if (id == 'password_login') {
                        password = elem[0].value;
                    }
                    if (dict[id][1] == 1) {
                        errorMessage(value, elem.parent()[0], 0);
                        dict[id][1] = 0;
                    }
                    elem[0].style.border = "";
                    dict[id][0] = 0;
                }
                var isComplete = 0;
                for (let key in dict) {
                    let val = dict[key][0];
                    if (val == 1) {
                        isComplete = 1;
                    }
                }
                if (isComplete == 0) {
                    submitBtn.disabled = false;
                    submitBtn.style.backgroundColor = '#ff4d4d';
                }
            }

        }
    });
});