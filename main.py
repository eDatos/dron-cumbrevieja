from dcv import core, utils

try:
    utils.prepare_downloads_dir()
    feature_layers = core.FeatureLayers()
    for layer in feature_layers.get_unchecked_layers():
        layer.download_shapefile()
        layer.mark_as_checked()
except Exception as err:
    print(err)
finally:
    core.webdriver.quit()
