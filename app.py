from flask import Flask, jsonify
from dotenv import load_dotenv

from controllers.pdf_controller import pdf_apis

load_dotenv()

app = Flask(__name__)
app.register_blueprint(pdf_apis, url_prefix="/v1")


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(port=8000)
