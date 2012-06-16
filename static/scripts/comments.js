$(document).ready(function(){
  $("#comment-submit").click(function(){
    return validateComment();
  });
});

function validateComment(){
  var isValidated = true;
  if($("#name-input").val().trim() == ""){
    $("#name-error").removeClass("unshown");
    isValidated = false;
  }else{
    $("#name-error").addClass("unshown");
  }
  if($("#email-input").val().trim() == ""){
    $("#email-error").removeClass("unshown");
    isValidated = false;
  }else{
     if(!$("#email-input").val().match(/^\w+((-\w+)|(\.\w+))*\@[A-Za-z0-9]+((\.|-)[A-Za-z0-9]+)*\.[A-Za-z0-9]+$/)){
       $("#email-error").removeClass("unshown");
       isValidated = false;
     }else{
      $("#email-error").addClass("unshown");
     }
  }
  if($("#comment-input").val().trim() == ""){
    $("#comment-error").removeClass("unshown");
    isValidated = false;
  }else{
    $("#comment-error").addClass("unshown");
  }
  return isValidated;
}
