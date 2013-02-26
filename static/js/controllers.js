//'use strict';

/* Controllers */
function test_ex() {
	console.log("test");
}
$(document).ready(function() { 
	console.log("getMap()");
	var map = new OpenLayers.Map('testmap');
	var geoServerUrl="http://mapserver.tis.bz.it";
	//var geoServerUrl="http://95.171.54.201:8080";
	var extent = new OpenLayers.Bounds(11.272473793029,46.447363967896, 11.426969032287, 46.516028518678);
	var wmscURL = [
	      geoServerUrl+"/cgi-bin/mapserv?"
	];
	/*var wmscURL = [
	      geoServerUrl+"/geoserver/wms"
	];*/
	var center=  new OpenLayers.Geometry.Point(46.481696243287,11.349721412658);
	var filter_format = new OpenLayers.Format.Filter({version: "1.1.0"});
	var xmlFormatter = new OpenLayers.Format.XML();
	var filter= new OpenLayers.Filter.Spatial({
		type: OpenLayers.Filter.Spatial.DWITHIN,
		property:'the_geom',
		value:center,
		distance:5000
	});
	var options={
			minResolution: 0.00000291534423828125,
			maxResolution: 0.00200291534423828125,
			buffer: 0, 
	        opacity: 1, 
	        isBaseLayer: true, 
	        visibility: true, 
	        singleTile: true 
		};
	var traffic = new OpenLayers.Layer.WMS( 'Südtirol',wmscURL, {
		layers: ['elgis:parkingarea'], 
		//map: "relay2.map",
		format: 'image/png',
		exceptions:'application-vnd.ogc.se_inimage'	
	},options);
	
	var st = new OpenLayers.Layer.WMS( 'Südtirol',wmscURL, {
		layers: ['elgis:l09'],
		//filter:xmlFormatter.write(filter_format.write(filter)), TODO fix this filter so that it works
		format: 'image/png',
		//map: "relay2.map",
		//exceptions:'test_ex'	
		exceptions:'application-vnd.ogc.se_inimage'	
	},{
		minResolution: 0.00000291534423828125,
		maxResolution: 0.00200291534423828125,
		buffer: 0, 
        opacity:0.2, 
        isBaseLayer: false, 
        visibility: true, 
        singleTile: true 
	});
	
	map.addLayer(st);
	map.addLayer(traffic);
	map.zoomToExtent(extent);
	st.events.on({
		 moveend: function(e) {
           if (e.zoomChanged) {
   			   self.box=map.getExtent();
               OpenLayers.Event.stop(e);
           }
        }
		
    });
});

