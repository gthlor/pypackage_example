import folium
import geopandas as gpd
from typing import Union


class FoliumMap(folium.Map):
    def __init__(self, center=(0, 0), zoom=2, **kwargs):
        super().__init__(location=center, zoom_start=zoom, **kwargs)

    def add_layer_control(self):
        """Enables layer control on the map."""
        folium.LayerControl().add_to(self)

    def add_vector(
        self,
        vector_data: Union[str, gpd.GeoDataFrame, dict],
        name="Vector Layer",
        zoom_to_layer=True,
    ):
        """
        Add vector data to the map. Supports file path, GeoDataFrame, or GeoJSON-like dict.

        Args:
            vector_data (Union[str, gpd.GeoDataFrame, dict]): file path, GeoDataFrame, or GeoJSON-like dict.
            name (str, optional): Set a layer name. Defaults to "Vector Layer".
            zoom_to_layer (bool, optional): Zoom to layer extantion. Defaults to True.

        Returns: None.
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

        # Load GeoJSON
        folium.GeoJson(data=geojson_data, name=name).add_to(self)
