import os
import json
import time
import requests
import structlog

from flask import Blueprint, request, jsonify
from flask_pydantic import validate
from langchain_community.document_loaders import PyPDFLoader
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter

from models.pdf_model import PDFModel, QuestionsModel
from utils.file_utils import allowed_file, is_valid_pdf
from config.config import TEXT_SPLITTER, SUCCESS_STATUS, FAILED_STATUS, EM_ENCODE_KWARGS, EM_MODEL_KWARGS, EM_MODEL_NAME
from templates.template import template

pdf_apis = Blueprint('pdf', __name__)

logger = structlog.getLogger()

@pdf_apis.post('/upload')
@validate(body=PDFModel)
def upload_pdf():
    try:
        data = request.json
        file_path = data['file_path']

        if not allowed_file(file_path):
            return jsonify({'error': 'Invalid file format', 'status': FAILED_STATUS}), 400

        if os.path.exists(file_path):
            pdf_valid, error = is_valid_pdf(file_path)
            if not pdf_valid:
                return jsonify({'message': 'Invalid pdf file', 'error': error, 'status': FAILED_STATUS}), 400
        else:
            return jsonify({'error': 'File not found', 'status': FAILED_STATUS}), 400

        loader = PyPDFLoader(file_path)
        data = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=TEXT_SPLITTER['chunk_size'], chunk_overlap=TEXT_SPLITTER['chunk_overlap'])
        documents = text_splitter.split_documents(data)
        logger.info(documents[1])
        logger.info(f"Number of Chunks: {len(documents)}")
        
        file_name = file_path.split("/")[-1]

        embeddings = HuggingFaceEmbeddings(model_name=EM_MODEL_NAME, model_kwargs=EM_MODEL_KWARGS, encode_kwargs=EM_ENCODE_KWARGS)
        vectorstore = FAISS.from_documents(documents, embeddings)
        vectorstore.save_local("faiss_index_constitution")

        return jsonify({"filename": file_name, "status": SUCCESS_STATUS})

    except Exception as e:
        return jsonify({'error': str(e), 'status': FAILED_STATUS}), 400

@pdf_apis.post('/ask')
@validate(body=QuestionsModel)
def ask_questions():
    try:
        data = request.get_json()
        questions = data.get('questions', [])

        prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=template,
        )
        answers = {}
        embeddings = HuggingFaceEmbeddings(model_name=EM_MODEL_NAME, model_kwargs=EM_MODEL_KWARGS, encode_kwargs=EM_ENCODE_KWARGS)
        persisted_vectorstore = FAISS.load_local("faiss_index_constitution", embeddings, allow_dangerous_deserialization=True)
        for question in questions:
            relevant_docs = persisted_vectorstore.similarity_search(query=question, fetch_k=1)
            logger.info(f"======{relevant_docs}")
            context = relevant_docs[0].page_content
            filled_prompt = prompt.format(question=question, context=context)
            
            request_payload = {
                "model": "llama2",
                "prompt": filled_prompt,
                "format": "json"
            }
            answers[question] = get_answer(request_payload)
        return jsonify(answers), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

def get_answer(request_payload):
    try:
        response = requests.post("http://localhost:11434/api/generate", json=request_payload, timeout=60.0)

        def stream_response_generator():
            response_str = ""
            for chunk in response.iter_lines():
                logger.info(f"Received chunk: {chunk}")
                json_data = json.loads(chunk)
                response_str += json_data['response'] + " "
                time.sleep(1) 
            return response_str
        return stream_response_generator()
    except Exception as e:
        return "could not find the answer!"
