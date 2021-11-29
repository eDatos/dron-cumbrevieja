def test_layer_time_is_extracted(feature_layer):
    assert feature_layer.layer_time == '13:00'


def test_layer_id(feature_layer):
    assert feature_layer.id == 'perimetro_dron_211108_1300'


def test_shapefile_is_downloaded(feature_layer):
    feature_layer.download_shapefile()
    assert feature_layer.layer_file.exists()
