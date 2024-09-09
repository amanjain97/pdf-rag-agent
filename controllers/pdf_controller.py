import os

from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from flask_pydantic import validate

from models.pdf_model import PDFModel, QuestionsModel
from utils.file_utils import allowed_file, is_valid_pdf

pdf_apis = Blueprint('pdf', __name__)

@pdf_apis.post('/upload')
@validate(body=PDFModel)
def upload_pdf():
    try:
        data = request.json
        file_path = data['file_path']

        if not allowed_file(file_path):
            return jsonify({'error': 'Invalid file format'}), 400

        if os.path.exists(file_path):
            pdf_valid, error = is_valid_pdf(file_path)
            if not pdf_valid:
                return jsonify({'message': 'Invalid pdf file', 'error': error}), 400

            return jsonify({'message': 'File exists', 'file_path': file_path}), 200
        else:
            return jsonify({'error': 'File not found'}), 400

    except ValidationError as e:
        return jsonify({'error': str(e)}), 400

@pdf_apis.post('/ask')
@validate(body=QuestionsModel)
def ask_questions():
    try:
        data = request.get_json()
        questions = data.get('questions', [])

        answers = {}
        for question in questions:
            answers[question] = f"Answer to '{question}'"

        return jsonify(answers), 200

    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
