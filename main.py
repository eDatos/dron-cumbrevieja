import itertools
import shutil

import logzero
import typer

import settings
from dcv import core, utils

app = typer.Typer(add_completion=False)
logger = utils.init_logger()


@app.command()
def run(
    verbose: bool = typer.Option(
        False, '--verbose', '-v', show_default=False, help='Loglevel increased to debug'
    ),
    clean: bool = typer.Option(
        False,
        '--clean',
        '-x',
        show_default=False,
        help='Remove download folder after execution',
    ),
    max_layers: int = typer.Option(
        100,
        '--max-layers',
        '-m',
        help='Maximum number of layers to be retrieved',
    ),
    ignore_checked_layers: bool = typer.Option(
        False,
        '--ignore-checked',
        '-i',
        show_default=False,
        help='Ignore checked layers. Process everything.',
    ),
    notify: bool = typer.Option(
        False, '--notify', '-n', show_default=False, help='Notify shapefile via email'
    ),
):
    logger.setLevel(logzero.DEBUG if verbose else logzero.INFO)
    try:
        feature_layers = core.FeatureLayers(ignore_checked_layers=ignore_checked_layers)
        layers = feature_layers.get_unchecked_layers()
        for layer in itertools.islice(layers, 0, max_layers):
            layer.download_shapefile()
            layer.mark_as_checked()
            if notify:
                layer.notify()
    except Exception as err:
        logger.error(str(err).strip())
    finally:
        logger.debug('Quiting webdriver handler')
        core.webdriver.quit()
        logger.debug('Quiting SMTP handler')
        core.smtp.quit()
        if clean:
            logger.debug('Cleaning downloads directory')
            shutil.rmtree(settings.DOWNLOADS_DIR, ignore_errors=True)


if __name__ == "__main__":
    app()
