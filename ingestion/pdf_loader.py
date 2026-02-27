import fitz  # PyMuPDF
from typing import List, Dict


def load_pdf(file_path: str) -> List[Dict]:
    """
    Extract text from a PDF file page by page.
    Returns structured content with metadata.
    """

    documents = []

    try:
        doc = fitz.open(file_path)

        for page_number in range(len(doc)):
            page = doc[page_number]
            text = page.get_text("text")

            if text.strip():  # avoid empty pages
                documents.append({
                    "content": text,
                    "metadata": {
                        "source": file_path,
                        "page": page_number + 1,
                        "type": "pdf"
                    }
                })

        doc.close()

    except Exception as e:
        raise RuntimeError(f"Error loading PDF: {str(e)}")

    return documents