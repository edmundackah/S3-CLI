import os

from flask import Flask, jsonify, make_response, request, send_file, abort

app = Flask(__name__)

# Directory for storing the .tgz file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TGZ_FILE_PATH = os.path.join(BASE_DIR, "package.tgz")

# Helper function for a 500 response
def internal_server_error(endpoint):
    response = {
        "timestamp": "2024-03-26T11:00:00Z",
        "status": 500,
        "error": "Internal Server Error",
        "message": f"An unexpected error occurred at endpoint {endpoint}",
        "path": request.path
    }
    return make_response(jsonify(response), 500)


@app.route('/artifactory/<application>/-/<version>/<filename>', methods=['GET', 'HEAD'])
def serve_file(application, version, filename):
    try:
        print(f"looking for file path: {BASE_DIR}/")

        if request.method == 'HEAD':
            # Check if the file exists without sending it
            with open(f"{BASE_DIR}/{filename}.tgz", 'rb'):
                return '', 200
        # Serve the file for GET requests
        return send_file(
            f"{BASE_DIR}/{filename}",
            as_attachment=True,
            download_name=filename,
            mimetype="application/gzip"
        )
    except FileNotFoundError:
        abort(404, description="File not found")
    except Exception as e:
        print(e)
        abort(500, description=str(e))


@app.route("/download/tgz", methods=["GET"])
def download_tgz():
    try:
        # Check if the file exists
        if not os.path.exists(TGZ_FILE_PATH):
            return make_response(jsonify({"error": "File not found"}), 404)

        # Serve the file with correct headers
        return send_file(
            TGZ_FILE_PATH,
            as_attachment=True,
            download_name="release-test.tgz",
            mimetype="application/gzip"
        )
    except Exception as e:
        return make_response(jsonify({"error": "Internal server error", "message": str(e)}), 500)


# Stub: MCR Responses
@app.route("/change/HBO%20Change/<mcr_number>", methods=["GET"])
def mcr_response(mcr_number):
    if mcr_number == "MCR500000":
        return internal_server_error(f"/change/HBO%20Change/{mcr_number}")
    elif mcr_number == "MCR000000":
        response = {
            "valid": True,
            "number": mcr_number,
            "short_description": "Comm - Trans - Coutts Broker Portal 2nd positional release for business proving prior to go live",
            "assignment_group": {
                "link": "https://rbs.service-now.com/api/now/table/sys_user_group/7364734ebce1050b5f",
                "value": "7364734ebce1050b5f"
            },
            "description": "An aim of the Mortgage Transformation programme is to digitise our processes...",
            "state": "7",
            "start_date": "2024-03-26 11:00:00",
            "end_date": "2024-03-27 09:00:00",
            "invalid_reason": "N/A"
        }
        return make_response(jsonify(response), 200)
    else:
        response = {
            "status": 404,
            "error": "Not Found",
            "description": f"Couldn't find the change record with reference {mcr_number}"
        }
        return make_response(jsonify(response), 404)

# Stub: INC Responses
@app.route("/incident/<inc_number>", methods=["GET"])
def inc_response(inc_number):
    if inc_number == "INC500000":
        return internal_server_error(f"/incident/{inc_number}")
    elif inc_number == "INC700000":
        response = {
            "valid": False,
            "number": inc_number,
            "short_description": "Request CA00296640 out of agreed SLA",
            "assignment_group": {
                "link": "https://rbs.service-now.com/api/now/table/sys_user_group/4f9a5f930fa6d680dcc74ebce1050eb9",
                "value": "4f9a5f930fa6d680dcc74ebce1050eb9"
            },
            "description": "Request CA00296640 out of agreed SLA. This request has been chased via Ask Archie...",
            "state": "7",
            "invalid_reason": "N/A"
        }
        return make_response(jsonify(response), 200)
    elif inc_number == "INC000000":
        response = {
            "valid": True,
            "number": inc_number,
            "short_description": "Request CA00296640 out of agreed SLA",
            "assignment_group": {
                "link": "https://rbs.service-now.com/api/now/table/sys_user_group/4f9a5f930fa6d680dcc74ebce1050eb9",
                "value": "4f9a5f930fa6d680dcc74ebce1050eb9"
            },
            "description": "Request CA00296640 out of agreed SLA. This request has been chased via Ask Archie...",
            "state": "7",
            "invalid_reason": "N/A"
        }
        return make_response(jsonify(response), 200)
    else:
        response = {
            "status": 404,
            "error": "Not Found",
            "description": f"Couldn't find the incident record with reference {inc_number}"
        }
        return make_response(jsonify(response), 404)

if __name__ == "__main__":
    app.run(port=5000, debug=True)