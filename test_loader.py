from rag.document_loader import load_pdf

docs = load_pdf(
    "knowledge_base/company_profile.pdf"
)

print("Total extracted pages: ",len(docs))

for doc in docs:
    print("Text: ",doc["text"])
    print("source: ",doc["metadata"]["source"])
    print("Page:", doc["metadata"]["page"])