from dcv import core

# try:
feature_layers = core.FeatureLayers()
for i, layer in enumerate(feature_layers.get_unchecked_layers()):
    layer.download_shapefile()
# except Exception as err:
#     print(err)
# finally:
# core.webdriver.quit()
