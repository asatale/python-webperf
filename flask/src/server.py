import multiprocessing
import gunicorn.app.base
from flask import Flask
from api.hello import hello_blueprint
from config import cfg


class App(Flask):
    def __init__(self, name='TestApp'):
        super().__init__(name)
        self.register_blueprint(hello_blueprint)


class Server(gunicorn.app.base.BaseApplication):

    def __init__(self, app: App, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


def main():
    def _num_workers():
        return (multiprocessing.cpu_count() * 2) + 1

    addr, port = cfg.addr.split(":")
    options = {
        'bind': '%s:%s' % (addr, port),
        'workers': _num_workers(),
        'threads': 2,
    }
    Server(App(), options).run()


if __name__ == '__main__':
    main()
