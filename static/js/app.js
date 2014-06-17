
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

$(document).on("click", ".forecast h3", function(e) {
    var ph = $(this).siblings('.graph')[0];
    var prediction_url = $(this).data("url");
    var chart = new plot(ph, prediction_url);
});

function plot (placeholder, url) {
    this.default_options = {
	    series: {
		    lines: {
			    show: false,
		    },
		    points: {
			    show: false
		    },
		    bars: {
		        show: true, barWidth: 0.6, fill: 1,  lineWidth:0
		    }
	    },
	    grid: {
			color: "#444444",
			/*	backgroundColor: "#DDDDDD",*/
			backgroundColor: {
				colors: ["#fff", "#e4f4f4"]
			},
			borderColor: "#FFFFFF",
			//tickColor: "#CCCCCC",
			//aboveData: false,
			//borderWidth: 1,
			clickable: true,
			hoverable: false,
			autoHighlight: true,
			/*markings: function(axes) {
				var markings = [];lea
				var xaxis = axes.xaxis;
				for (var x = Math.floor(xaxis.min); x < xaxis.max; x += xaxis.tickSize * 2) {
					markings.push({ xaxis: { from: x, to: x + xaxis.tickSize }, color: "rgba(232, 232, 255, 0.2)" });
				}
				return markings;
			}*/
		},
	    xaxis: {
		    tickDecimals: 0
	    },
	    yaxis: {
		    min: 0
	    },
	    selection: {
		    mode: "x"
	    },
	    legend: false,
	};

    this.data = [{
		    threshold: [{
				below: 21,
				color: "rgb(247,154,8)"
			}, {
				below: 19,
				color: "rgb(200, 20, 30)"
			}], color: "rgb(111,170,41)",
			data: []
	}];

    this.onDataReceived = function (json, url) {
        this.data[0].data = json;
        var plot = $.plot(this.ph, this.data, this.default_options);
    };

    this.loadData = function(url) {
        console.log(url);
	    var that = this;
        that.n_active_operations = that.n_active_operations + 1;
        $(that.placeholder).trigger($.Event('loading',{}));
		$.ajax({
			url: url,
			method: 'GET',
		    dataType: 'json',
		    success: function(json) {
		        that.onDataReceived(json, url)
                that.n_active_operations = that.n_active_operations - 1;
		        if (that.n_active_operations === 0) {
                    $(that.placeholder).trigger($.Event('loaded',{}));
                }
		    },
		});
	};

    this.init = function(placeholder, url) {
        this.ph = placeholder;
        this.loadData(url);
    };
	this.init(placeholder, url);
}
