const links = document.querySelectorAll('.category-link');

links.forEach(link => {
  link.addEventListener('click', function() {
    // Prevent default behavior of link
    e.preventDefault();
    links.forEach(link => link.classList.remove('active'));     // remove the active class from all links
    this.classList.add('active');       // add the active class to the clicked link

  });
});
