$(document).ready(function() {
		
	
	// Remove TEL link on desktop
    var width = $(window).width();
    if( width >= 768) {
        $('.phone a').each(function(){
            var tel = $(this).html();
            $(this).replaceWith('<span>'+tel+'</span>');
            
        });
    } 
	
	
	$('.actions .time span,.carpark-selector span').click(function(){
		$(this).toggleClass('open').next().fadeToggle('fast');
	})
	
	$('.forecast .graph').hide();
	
	$('.forecast h3').click(function(){
		$(this).toggleClass('open').next().slideToggle('fast');
	})
	
	$('.widget').hide();
	$('.buttons .share-btn').click(function(){
		$(this).toggleClass('open');
		$('.widget').slideToggle('fast');
		$('.share').fadeToggle('fast');
		return false;
	})
	
	
	
	// ---- Link esterno ----------------------------------------------------------------------------------------------------------
	
	$("a[href*='http://']:not([href*='"+location.hostname+"']),[href*='https://']:not([href*='"+location.hostname+"'])").attr("target","_blank");	
	
	
		
});	