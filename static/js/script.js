$(window).load(function() {
 
    $(".loader_inner").fadeOut();
    $(".loader").delay(400).fadeOut("slow");
   
  });

function load() {
    let loader = document.getElementById('loader');
    loader.style.display = "grid";
}