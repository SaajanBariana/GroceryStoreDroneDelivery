$(".info-item .btn").click(function(){
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

function buttonCreate() {
    var a = $(".container");
    a.height(540);
    document.getElementById('login-form').style.visibility="hidden";
    document.getElementById('signup-form').style.visibility="visible";
}
function buttonLogin() {
    var a = $(".container");
    a.height(400);
    document.getElementById('signup-form').style.visibility="hidden";
    document.getElementById('login-form').style.visibility="visible";
}



// This function trigger after click on "Sign up" button
function sign_up() {
  alert("Hi sign_up");

};
