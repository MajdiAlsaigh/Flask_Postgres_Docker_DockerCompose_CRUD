from flask import jsonify, make_response


# Function to create a standardized response
def response(success=True, data=None, error=None, status_code=200):
    body = {"success": success}
    if success and data is not None:
        body["data"] = data
    elif not success:
        body["error"] = error or "Unknown error"
    return make_response(jsonify(body), status_code)

