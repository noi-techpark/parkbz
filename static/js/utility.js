function initTooltip(){
	// Remove TEL link on desktop
    var width = $(window).width();
    if( width >= 768) {
        $('.phone a').each(function(){
            var tel = $(this).html();
            $(this).replaceWith('<span>'+tel+'</span>');
        });
    }
};

$(document).on('click', '.forecast h3', function(){
    var el = $(this);
	$(this).toggleClass('open').next().slideToggle('fast', function() {
	    $(el).trigger('slidend');
	});
});

$(document).on('click', '.actions .time span,.carpark-selector span,.lang span', function(){
	if(!$(this).hasClass('open')){
		var docHeight = $(document).height();
		//$('<div class="overlay-dropdown" style="width:100%;height:'+docHeight+'px;position:absolute;top:0;left:0;bottom:0;right:0;z-index:120"></div>').appendTo('body');
		//overlayDropdown(this);
	} else {
	    $('.overlay-dropdown').remove();
	}
	$(this).toggleClass('open').next().fadeToggle('fast');
});

$(document).on('click', '.buttons .share-btn', function(){
	$(this).toggleClass('open');
		$('.widget').slideToggle('fast');
		$('.share').fadeToggle('fast');
		return false;
});

function overlayDropdown (e){
    $('.overlay-dropdown').off('click');
	$('.overlay-dropdown').on('click',function(){
		e.click();
		$('.overlay-dropdown').remove();
	});	
};	

$(document).ready(function() {
	$('.widget').hide();
	initTooltip();
	// ---- Link esterno ----------------------------------------------------------------------------------------------------------
	$("a[href*='http://']:not([href*='"+location.hostname+"']),[href*='https://']:not([href*='"+location.hostname+"'])").attr("target","_blank");	
});	
