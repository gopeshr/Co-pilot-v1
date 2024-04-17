# import os
# # from langchain_openai import ChatOpenAI, OpenAI
# from langchain.chains.combine_documents.stuff import StuffDocumentsChain
# from langchain.chains.llm import LLMChain
# from langchain_community.llms import HuggingFaceEndpoint
# from langchain.prompts import PromptTemplate
# from PyPDF2 import PdfReader
# from langchain.text_splitter import CharacterTextSplitter
# from vertexai.preview.generative_models import GenerativeModel
# from langchain_google_vertexai import VertexAI
# import tempfile
# import io
# from google.cloud import storage
# import os
# import logging
# # import openai

# # os.environ['OPENAI_API_KEY'] = "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"
# # os.environ['HUGGINGFACEHUB_API_TOKEN'] = "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"
# # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "lumen-b-ctl-047-e2aeb24b0ea0.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "sa-adapt-app-ai-services.json"


# # Authenticate with your GCP credentials
# client = storage.Client()
# bucket_name = 'Co-pilot-bot-bucket'
# bucket = client.get_bucket(bucket_name)
# # repo_id = 'mistralai/Mistral-7B-v0.1'
# # llm = HuggingFaceEndpoint(
# #     repo_id=repo_id, max_length=128, temperature=0.5
# # )
# # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
# llm = VertexAI(model_name="gemini-1.5-pro")
# # llm = OpenAI()

# prompt_template= """The following is a Business Requirement Document. Based on your understanding of the business requirement, generate a Mermaid JS flowchart. Let all the content of the components be enclosed within quotes and let the flowchart be concise:
# Text: "{text}"
# mermaid:"""
# # prompt_template= """Create a concise Mermaid JS flowchart aimed at creating an outline of your understanding of the following content. Let all the content of the components be enclosed within quotes and let the flowchart be concise:
# # Text: "{text}"
# # mermaid:"""

# prompt = PromptTemplate.from_template(prompt_template)

# def read_file():
#     blobs = bucket.list_blobs()
#     # Sort the blobs by their updated time
#     sorted_blobs = sorted(blobs, key=lambda x: x.updated, reverse=True)
#     num_files_to_get = 5  # Change this number as needed
#     latest_files = sorted_blobs[:num_files_to_get]
#     logging.warning(latest_files[0].name)
#     print(latest_files[0].name)
#     return latest_files[0].name

# class Document:
#     def __init__(self, page_content, metadata):
#         self.page_content = page_content
#         self.metadata = metadata
#     def __str__(self):
#         return f"Document (page_content='{self.page_content}', metadata={self.metadata})"
#     def __repr__(self):
#         return self.__str__()

# def summarize_pdf():
#     pdf_file = read_file()
#     blob = bucket.blob(pdf_file)
#     content = blob.download_as_string()
#     data = io.BytesIO(content)
#     document=[]
#     pdfreader = PdfReader (data)
#     raw_text =""
#     for i, page in enumerate(pdfreader.pages):
#         content = page.extract_text()
#         if content:
#             raw_text += content
#             text_splitter = CharacterTextSplitter(
#             separator="In", chunk_size=800, chunk_overlap=200, length_function=len,
#             )
#     texts = text_splitter.split_text(raw_text)
#     #print(texts)
#     document=Document(page_content=texts[0],metadata={})
#     #print(document)
#     llm_chain = LLMChain(llm=llm, prompt=prompt)
#     stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
#     summary = stuff_chain.run([document])
#     return summary

# def solution_architecture():
#         mermaid_code = summarize_pdf()
#         return mermaid_code

