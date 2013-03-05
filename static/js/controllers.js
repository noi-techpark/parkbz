//'use strict';

/* Controllers */
$(document).ready(function() { 
	var map = new OpenLayers.Map('testmap',{
		displayProjection: new OpenLayers.Projection("EPSG:900913"),
		projection: "EPSG:900913",
	});

	var geoServerUrl="http://mapserver.tis.bz.it";
	var wmscURL = [
	      geoServerUrl+"/cgi-bin/mapserv?"
	];

	var options={
		/*minResolution: 0.00000291534423828125,
		maxResolution: 0.00200291534423828125,*/
		opacity: 1, 
		isBaseLayer: false, 
		visibility: true, 
		singleTile: true,
	};
	
	var layer_parking = new OpenLayers.Layer.WMS( 'Südtirol',wmscURL, {
		layers: ['elgis:parkingarea'], 
		map: "relay_2.map",
		format: 'image/png',
		transparent: true,
		exceptions:'application-vnd.ogc.se_inimage'	
	}, options);

	// Test wms
	//var wms = new OpenLayers.Layer.WMS( "OpenLayers WMS",
    //            "http://vmap0.tiles.osgeo.org/wms/vmap0", {layers: 'basic'},{isBaseLayer: false, opacity:0.6});

	var fromProjection = new OpenLayers.Projection("EPSG:4326");   // Transform from WGS 1984
	var toProjection   = new OpenLayers.Projection("EPSG:900913"); // to Spherical Mercator Projection
	var layer_osm = new OpenLayers.Layer.OSM()

	var extent = new OpenLayers.Bounds(11.272473793029,46.447363967896, 11.426969032287, 46.516028518678);
	var center=  new OpenLayers.Geometry.Point(46.481696243287,11.349721412658);
	map.addLayer(layer_osm);
	map.addLayer(layer_parking);
	map.zoomToExtent(extent.transform( fromProjection, toProjection));
	map.setCenter(center);
});

