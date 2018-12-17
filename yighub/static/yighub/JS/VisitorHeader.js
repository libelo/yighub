//Jquery 쓸 때는 Jquery에 맞게 지정
var sub=document.querySelector(".sub_all");
var sub_one=$(".sub_depth1_drop");
var sub_two=$(".sub_depth2_drop");
var Nav_lst=$(".Nav_lst");
var sub_bar=$(".sub_bar");
var contents=$(".container-fluid");
var menu_btn=$("#menu_btn");

function showup(){
    sub.style.height="100%";
};

function disappear() {
    sub.style.height="0%";
};

$(document).ready(function(){

   //Nav 클릭시 sub_nav 통제 함수
   $(".Nav_lst>ul>li").click(function (e) {
       e.preventDefault();
       $(this).children("ul").toggleClass("show");
   });

   //Manu_btn 클릭시 .Nav_lst 통제 함수
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

   //menu_btn Max_width로 인한 버그 수정
    if(menu_btn.css("display")=="none"){
        Nav_lst.css("display", "none");
    }

   $("#current").click(function (e) {
       e.preventDefault();
       sub_one.toggleClass("show");
       if($(".sidebar-nav").css("margin-top")!="200px"){
        $(".sidebar-nav").css("margin-top", "200px");
       }else{
        $(".sidebar-nav").css("margin-top", "20px");   
       }
   });

   $("#current_two").click(function (e) {
       e.preventDefault();
       sub_two.toggleClass("show");
       if($(".sidebar-nav").css("margin-top")!="100px"){
        $(".sidebar-nav").css("margin-top", "100px");
       }else{
        $(".sidebar-nav").css("margin-top", "20px");
       }
   });
});
