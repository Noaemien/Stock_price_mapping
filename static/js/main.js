var stop = false;

var it = 1; //Count total amount of iterations since reset
//triggers the function linked to "/nn_iteration/<float:alpha>" when button "run_button" is pressed.
$(function() {
  $('#run_button').on('click', function(e) {
    $("#run_button").prop("disabled",true); //disable the button so that a user cant spam and crash the system
    var link = "/nn_iteration";
    var iterations = $("#iterations").val(); 
    var run_it = 0; //count number of iterations in this run
    stop = false;
    e.preventDefault();
    var beta1 = 0.9;
    var beta2 = 0.999;
    //this function performs a single iteration, it is recursive with a callback 
    function nn_iteration(){
      if (run_it < iterations && stop == false){
        var alpha = $("#alpha_input").val().toString();
         $.post(link,{
          alpha: alpha,
          iteration: it.toString(),
          beta1: beta1.toString(),
          beta2: beta2.toString()
        }, function(data) {
            it++;
            run_it++;
            nn_iteration();    //Loop structured as a callback so that the neural network iteration in the app.py file has the time to finish.
            var cost = $.parseJSON(data); //retrieve json sent by the nn_iteration function in app.py
            $("#cost").html(cost.toString());
            if (run_it == iterations - 1){
              var t1 = performance.now();
              console.log(t1-t0);
            }
      });
      } else if(stop == true || run_it == iterations){ //this is here to stop iterating as soon as stop becomes true, 
        stop == false;
        $("#run_button").prop("disabled",false); //re-enable button so user can start again
      }
    }      
    var t0 = performance.now();
    nn_iteration();
    
    
  });
});


//
//
//
// TO DO
//
//
//
function getBetas(){
  return 0.9, 0.999;
}

//turn stop to true when "stop_button" is clicked
$(function() {
  $('#stop_button').on('click', function(e) {
    stop = true;
    e.preventDefault();
    $("#run_button").prop("disabled",false);
    return false;
  });
});


//triggers the function linked to "/init_params" url when button "init_params" is pressed.
$(function() {
  $('#init_params').on('click', function(e) {
    stop = true;
    var link = "/init_params";
    e.preventDefault();
    it = 1;

    //Take parameters from basic settings
    if (advanced_settings == false){
      var optimisation_f = $("#optimisation_function").val();
      var layer_activations = getLayerActivations();
      var cost_f = $("#cost_function").val();
      for (var i = 0; i < layers.length; i++){
        layers[i] = parseInt( $("#neuron_counter_" + (i + 1).toString() ).val() );
      }

      var post_layers = [].concat(layers);
      post_layers.push(outNeurons);

      console.log(post_layers, layers)
      $.post(link, {
        optimisation_function: optimisation_f,
        layer_activations: JSON.stringify(layer_activations), //Have to stringify list because cannot transfer array as a json.
        layer_neurons: JSON.stringify(post_layers), //Have to stringify list because cannot transfer array as a json. 
        cost_function: cost_f
      });
    } else {
          //What to return if advanced settings are on.
    }
  });
});


//Creates a list with activation functions for each layer
function getLayerActivations(){
  if (advanced_settings == false){
    var h_act = $("#hidden_activation").val();
    var o_act = $("#out_activation").val();
    var activations = []
    for (var i = 0; i < layers.length + 1; i++){  //plus one because of output kayer
      if (i + 1 !== layers.length + 1){ //same reason here
        activations.push(h_act);
      } else {
        activations.push(o_act); 
      }
    }
    return activations;
  }
}

//Enables toggling between basic and advanced settings UI. (Back end still needs work.)
var advanced_settings = false;
function ToggleSettings(){
  if (advanced_settings == false){
    advanced_settings = true;
    $(".basic_settings").css("display", "none");
    $("#toggle_advanced_settings").attr("value", "Default settings");
  } else {
    advanced_settings = false;
    $(".basic_settings").css("display", "block");
    $("#toggle_advanced_settings").attr("value", "Advanced settings");
  }
}

var layers = [];
function AddLayer(){
  var layernbr = layers.length;
  var newLayernbr = parseInt(layernbr) + 1;
  document.getElementById("layer_nbr").value = newLayernbr;

  var newDiv = document.createElement("div");
  var divID = "layer_" + newLayernbr.toString()
  newDiv.id = divID;
  document.getElementById("hidden_layers").appendChild(newDiv);

  var neuronInput_label = document.createElement("LABEL");
  neuronInput_label.htmlFor = "neuron_counter_" + newLayernbr.toString();
  neuronInput_label.innerHTML = "Number of neurons: "
  document.getElementById(divID).appendChild(neuronInput_label);

  var neuronInput = document.createElement("INPUT");
  neuronInput.type = "number";
  if (layers.length == 0){ //If there are no layers, create a new layer with 8 neurons
    neuronInput.value = 8; 
    layers.push(8);
  } else { //If there is at least one layer, create a new layer with the amount of neurons on the previous one.
    var prevLayerNeurons = parseInt($("#neuron_counter_" + (newLayernbr - 1).toString()).val());
    neuronInput.value = prevLayerNeurons;
    layers.push(prevLayerNeurons); 
  }
  neuronInput.id = "neuron_counter_" + newLayernbr.toString();
  neuronInput.className = "layer";
  document.getElementById(divID).appendChild(neuronInput);

}

