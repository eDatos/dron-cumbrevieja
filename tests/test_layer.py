def test_layer_time_is_extracted(feature_layer):
    feature_layer.extract_layer_time()
    assert feature_layer.layer_time == '13:00'


def test_shapefile_is_downloaded(feature_layer):
    feature_layer.download_shapefile()
    assert feature_layer.layer_file.exists()
