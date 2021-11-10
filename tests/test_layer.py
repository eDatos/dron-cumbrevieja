def test_shapefile_is_downloaded(feature_layer):
    feature_layer.download_shapefile()
    assert feature_layer.layer_file.exists()
