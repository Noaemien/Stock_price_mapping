
//triggers the function linked to "/nn_iteration/<float:alpha>" when button "run_button" is pressed.
$(function() {
    $('#run_button').on('click', function(e) {
      var link = "/nn_iteration/" + document.getElementById("alpha_input").value.toString();
      var iterations = document.getElementById("iterations").value; 
      var i = 0;
      e.preventDefault();
      function nn_iteration(){
        if (i < iterations){
          $.getJSON(link,          //run nn_iteration function in app.py
              function(data) {
                i++;
                nn_iteration();    //Loop structured as a callback so that the neural network iteration in the app.py file has the time to finish.
          });
        }
      }
      nn_iteration();
      return false;
    });
  });

//triggers the function linked to "/init_params" url when button "init_params" is pressed.
$(function() {
  $('#init_params').on('click', function(e) {
    var link = "/init_params";
    e.preventDefault();
    $.getJSON(link,
        function(data) {
    });
    return false;
  });
});
