$(window).load(function() {
 
    $(".loader_inner").fadeOut();
    $(".loader").delay(400).fadeOut("slow");
   
  });

  function load() {
    let loaders = document.getElementById('loaders');
    loaders.style.display = "grid";
} 