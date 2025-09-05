"""Main module."""

import os
import ipyleaflet
import geopandas as gpd
from typing import Union


class LeafletMap(ipyleaflet.Map):
    def __init__(self, center=[20, 0], zoom=2, height="400px", **kwargs):
        super().__init__(center=center, zoom=zoom, **kwargs)
        self.layout.height = height
        self.scroll_wheel_zoom = True

    def add_basemap(self, basemap="OpenStreetMap"):
        basemaps = {
            "OpenStreetMap": ipyleaflet.basemaps.OpenStreetMap.Mapnik,
            "CartoDB Positron": ipyleaflet.basemaps.CartoDB.Positron,
            "CartoDB DarkMatter": ipyleaflet.basemaps.CartoDB.DarkMatter,
            "OpenTopoMap": ipyleaflet.basemaps.OpenTopoMap,
            "Esri WorldImagery": ipyleaflet.basemaps.Esri.WorldImagery,
        }
        if basemap in basemaps:
            tile_layer = ipyleaflet.TileLayer(
                url=basemaps[basemap]["url"],
                attribution=basemaps[basemap]["attribution"],
            )
            self.add_layer(tile_layer)
        else:
            raise ValueError(
                f"Basemap '{basemap}' not recognized. Available options: {list(basemaps.keys())}"
            )

    def add_basemap2(self, basemap="OpenTopoMap"):

        try:
            url = eval(f"ipyleaflet.basemaps.{basemap}").build_url()
        except:
            raise ValueError(
                f"Basemap '{basemap}' not recognized. Available options: {list(ipyleaflet.basemaps.keys())}"
            )

        layer = ipyleaflet.TileLayer(url=url, name=basemap)
        self.add(layer)

    def add_layer_control(self):
        layer_control = ipyleaflet.LayersControl(position="topright")
        self.add(layer_control)

    def add_vector(
        self,
        vector_data: Union[str, gpd.GeoDataFrame, dict],
        name="Vector Layer",
        zoom_to_layer=True,
        style=None,
        hover_style=None,
    ):
        """
        Add vector data to the map. Supports file path, GeoDataFrame, or GeoJSON-like dict.
        """

        if isinstance(vector_data, str):
            gdf = gpd.read_file(vector_data)
        elif isinstance(vector_data, gpd.GeoDataFrame):
            gdf = vector_data
        elif isinstance(vector_data, dict) and "features" in vector_data:
            gdf = gpd.GeoDataFrame.from_features(vector_data["features"])
        else:
            raise ValueError(
                "vector_data must be a filepath, GeoDataFrame or GeoJSON-like dict"
            )

        geojson_data = gdf.__geo_interface__

        # Zoom to layer
        if zoom_to_layer:
            minx, miny, maxx, maxy = gdf.total_bounds
            self.fit_bounds([[miny, minx], [maxy, maxx]])

        # Setting style and hover style
        if style is None:
            style = {"color": "blue", "fillOpacity": 0.4}

        if hover_style is None:
            hover_style = {"color": "red", "fillOpacity": 0.7}

        # Load GeoJSON
        geo_json = ipyleaflet.GeoJSON(
            data=geojson_data,
            name=name,
            style=style,
            hover_style=hover_style,
        )
        self.add(geo_json)
