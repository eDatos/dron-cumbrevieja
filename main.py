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
        False, '--verbose', '-v', show_default=False, help='Loglevel increased to debug.'
    ),
    clean: bool = typer.Option(
        False,
        '--clean',
        '-x',
        show_default=False,
        help='Remove download folder after execution.',
    ),
    max_layers: int = typer.Option(
        settings.MAX_LAYERS_TO_PROCESS,
        '--max-layers',
        '-m',
        help='Maximum number of layers to be processed.',
    ),
    ignore_checked_layers: bool = typer.Option(
        False,
        '--ignore-checked',
        '-i',
        show_default=False,
        help='Ignore checked layers. Process everything.',
    ),
    notify: bool = typer.Option(
        False, '--notify', '-n', show_default=False, help='Notify shapefile via email.'
    ),
):
    logger.setLevel(logzero.DEBUG if verbose else logzero.INFO)
    try:
        layers_handler = core.LayersHandler(
            ignore_checked_layers=ignore_checked_layers, max_layers_to_process=max_layers
        )
        layers = layers_handler.get_unchecked_layers()
        for layer in layers:
            if layer.download_shapefile():
                layer.mark_as_checked()
                if notify:
                    layer.notify()
            else:
                logger.error('Shapefile is not available')
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
