$(document).ready(()=>{
    $("#loginform").show();
    $("#login").click(()=>{
      $("#loginform").show();
    });
    $("#closelogin").click(()=>{
        $("#loginform").hide();
      });

      $("#signup").click(()=>{
        $("#signupform").show();
      });
      $("#closesignup").click(()=>{
          $("#signupform").hide();
        });
    
  });