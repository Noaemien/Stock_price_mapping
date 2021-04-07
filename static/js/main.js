var stop = false;

var it = 1; //Count total amount of iterations since reset
//triggers the function linked to "/nn_iteration/<float:alpha>" when button "run_button" is pressed.
$(function() {
    $('#run_button').on('click', function(e) {
      var link = "/nn_iteration/" + document.getElementById("alpha_input").value.toString();
      var iterations = $("#iterations").val(); 
      var run_it = 0; //count number of iterations in this run
      stop = false;
      e.preventDefault();
      var beta1 = 0.9;
      var beta2 = 0.999;
      function nn_iteration(){
        if (run_it < iterations && stop == false){
          var alpha = $("#alpha_input").val().toString();

          $.post("/nn_iteration",{
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
        });
          
          /*
          $.getJSON(link,          //run nn_iteration function in app.py
              function(data) {
                it++;
                nn_iteration();    //Loop structured as a callback so that the neural network iteration in the app.py file has the time to finish.
                var cost = $.parseJSON(data); //retrieve json sent by the nn_iteration function in app.py
                $("#cost").attr("innerHTML", cost.toString());
          });*/
        } else if(stop == true){
          stop == false;
        }
      }      
      nn_iteration();
      return false;
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
      var optimisation_f = document.getElementById("optimisation_function").value;
      var layer_activations = getLayerActivations();
      for (var i = 0; i < layers.length; i++){
        layers[i] = parseInt(document.getElementById("neuron_counter_" + (i + 1).toString()).value);
      }
      $.post(link, {
        optimisation_function: optimisation_f,
        layer_activations: JSON.stringify(layer_activations), //Have to stringify list because cannot transfer array as a json.
        layer_neurons: JSON.stringify(layers) //Have to stringify list because cannot transfer array as a json. 
      });
    } else {
          //What to return if advanced settings are on.
    }
  });
});

function getLayerActivations(){
  if (advanced_settings == false){
    var h_act = $("#hidden_activation").val();
    var o_act = $("#out_activation").val();
    var activations = []
    for (var i = 0; i < layers.length; i++){
      if (i + 1 !== layers.length){
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
  document.getElementById("layers").appendChild(newDiv);

  //Generate button to add neuron to layer
  var newAddButton = document.createElement("BUTTON");
  newAddButton.innerHTML = "Add neuron";
  newAddButton.onclick = "AddNeuron()";
  document.getElementById(divID).appendChild(newAddButton);

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
    var prevLayerNeurons = parseInt(document.getElementById("neuron_counter_" + layernbr).value)
    neuronInput.value = prevLayerNeurons;
    layers.push(prevLayerNeurons); 
  }
  neuronInput.id = "neuron_counter_" + newLayernbr.toString();
  neuronInput.className = "layer";
  document.getElementById(divID).appendChild(neuronInput);


  var newRemoveButton = document.createElement("BUTTON");
  newRemoveButton.innerHTML = "Remove neuron";
  newRemoveButton.onclick = "RemoveNeuron()";
  document.getElementById(divID).appendChild(newRemoveButton);

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


