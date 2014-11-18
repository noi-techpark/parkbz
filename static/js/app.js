
/* fix missing indexOf for ie8 */
if (!('indexOf' in Array.prototype)) {
    Array.prototype.indexOf= function(find, i /*opt*/) {
        if (i===undefined) i= 0;
        if (i<0) i+= this.length;
        if (i<0) i= 0;
        for (var n= this.length; i<n; i++)
            if (i in this && this[i]===find)
                return i;
        return -1;
    };
}

var template_js = '<p class="repo-name"><a href="{{link}}"><strong>{{name}}</strong></a></p><small>{{address}}</small>';
var type='free';
var default_msg = free_slot_text;
var msg = default_msg;
var period=undefined;
var text;
var popup_open;
$(document).on("slidend", ".forecast h3.open", function(e) {
    if (popup_open != undefined) {
        popup_open._adjustPan();    // _adjustPan is an internal function, it could change in the future
    }
    var ph = $(this).siblings('.graph')[0];
    var prediction_url = $(this).data("url");
    var slots = $(this).data("slots");
    var chart = new plot(ph, prediction_url, slots);
});

$(document).on("click", "#updateall", function(e) {
    $('.carpark').trigger('reload');
});

$(document).on("reload", '.carpark', function(e, avoid_notification) {
    el = $(this);
    park_id = $(el).data('id');
    park_url = $(el).data('url');
    realtime_slots(park_id, park_url, avoid_notification);
});

$(document).on("click", '.times a', function(e) {
    var el = $(this);
    type = $(el).data('type'); //'Parking forecast'
    period = $(el).data('period');
    text = $(el).html();
    if ($(el).data('default-msg')){
        msg = el.html();
        $('main').addClass('forecast');
    } else {
        msg = default_msg;
        $('main').removeClass('forecast');
    }
    $('.time span.box.round').html(el.html());
    $('.carpark').trigger('reload', true);
    $('.times.round.box').fadeToggle('fast');
//    $('.overlay-dropdown').remove();
    $('.actions .time li.current').removeClass('current');
    $(el).parent('li').addClass('current');
    $('.map-cont').trigger('forecast', true);
});

function realtime_slots (id, url, avoid_notification) {
    var el = $( '#park_'+id);
    $(".slots .updating", el).show();
    $(".actions .notice-update").hide();
    var params = { type:type, period:period };
    url_request = url + '&' + jQuery.param(params);
    $.ajax({
		url: url_request,
		method: 'GET',
	    dataType: 'json',
	    complete: function() {
            $(".slots .updating", el).hide();
	    }, 
	    success: function(json) {
            $('.available-slots', el).removeClass('almost-full');
            $('.available-slots', el).removeClass('available');
            $('.available-slots', el).removeClass('full');
	        if(json.length == 0) {
                $(".notice-time").hide();
                $('.number', el).html("...");
                $(".value_time", el).html('')
                return
            }

	        //if (n_realtime_active_operations === 0) {
            //    $(that.placeholder).trigger($.Event('loaded',{}));
            //}
            $('.number', el).html(json.freeslots);
            
            if (! avoid_notification) {
                $(".actions .notice-update").show();
                $(".actions .notice-update").delay(5000).fadeOut(500);
            }
            if (json.freeslots < 10){
                css_class = 'full';
            } else if (json.freeslots < 70){
                css_class = 'almost-full'
            } else {
                css_class = 'available'
            }

            $('.available-slots', el).addClass(css_class);
            //{{='full' if park['freeslots'] < 10 else ('almost-full' if park['freeslots'] < 70 else 'available')}}
            if (json.created_on) {
                $(".notice-time span").html(json.created_on);
                $(".notice-time").show();
                $(el).addClass('forecast');
                $(".value_time", el).html(msg);
            } else {
                $(".notice-time").hide();
                $(el).removeClass('forecast');
                $(".value_time", el).html('');
            }
	    },
	    error: function (e, status) {
            $('.available-slots', el).removeClass('almost-full');
            $('.available-slots', el).removeClass('available');
            $('.available-slots', el).removeClass('full');
            $(".notice-time").hide();
            $('.number', el).html("...");
            $(".value_time", el).html('');
            return
	    },
	});
}

