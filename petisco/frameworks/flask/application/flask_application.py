import connexion
from flask_bcrypt import Bcrypt

from flask_cors import CORS

from petisco.frameworks.flask.application.json_encoder import JSONEncoder
from petisco.frameworks.interface_application import IApplication


class FlaskApplication(IApplication):
    def __init__(
        self,
        application_name: str,
        swagger_dir: str,
        config_file: str,
        port: int = 8080,
    ):
        self.application_name = application_name
        self.app = connexion.App(__name__, specification_dir=swagger_dir)
        self.config_file = config_file
        self.port = port
        self._configure()

    def _configure(self):
        CORS(self.app.app)
        self.app.app.config["BCRYPT_HANDLE_LONG_PASSWORDS"] = True
        self.bcrypt = Bcrypt(self.app.app)
        self.app.app.json_encoder = JSONEncoder
        self.app.add_api(self.config_file, arguments={"title": self.application_name})

    def start(self):
        self.app.run(port=self.port)

    def get_config(self):
        return self.config

    def get_app(self):
        return self.app

    config = property(get_config)
