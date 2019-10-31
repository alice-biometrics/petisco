import connexion

from flask_cors import CORS

from petisco.frameworks.flask.application.json_encoder import JSONEncoder


class FlaskApplication:
    def __init__(self, application_name: str, swagger_dir: str, port: int = 8080):
        self.application_name = application_name
        self.app = connexion.App(__name__, specification_dir=swagger_dir)
        self.port = port
        self._configure()

    def _configure(self):
        CORS(self.app.app)
        self.app.app.json_encoder = JSONEncoder
        self.app.add_api("swagger.yaml", arguments={"title": self.application_name})

    def start(self):
        self.app.run(port=self.port)

    def get_config(self):
        return self.config

    def get_app(self):
        return self.app

    config = property(get_config)
