( function( $ ) {

  $(document).ready(function($){

  	// News ticker.
  	var $news_ticker = $('#news-ticker');
  	if ( $news_ticker.length > 0 ) {
  		$news_ticker.easyTicker({
  			direction: 'up',
  			easing: 'swing',
  			speed: 'slow',
  			interval: 3000,
  			height: 'auto',
  			visible: 1,
  			mousePause: 1
  		});
  	}

    // Implement go to top.
	var $scroll_obj = $( '#btn-scrollup' );
	$( window ).on( 'scroll',function(){
		if ( $( this ).scrollTop() > 100 ) {
			$scroll_obj.fadeIn();
		} else {
			$scroll_obj.fadeOut();
		}
	});

	$scroll_obj.on( 'click',function(){
		$( 'html, body' ).animate( { scrollTop: 0 }, 600 );
		return false;
	});

  });

} )( jQuery );
