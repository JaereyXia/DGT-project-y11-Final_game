/* Toggle between showing and hiding the navigation menu links when the user clicks on the hamburger menu / bar icon */
function myFunction() {
  var links = document.getElementById("myLinks");
  if (links.style.display === "none" || links.style.display === "") {
    links.style.display = "block";
  } else {
    links.style.display = "none";
  }
}