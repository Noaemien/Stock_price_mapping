var stop = false;
//triggers the function linked to "/nn_iteration/<float:alpha>" when button "run_button" is pressed.
$(function() {
    $('#run_button').on('click', function(e) {
      var link = "/nn_iteration/" + document.getElementById("alpha_input").value.toString();
      var iterations = document.getElementById("iterations").value; 
      var i = 0;
      stop = false;
      e.preventDefault();
      function nn_iteration(){
        if (i < iterations && stop == false){
          $.getJSON(link,          //run nn_iteration function in app.py
              function(data) {
                i++;
                nn_iteration();    //Loop structured as a callback so that the neural network iteration in the app.py file has the time to finish.
                var cost = $.parseJSON(data); //retrieve json sent by the nn_iteration function in app.py
                document.getElementById("cost").innerHTML = cost.toString();
          });
        } else if(stop == true){
          stop == false;
        }
      }      
      function get_cost(a){
        $.get("/nn_iteration/0", function(data){
          var cost = $.parseJSON(data);
          console.log(cost);
        });
      }
      nn_iteration();

      return false;
    });
  });

//turn stop to true on click of "stop_button"
$(function() {
  $('#stop_button').on('click', function(e) {
    stop = true;
    e.preventDefault();
    return false;
  });
});


//triggers the function linked to "/init_params" url when button "init_params" is pressed.
$(function() {
  $('#init_params').on('click', function(e) {
    stop = true;
    var link = "/init_params";
    e.preventDefault();
    $.getJSON(link,
        function(data) {
    });
    return false;
  });
});
