from .core import PyHades

class PyHadesContext(object):
    r"""
    When you need run threads with PyHades with a web framework, where these frameworks have a main thread, the PyHades app
    must run with a context to avoid lock the main app with the main thread.
    
    Usage

    ```python
    >>> from flask import Flask
    >>> from pyhades import PyHades, PyHadesContext, State, PyHadesStateMachine

    >>> flask_app = Flask(__name__)
    >>> hades_app = PyHades()
    >>> @hades_app.define_machine(name='TrafficLight', interval=1.0, mode="async")
        class TrafficLightMachine(PyHadesStateMachine):

        # states
        ...

    
    >>> if __name__ == "__main__":

    >>> with PyHadesContext(hades_app):
        
            flask_app.run()
    ```
    """

    def __init__(self, app):

        if isinstance(app, PyHades):
            self.app = app

    def __enter__(self):
        self.app.safe_start()
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.app.safe_stop()
