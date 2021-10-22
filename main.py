from dcv import core

feature_layers = core.FeatureLayers()
for layer in feature_layers.get_unchecked_layers():
    print(layer.layer_url)
