import pymupdf
import os

script_dir = os.path.dirname(os.path.abspath(__file__))

file_name = "/Sample Knowledge Base.pdf"

abs_path = script_dir + file_name

pdf_doc = pymupdf.open(abs_path)

docs = []

for page in pdf_doc:
    single_page_docs = page.get_text().split('Group ')
    docs += [doc.strip() for doc in single_page_docs if doc.strip()]

    
print(len(docs))


