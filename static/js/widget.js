(function() {

// Localize jQuery variable
var jQuery;

/******** Load jQuery if not present *********/
if (window.jQuery === undefined || window.jQuery.fn.jquery !== '1.9.1') {
    var script_tag = document.createElement('script');
    script_tag.setAttribute("type","text/javascript");
    script_tag.setAttribute("src",
        "http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js");
    if (script_tag.readyState) {
      script_tag.onreadystatechange = function () { // For old versions of IE
          if (this.readyState == 'complete' || this.readyState == 'loaded') {
              scriptLoadHandler();
          }
      };
    } else { // Other browsers
      script_tag.onload = scriptLoadHandler;
    }
    // Try to find the head, otherwise default to the documentElement
    (document.getElementsByTagName("head")[0] || document.documentElement).appendChild(script_tag);
} else {
    // The jQuery version on the window is the one we want to use
    jQuery = window.jQuery;
    main();
}

/******** Called once jQuery has loaded ******/
function scriptLoadHandler() {
    // Restore $ and window.jQuery to their previous values and store the
    // new jQuery in our local jQuery variable
    jQuery = window.jQuery.noConflict(true);
    // Call our main function
    main(); 
}

/******** Our main function ********/
function main() { 
    jQuery(document).ready(function($) { 
		var link = $("<link>");
		link.attr({
	    	type: 'text/css',
	   		rel: 'stylesheet',
	   		href: "http://parking.integreen-life.bz.it/parkbz/static/css/widget.css"
		});
		$("head").append( link );
		// Get base layout
		var urlParkWidget = '/parkbz/default/freeslots.jsonp/';

		function load_park_bar(element) {
			park_id = $(element).attr('data-ref');
			domain  = $(element).attr('data-href');
			if ((domain === undefined) || (park_id === undefined)) {
				$(element).html('<div><strong>Error, please check your widget parameters</strong></div>');
				return;
			}
			
			$.ajax({
				type: 'GET',
				url: domain + urlParkWidget + park_id,
				async: false,
				contentType: "application/json",
				dataType: 'jsonp',
				success: function(json) {
					$(element).html(json.plain_html);
				},
				error: function(e) {
				   console.log(e.message);
				}
			});
		}

		placeholders = $('.parking-widget');
		$.each(placeholders, function(i, element) {	
			load_park_bar($(this));
		});
    });
}

})(); // We call our anonymous function immediately
