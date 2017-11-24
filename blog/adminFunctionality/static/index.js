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



// This function trigger after click on "Sign up" button
function sign_up() {
  alert("Hi sign_up");
  
};
