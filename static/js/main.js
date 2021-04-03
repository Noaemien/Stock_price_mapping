
//triggers the function linked to "test url"
$(function() {
    $('#test').on('click', function(e) {
      e.preventDefault()
      $.getJSON('/test',
          function(data) {
        //do nothing
      });
      return false;
    });
  });