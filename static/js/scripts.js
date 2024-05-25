
const movies = document.querySelectorAll('.movie');
const shows = document.querySelectorAll('.tv-show');
        
function addBlur(event) {
    event.target.classList.add('blur');
}

function removeBlur(event) {
    event.target.classList.remove('blur');
}

for (let movie of movies) {
    movie.addEventListener('mouseenter', addBlur);
    movie.addEventListener('mouseleave', removeBlur);
}

for (let show of shows) {
    show.addEventListener('mouseenter', addBlur);
    show.addEventListener('mouseleave', removeBlur);
}

function showPassword(id) {
    var x = document.getElementById(id);
    if (x.type === "password") {
      x.type = "text";
    } else {
      x.type = "password";
    }
}