document.querySelector(".navbar-toggle").onclick = function() {buttonCollapse()};

/* myFunction toggles between adding and removing the show class, which is used to hide and show the dropdown content */
function buttonCollapse() {
  if (document.querySelector(".navbar-collapse").getAttribute("class") == "navbar-collapse collapse"){
    document.querySelector(".navbar-collapse").setAttribute("class", "navbar-collapse");
  }
  else{
    document.querySelector(".navbar-collapse").setAttribute("class", "navbar-collapse collapse");
  };
};