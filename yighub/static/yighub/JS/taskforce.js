$(document).ready(function () {
   $('.icon>a').click(function (e) {
       e.preventDefault();
       console.log(2);
       $('.icon>a').toggleClass('change');

       if($('.nav-list').css("display")=="none"){
        $('.nav-list').css("display", "block");
       }else{
        $('.nav-list').css("display", "none");
       }
   });

});