import os
from src.downloader import Mangadex
from flask import Flask, request, jsonify, send_file

app = Flask(__name__)

@app.route("/")
def welcome():
	return jsonify(
		{
			"status": True,
		}
	)
	
@app.route("/download")
def download():
	id = request.args.get("id")
	if id == None:
		return jsonify(
		{
			"status": False,
			"reason": "please pass the id of the manga"
		}
	)
		
	if os.path.exists(os.path.join("tmp", f"{id}.pdf")):
		return send_file(os.path.join("tmp",f"{id}.pdf"), as_attachment=True)

	condition = Mangadex(id).fetch()
	if condition:
		return send_file(os.path.join("tmp",f"{id}.pdf"), as_attachment=True)
	else:
		return jsonify(
			{
				"status": False,
				"reason": "make sure the manga related to given id has more than 0 pages."
			}
		)

if __name__ == "__main__":
	app.run(debug=True)