function plot (placeholder, url, slots) {
    timezoneJS.timezone.zoneFileBasePath = '/' + appName + '/static/js/tz';

    this.default_options = {
        xaxis: { mode: "time", timezone: "Europe/Rome", alignTicksWithAxis:true,},
	    series: {
		    lines: {
			    show: false
		    },
		    points: {
			    show: false
		    },
		    bars: {
		        show: true, barWidth: 900*1000*0.8, fill: 1, linewidth:0,align: "center",
		    }
	    },
	    grid: {
			color: "#444444",
			backgroundColor: {
				colors: ["#fff", "#e4f4f4"]
			},
			borderColor: "#FFFFFF",
			//tickColor: "#CCCCCC",
			//aboveData: false,
			//borderWidth: 1,
			clickable: true,
			hoverable: true,
			autoHighlight: true,
			markings: [
			    { color: "#FF0000", lineWidth: 1, yaxis: {} }
		    ],
		},
	    yaxis: {
		    min: 0, max: this.slots,
		    axisLabel: free_slot_text,
		    axisLabelFontFamily: "Helvetica Neue,Helvetica,Arial,sans-serif",
		    axisLabelPadding: 2,
		    //tickSize: 200,
		    ticks: 4, //[0, [this.slots, "\u03c0/2"]],
		    //axisLabelUseCanvas: true,
			//axisLabelFontSizePixels: 1em,
	    },
	    tooltip: true, 
		tooltipOpts: {
			content:      free_slot_text + " %y",
			xDateFormat: "%b %d, %H:%M:%S",
			defaultTheme:  true,
		},

	    legend: false,
	};

    this.data = [{
		    threshold: [{
				below: 70,
				color: "rgb(247,154,8)"
			}, {
				below: 10,
				color: "rgb(200, 20, 30)"
			}],
            color: "rgb(111,170,41)",
			data: []
	}];

    this.onDataReceived = function (json, url) {
        if(json.length == 0) {
            return this.data_not_available();
        }
        this.data[0].data = json;
        this.default_options.yaxis.max = this.slots + (0.1*this.slots);
        this.default_options.grid.markings[0].yaxis = {from:this.slots, to:this.slots}; // RED line 
        this.plot = $.plot(this.ph, this.data, this.default_options);
        //var thatC = this;
        //setTimeout(function(){
            //o = thatC.plot.pointOffset({ x: 0, y: thatC.slots});
        $(this.ph).append("<div class='capacity'>" + capacity + "</div>");
		    //$(thatC.ph).append("<div class='capacity'>Capacità</div>");
        //}, 10);
    };

    this.loadData = function(url) {
	    var that = this;
        that.n_active_operations = that.n_active_operations + 1;
        $(that.ph).trigger($.Event('loading',{}));
		$.ajax({
			url: url,
			method: 'GET',
		    dataType: 'json',
		    success: function(json) {
		        that.onDataReceived(json, url);
                that.n_active_operations = that.n_active_operations - 1;
		        if (that.n_active_operations === 0) {
                    $(that.ph).trigger($.Event('loaded',{}));
                }
                $(that.ph).siblings(".updating").hide();
		    },
		});
    };

    this.data_not_available = function() {
        $(this.ph).html(data_not_available_str);
    };
    
    this.init = function(placeholder, url, slots) {
        this.slots = slots;
        this.ph = placeholder;
        this.loadData(url);
    };
	this.init(placeholder, url, slots);
	this.plot;
}


setInterval( function() {
    $('.carpark').trigger('reload', true);    
}, 300000 );
setTimeout( function() { 
    $('.carpark').trigger('reload', true);
}, Math.floor((Math.random()*10)+1)*250);



