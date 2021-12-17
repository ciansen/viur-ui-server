import flask
from routes import default
from flask_cors import CORS
import viur

if __name__ == "__main__":
	app = flask.Flask(__name__)
	app.register_blueprint(default)
	CORS(app)

	for k, v in viur.ViurCommandManager().items():
		build_params = "".join([f"<{arg}>/" for arg in v.args])
		app.add_url_rule(f"/{k}/{build_params}", None, v, methods=["GET", "POST"])


	app.run(debug=True, host="127.0.0.1", port=9001)