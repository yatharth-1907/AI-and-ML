from langchain_community.document_loaders import PyPDFLoader

from pathlib import Path

loader = PyPDFLoader(str(Path(__file__).parent/'dl-curriculum.pdf'))
docs= loader.load()

print(len(docs))
print(docs[0].page_content) #give he content of the first page.
print()
print(docs[1].metadata)
