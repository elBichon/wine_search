$(document).ready(function(){
    $("form").on("submit", function(event){
        event.preventDefault();
        var formValues= $(this).serialize();
        var actionUrl = $(this).attr("action");
        $.post(actionUrl, formValues, function(data){
            $("#result").html(data);
        });
    });
});