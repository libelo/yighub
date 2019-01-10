//Jquery 쓸 때는 Jquery에 맞게 지정
var sub=document.querySelector(".sub_all");
var sub_one=$(".sub_depth1_drop");
var sub_two=$(".sub_depth2_drop");
var Nav_lst=$(".Nav_lst");
var sub_bar=$(".sub_bar");
var contents=$(".container-fluid");
var menu_btn=$("#menu_btn");
var all_contents=$("#all");
var Vanilla_nav=document.getElementsByClassName("Nav_lst");
var x = window.matchMedia("(max-width: 850px)");

(function() {
  if(window.matchMedia('(max-width:850px)').matches){
      console.log(Vanilla_nav);
    Vanilla_nav[0].style.display="none";
  } else{
    console.log(12);
    }
})();

$(document).ready(function(){

    //Header Showup & disappear 함수
    $("#header").mouseover(function (e) {
        e.preventDefault();
        if (x.matches) { // If media query matches
        } else{
            $("#header").css("height", "220px");
            $(".sub_visual").css("height", "0px");
        }
    });

    $("#header").mouseleave(function (e) {
        e.preventDefault();
        if (x.matches) { // If media query matches
        } else{
            $("#header").css("height", "60px");
            $(".sub_visual").css("height", "160px");
        }
    });

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
