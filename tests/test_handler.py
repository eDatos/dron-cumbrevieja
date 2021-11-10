def test_feature_layers_are_available(layers_handler, max_layers_to_process):
    assert layers_handler.url is not None
    assert isinstance(layers_handler.layers, list)
    assert len(layers_handler.layers) >= max_layers_to_process


def test_downloads_dir_exists(layers_handler, downloads_dir):
    assert downloads_dir.exists()


def test_unchecked_layers_are_available(layers_handler, max_layers_to_process):
    unchecked_layers = layers_handler.get_unchecked_layers()
    assert len(unchecked_layers) == max_layers_to_process
