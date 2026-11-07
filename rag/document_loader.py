from pathlib import Path
import pymupdf

def load_pdf(pdf_path):

    pdf_path=Path(pdf_path)

    if not pdf_path.exists():
        raise FileNotFoundError(
            f"File not found: {pdf_path}"
        )

    documents=[]

    with pymupdf.open(pdf_path) as doc:
        for i,page in enumerate(doc):

            text = page.get_text()

            if not text.strip():
                continue

            document = {
                "text":text,
                "metadata":{
                    "source":pdf_path.name,
                    "page":i + 1
                }
            }

            documents.append(document)

    return documents
