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
        var resources_url='http://127.0.0.1:8000/parkbz/static/'
		var link = $("<link>");
		link.attr({
	    	type: 'text/css',
	   		rel: 'stylesheet',
	   		href: resources_url + "css/standard.css"
//	   		href: "http://parking.bz.it/parkbzNew/static/css/standard.css"
		});
		$("head").append( link );
	    var script   = document.createElement("script");
        script.type  = "text/javascript";
        script.src   = resources_url + 'js/app.js';
        document.body.appendChild(script);
        $.ajaxSetup({
            cache: true
        });
		script_list= ['date.js', 'jquery.flot.js', 'jquery.flot.time.js', 'jquery.flot.resize.js', 'jquery.flot.tooltip.js', 'jquery.flot.axislabels.js', 
		'jquery.flot.threshold.js'];
        for (i=0; i<script_list.length; i++) {
            /*$.getScript(resources_url + 'js/' + script_list[i], function( data, textStatus, jqxhr ) {
            });*/
      	    var script   = document.createElement("script");
            script.async = false;
            script.type  = "text/javascript";
            script.src   = resources_url + 'js/' + script_list[i];
            document.body.appendChild(script);
        }
		// Get base layout
		var urlParkWidget = '/parkbz/widget/index/';

		function load_park_bar(element) {
			park_id = $(element).attr('data-id');
			domain  = $(element).attr('data-ref');
			if ((domain === undefined) || (park_id === undefined)) {
				$(element).html('<div><strong>Error, please check your widget parameters</strong></div>');
				return;
			}

			$.getJSON(domain + urlParkWidget + park_id, function(data){
        			html = $.parseHTML(data.plain_html);
					$(element).html(html);
					var script   = document.createElement("script");
                    script.type  = "text/javascript";
                    script.text  = data.plain_script;
                    document.body.appendChild(script);
                    
                    if ((typeof parking_interval != 'undefined') && (parking_interval)) {
                        clearInterval(parking_interval);
                    }
                    parking_interval = setInterval( function() {
                        $('.carpark').trigger('reload', true);
                    }, 300000 );
                    setTimeout( function() {
                        console.log('cc');
                        $('.carpark').trigger('reload', true);
                    }, Math.floor((Math.random()*10)+1)*250);
            });
		}

		placeholders = $('.parking-widget');
		$.each(placeholders, function(i, element) {	
			load_park_bar($(this));
		});
    });
}

})(); // We call our anonymous function immediately
