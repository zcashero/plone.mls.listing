$(document).ready(function() {

  // Build JS Gallery
  if ($('#listing-images .thumbnails').length > 0) {
    // Load the theme ones more. This is necessary for mobile devices.
    Galleria.loadTheme('++resource++plone.mls.listing.javascript/classic/galleria.classic.min.js');
    $('#listing-images a.preview').replaceWith('<div id="galleria"></div>');

    // Hide the thumbnails
    $('#listing-images .thumbnails').hide();

    // Initialize Galleria.
    var galleria_obj = $('#galleria').galleria({
      dataSource: '.thumbnails',
      width: 410,
      height: 400,
      preload: 3,
      transition: 'fade',
      transitionSpeed: 1000,
      autoplay: 5000
    });
  }

});
