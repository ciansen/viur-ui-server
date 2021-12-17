from .bp import default
from shutil import which
from flask import jsonify
import subprocess
import time

@default.route("/viur")
def viur():
	has_viur = which("viur") is not None
	return jsonify({
		"state": has_viur,
		"version": subprocess.check_output(["viur", "--version"]) if has_viur else ""
	})

@default.route("/project")
def index():
	return "hello"


