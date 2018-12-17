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
