
$("#seeAnotherField").change(function() {
      if ($(this).val() == "label") {
        $('#otherFieldDiv').hide();
        $('#otherFieldDiv1').hide();
        $('#otherFieldDiv2').hide();
        $('#otherFieldDiv').show();
        $('#otherField').attr('required','');
        $('#otherField').attr('data-error', 'This field is required.');
      } 
      else if ($(this).val() == "name") {
        $('#otherFieldDiv').hide();
        $('#otherFieldDiv1').hide();
        $('#otherFieldDiv2').hide();
        $('#otherFieldDiv1').show();
        $('#otherField1').attr('required','');
        $('#otherField1').attr('data-error', 'This field is required.');
      } 
      else if ($(this).val() == "help") {
        $('#otherFieldDiv').hide();
        $('#otherFieldDiv1').hide();
        $('#otherFieldDiv2').hide();
        $('#otherFieldDiv2').show();
        $('#otherField2').attr('required','');
        $('#otherField2').attr('data-error', 'This field is required.');
      } 
      else{
        $('#otherFieldDiv').hide();
        $('#otherFieldDiv1').hide();
        $('#otherFieldDiv2').hide();
      }
    });
    $("#seeAnotherField").trigger("change");