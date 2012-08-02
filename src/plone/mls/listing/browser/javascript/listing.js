jQuery(function($) {


  if ($('#listing-search').length > 0) {
    // Listing search viewlet.

    if ($('#listing-search div.results').length > 0) {
      // Hide the form when search was performed and show the edit form options link.
      $('div.results > form').hide();
      $('div.results #show-form').show().click(function(event) {
        event.preventDefault();
        $('div.results > form').slideToggle();
      });
    }
  }

  if ($('#listing-images .thumbnails').length > 0) {
    // Build JS Gallery for listing detail view.

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


  if ($('#content-views #contentview-listing-collection-config').length > 0) {
    // Show the listing search configuration form with a nice overlay.
    $('#content-views #contentview-listing-collection-config > a').prepOverlay({
      subtype: 'ajax',
      filter: '#content>*',
      formselector: '#content-core > form',
      noform: 'reload',
      closeselector: '[name=form.buttons.cancel]'
    });
  }

  if ($('#content-views #contentview-listing-search-config').length > 0) {
    // Show the listing search configuration form with a nice overlay.
    $('#content-views #contentview-listing-search-config > a').prepOverlay({
      subtype: 'ajax',
      filter: '#content>*',
      formselector: '#content-core > form',
      noform: 'reload',
      closeselector: '[name=form.buttons.cancel]'
    });
  }

  if ($('#content-views #contentview-recent-listings-config').length > 0) {
    // Show the listing search configuration form with a nice overlay.
    $('#content-views #contentview-recent-listings-config > a').prepOverlay({
      subtype: 'ajax',
      filter: '#content>*',
      formselector: '#content-core > form',
      noform: 'reload',
      closeselector: '[name=form.buttons.cancel]'
    });
  }

});
