{% extends "gis/admin/openlayers.js" %}
{% block base_layer %}
  new OpenLayers.Layer.OSM(
    "OpenCycleMap",
    [
      "http://a.tile.opencyclemap.org/cycle/${z}/${x}/${y}.png",
      "http://b.tile.opencyclemap.org/cycle/${z}/${x}/${y}.png",
      "http://c.tile.opencyclemap.org/cycle/${z}/${x}/${y}.png",
    ]
  );
{% endblock %}
