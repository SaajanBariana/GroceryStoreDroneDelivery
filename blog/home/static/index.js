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


function sendTracking(e)
{
  e.preventDefault(); // prevent auto refresh maybe 
  if(trackingNumber.value != "")
  {
    var trackNumber = trackingNumber.value;

   $.ajax({ //This is the dictionary
        url : "./post_tracking", // the endpoint (where to send the data and goes to url the to views)
        type : "GET", // http method
        data : { tNumber : trackNumber, //what we sending 
            csrfmiddlewaretoken: '{{ csrf_token }}' //bypass secuirty permission
         }, // data sent with the post request

        // handle a successful response
        success : function(json) {
            //$('#trackingNumberInput').val(''); // remove the value from the input
          //  console.log("tracking number sent back by server", json); // log the returned json to the console
          //  setTrackingPageValues(json);
          window.location.href = 'track'; //ocnce successfully data is sent then track is called in URL to Views
            console.log("success"); // another sanity check

        },

        // handle a non-successful response
        error : function(err)
        {
          console.log("data could not be sent to server");
        }
        
    });
}
else 
{ 
  console.log("no input");
    alert("Please enter Tracking Number for your Order")
}

}


// This function trigger after click on "Sign up" button
function sign_up() {
  alert("Hi sign_up");
  
};


