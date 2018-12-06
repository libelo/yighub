//Jquery 쓸 때는 Jquery에 맞게 지정
var sub=document.querySelector(".sub_all");
var sub_one=$(".sub_depth1_drop");
var sub_two=$(".sub_depth2_drop");
var Nav_lst=$(".Nav_lst");
var sub_bar=$(".sub_bar");
var contents=$(".container-fluid");

function showup(){
    sub.style.height="100%";
};

function disappear() {
    sub.style.height="0%";
};

$(document).ready(function(){
   $(".Nav_lst>ul>li").click(function (e) {
       e.preventDefault();
       $(this).children("ul").toggleClass("show");
   });

   $("#menu_btn").click(function (e) {
      e.preventDefault();
      if(Nav_lst.css("display")=="none"){
          Nav_lst.css("display", "block");
          sub_bar.css("display", "none");
          contents.css("display", "none");
      } else{
          Nav_lst.css("display", "none");
          sub_bar.css("display", "block");
          contents.css("display", "block");
      }
   });

   $(".sub_depth1").click(function (e) {
       e.preventDefault();
       sub_one.toggleClass("show");
   });

   $(".sub_depth2").click(function (e) {
       e.preventDefault();
       sub_two.toggleClass("show");
   });
});
