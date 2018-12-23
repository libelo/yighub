var x = window.matchMedia("(max-width: 750px)");

$(".Main_nav").mouseover(function(e){
    e.preventDefault();
    var subnav=$(".subnav");

    if (x.matches) { // If media query matches

    } else {
        subnav.addClass("show");
    }
  });

$(".Main_nav").mouseout(function(e){
    e.preventDefault();
      var subnav=$(".subnav");
      subnav.removeClass("show");
  });

//Jquery 쓸 때는 Jquery에 맞게 지정
var Nav_lst=$(".Nav_lst");
var menu_btn=$("#menu_btn");

$(document).ready(function(){

   //Nav 클릭시 sub_nav 통제 함수

   $(".drive>a").click(function (e) {
       e.preventDefault();
       $(this).parent().children("ul").toggleClass("show");
   });

   //Manu_btn 클릭시 .Nav_lst 통제 함수
   $("#menu_btn").click(function (e) {
      e.preventDefault();
      if(Nav_lst.css("display")=="none"){
          Nav_lst.css("display", "block");
          sub_bar.css("display", "none");
          contents.css("display", "none");
          all_contents.css("display", "none");
      } else{
          Nav_lst.css("display", "none");
          sub_bar.css("display", "block");
          contents.css("display", "block");
          all_contents.css("display", "block");
      }
   });

   //menu_btn Max_width로 인한 버그 수정
    if(menu_btn.css("display")=="none"){
        Nav_lst.css("display", "none");
    }
});

