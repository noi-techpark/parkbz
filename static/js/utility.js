function initTooltip(){
		// Remove TEL link on desktop
	    var width = $(window).width();
	    if( width >= 768) {
	        $('.phone a').each(function(){
	            var tel = $(this).html();
	            $(this).replaceWith('<span>'+tel+'</span>');
	        });
	    }

		// Handle graph
	    $('.forecast .graph').hide();
		$('.forecast h3').click(function(){
			$(this).toggleClass('open').next().slideToggle('fast');
		})
		
	};
$(document).ready(function() {
	
	$('.actions .time span,.carpark-selector span').click(function(){
		if(!$(this).hasClass('open')){
			var docHeight = $(document).height();
			$('<div class="overlay-dropdown" style="width:100%;height:'+docHeight+'px;position:absolute;top:0;left:0;bottom:0;right:0;z-index:120"></div>').appendTo('body');
			overlayDropdown(this);
		} else {$('.overlay-dropdown').remove();}
		$(this).toggleClass('open').next().fadeToggle('fast');
	})
	
	function overlayDropdown (e){
		$('.overlay-dropdown').click(function(){
			e.click();
			$('.overlay-dropdown').remove();
		});		
	};	
	
	$('.widget').hide();

	$('.buttons .share-btn').click(function(){
		$(this).toggleClass('open');
		$('.widget').slideToggle('fast');
		$('.share').fadeToggle('fast');
		return false;
	})
	
	initTooltip();
	
	
	// ---- Link esterno ----------------------------------------------------------------------------------------------------------
	
	$("a[href*='http://']:not([href*='"+location.hostname+"']),[href*='https://']:not([href*='"+location.hostname+"'])").attr("target","_blank");	
		
});	