function RemoveLayer(){
  var layernbr = document.getElementById("layer_nbr").value;
  layernbr = parseInt(layernbr);
  if (layernbr > 0){
    document.getElementById("layer_nbr").value = layernbr - 1;
    $("#layer_" + layernbr.toString()).remove();
    layers.pop();
  }
}


$(function(){
    $("#data_set_import").change(function(){
      var file_name = $("#data_set_import").val();
      var data = new FormData($("#import_form")[0]);

      if (file_name !== ""){ //This verification is done to make sure the user choses a file
        $(".feature_count_class").css("display", "inline-block");
        $.ajax({
          type: "POST",
          url:"/get_dims",
          enctype: "multipart/form-data", //This encryption is required to send files
          data: data,
          cache: false,
          processData: false,
          contentType: false,

          //function to run on success of post
          success: function(data){

            var dimentions = $.parseJSON(data); //request json
            var size_x = dimentions["size_x"]; //get X dims
            var size_y = dimentions["size_y"];

            if (size_y < size_x){
              var temp = size_y;
              size_y = size_x;
              size_x = temp;
            }
            
            $("#choice1").remove();
            $("#choice2").remove();

            var choice1 = document.createElement("option");
            choice1.value = size_x.toString();
            choice1.id = "choice1";
            choice1.innerHTML = size_x.toString();
            $("#feature_count_selection").append(choice1);

            var choice2 = document.createElement("option");
            choice2.value = size_y.toString();
            choice2.id = "choice2";
            choice2.innerHTML = size_y.toString();
            $("#feature_count_selection").append(choice2);
            //
            //
            //
            // Need to add transposition of dataset on change of choice
            //
            //

          } 
        });
      } else {
        $(".feature_count_class").css("display", "none");
      }
    });
});

$(function(){
  $("#select_test_dataset").change(function(){
    var choice = $("#select_test_dataset").val();
    if (choice !== "NONE"){
      $.post("/set_test_dataset", {
        data: choice
      });
    }
  });
});

$(function(){
  $("#feature_count_selection").change(function(){
      $.post("/tranposeX", {
        data: "None"
      });
  });
});

$(function(){
  $("#graph_results").on("click", function(){
      $.post("/graph_results", {
        data: "None"
      }, function(data){
        var im = data;
        var r = new FileReader();

        $('#results_graph').attr('src', r.readAsDataURL(im));
      });
  });
});


var outNeurons = 0;

$(function(){
  $("#data_set_import_y").change(function(){
    var file_name = $("#data_set_import_y").val();
    var data = new FormData($("#import_y_form")[0]);

    if (file_name !== ""){ //This verification is done to make sure the user choses a file
      $.ajax({
        type: "POST",
        url:"/checkYDataset",
        enctype: "multipart/form-data", //This encryption is required to send files
        data: data,
        cache: false,
        processData: false,
        contentType: false,

        //function to run on success of post
        success: function(data){

          var returnedvals = $.parseJSON(data);
          var isSuccess = returnedvals["isSuccess"]; //request json
          if (isSuccess == "0"){
            $("#correct_data_shape").html("These datasets are not compatible.");
            $("#run_button").prop("disabled",true);
            $("#stop_button").prop("disabled",true);
            return "None";
          } else {
            $("#correct_data_shape").html("These datasets are compatible.");
            $("#run_button").prop("disabled",false);
            $("#stop_button").prop("disabled",false);
            $("#add_layer_button").prop("disabled",false);
            $("#del_layer_button").prop("disabled",false);


            var outputsRequired = parseInt(returnedvals["size_y"]);

            if ($("#last_neuron").length){ //if last_neuron exists, just modify its value to the correct number of outputs
              $("#last_neuron").val(outputsRequired);
              layers[layers.length - 1] = outputsRequired;
            } else { //if last_neuron doesnt exist, create it with the correct number of neurons

              var lastNeuronInput_label = document.createElement("LABEL");
              lastNeuronInput_label.htmlFor = "last_neuron";
              lastNeuronInput_label.innerHTML = "Ouput neurons: "
              document.getElementById("layers").appendChild(lastNeuronInput_label);


              var lastNeuronInput = document.createElement("INPUT");  
              lastNeuronInput.type = "number";
              lastNeuronInput.value = outputsRequired; //to get the correct number of neurons
              outNeurons = outputsRequired; 
              lastNeuronInput.id = "last_neuron";
              lastNeuronInput.className = "layer";
              lastNeuronInput.readOnly = true;
              document.getElementById("layers").appendChild(lastNeuronInput);


          }
          
            
          }

          
        } 
      });
    }
  });
});
