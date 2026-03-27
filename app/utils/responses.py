from flask import jsonify


def success_response(data=None, message=None, status_code=200):
    payload = {}
    if message:
        payload["message"] = message
    if data is not None:
        payload["data"] = data
    return jsonify(payload), status_code


def error_response(message, status_code=400, code="error", details=None):
    payload = {
        "error": {
            "code": code,
            "message": message,
        }
    }
    if details is not None:
        payload["error"]["details"] = details
    return jsonify(payload), status_code
