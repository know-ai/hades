from .core import PyHades
import logging
import sys

class PyHadesContext(object):
    r"""
    Documentation here
    """

    def __init__(self, app):

        if isinstance(app, PyHades):
            self.app = app

    def __enter__(self):
        self.app.run_in_context()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.app._stop_threads()
        self.app._stop_workers()
        logging.info("Manual Shutting down")
        sys.exit()