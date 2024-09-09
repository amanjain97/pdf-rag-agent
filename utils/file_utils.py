import PyPDF2

ALLOWED_EXTENSIONS = ['pdf']

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_valid_pdf(filepath):
    try:
        with open(filepath, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            if reader.isEncrypted:
                return False, 'PDF is encrypted'
        return True, 'Valid PDF'
    except Exception as e:
        return False, str(e)
