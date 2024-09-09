from flask import Flask, jsonify

from controllers.pdf_controller import pdf_blueprint

app = Flask(__name__)
app.register_blueprint(pdf_blueprint, url_prefix="/pdf")

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(port=8000)
