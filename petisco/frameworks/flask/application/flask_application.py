import connexion
import yaml
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
        self.app.add_api(
            self.config_file,
            arguments={"title": self.application_name},
            options={"serve_spec": False},
        )
        self.app.app.add_url_rule(
            rule=f"/{self.application_name}/openapi.json",
            view_func=self._openapi_json,
            endpoint=f"/{self.application_name}./{self.application_name}_openapi_json",
        )

    def start(self):
        self.app.run(port=self.port)

    def get_config(self):
        return self.config

    def get_app(self):
        return self.app

    def _openapi_json(self):
        openapi_yaml_path = f"{self.app.specification_dir}/{self.config_file}"

        with open(openapi_yaml_path) as openapi_yaml:
            openapi = yaml.safe_load(openapi_yaml)

        hidden_endpoints = []
        for path, methods in openapi["paths"].items():
            for method, endpoint in methods.items():
                print(f"{path} {method}")
                if endpoint.get("x-hidden"):
                    hidden_endpoints.append((path, method))

        for path, method in hidden_endpoints:
            del openapi["paths"][path][method]

        return openapi

    config = property(get_config)
