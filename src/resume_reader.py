from pypdf import PdfReader
import docx
import io

def extract_text_from_file(uploaded_file):
    """
    Kisi bhi format (.txt, .pdf, .docx) se text nikalta hai.
    """
    filename = uploaded_file.name.lower()
    
    if filename.endswith('.txt'):
        return uploaded_file.read().decode('utf-8')
    
    elif filename.endswith('.pdf'):
        reader = PdfReader(io.BytesIO(uploaded_file.read()))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    elif filename.endswith('.docx'):
        doc = docx.Document(io.BytesIO(uploaded_file.read()))
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    
    else:
        raise ValueError("Unsupported file format")