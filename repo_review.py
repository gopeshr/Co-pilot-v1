# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# import git
# from langchain.prompts import PromptTemplate
# from langchain_community.document_loaders import Docx2txtLoader
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.chains.llm import LLMChain
# from langchain_google_vertexai import VertexAI
# from langchain.chains.combine_documents.stuff import StuffDocumentsChain
# from langchain.chains import StuffDocumentsChain, LLMChain
# from langchain.memory import ConversationSummaryBufferMemory, ConversationTokenBufferMemory, ConversationBufferMemory
# from docx import Document
# from langchain.chains.question_answering import load_qa_chain
# from langchain.text_splitter import CharacterTextSplitter
# # from fastapi import Websocket
# import os

# # os.environ['COHERE_API_KEY'] = "HnNAY4N9Q3kmCRY6pJOzOXUbtMUopHW03MLp55zp"
# # os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "sa-adapt-app-ai-services.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "lumen-b-ctl-047-e2aeb24b0ea0.json"

# prompt_template= """You are an programmer assistant. The following is a code written in python. Evaluate the code and give suggestions for improvement of the code. Be concise and on point. Answer in points.
#     Python code: {text}
#     Assistant:
#     """
# prompt = PromptTemplate.from_template(prompt_template)
# llm = VertexAI(model="gemini-1.5-pro", temperature=0.5, max_output_tokens=1024)
# llm_chain = LLMChain(llm=llm, prompt=prompt)
# stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")

# def summarize_pdf(pdf_file_path):
#     # llm = ChatCohere(model="command")
#     try:
#         loader = PyPDFLoader(pdf_file_path)
#         docs = loader.load()
#     except:
#         loader = Docx2txtLoader(pdf_file_path)
#         docs = loader.load()
#     # print(docs)
#     # print(docs)
#     text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     split_docs = text_splitter.split_documents(docs)
#     summary = stuff_chain.invoke(docs)
#     return summary['output_text'], split_docs
#     # return split_docs

# def git_extract(username, access_token, repo_name):
#     repo_url = f"https://{username}:{access_token}@github.com/{username}/{repo_name}"
#     try:
#         repo = git.Repo.clone_from(repo_url, repo_name)
#         print("Repository cloned successfully:", repo)
#     except git.exc.GitCommandError as e:
#         print("Cloning failed. Removing directory and trying again...")
#         try:
#             # Attempt to remove the directory
#             os.system(f'rm -rf {repo_name}')
#             # Clone the repository again
#             repo = git.Repo.clone_from(repo_url, repo_name)
#             print("Repository cloned successfully:", repo)
#         except git.exc.GitCommandError as e:
#             print("Failed to clone repository after removing directory.")

# def convert_to_docx(code_path, docx_path):
#     with open(code_path, 'r') as code_file:
#         code_content = code_file.read()
#     doc = Document()
#     doc.add_paragraph(code_content)
#     doc.save(docx_path)

# def list_files(repo_path):
#     files = []
#     for root, dirs, files_list in os.walk(repo_path):
#         for file in files_list:
#             file_path = os.path.join(root, file)
#             files.append(file_path)
#     return files

# async def select_file(username,access_token,repo_name, websocket: WebSocket):
#     # username = "gopeshr"
#     # access_token = "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"
#     # repo_name = "dummy01"
#     await websocket.accept()
#     git_extract(username, access_token, repo_name)
#     repo_path = os.path.join(repo_name)

#     await websocket.send_text("Available files in the repository:")
#     # print('Available files in the repository:')
#     file_paths = []
#     for root, dirs, files in os.walk(repo_path):
#         if '.git' in dirs:
#             dirs.remove('.git')  # Exclude .git folder from further traversal
#         for file_name in files:
#             full_path = os.path.join(root, file_name)
#             # print(f"- {file_name}")
#             await websocket.send_text(f"- {file_name}")
#             file_paths.append(full_path)
            
#     #         await websockets.send_text(f"- {file_name}")
#     await websocket.send_text("Enter the name of the file you want to chat with: ")
#     # print("Enter the name of the file you want to chat with: ")
#     # file_choice=input()
#     file_choice = await websocket.receive_text()
#     selected_file = next((file_path for file_path in file_paths if os.path.basename(file_path) == file_choice), None)

#     if selected_file:
#         return selected_file
#     else:
#         await websocket.send_text(f"File '{file_choice}' not found in the repository.")
#         # print(f"File '{file_choice}' not found in the repository.")
#         return None

# qa_template = """
# - You are a chatbot named Cody having a conversation with a human developer.
# - You NEVER answer that your are an AI language model.
# - If you don't have the context from the documents, answer from your knowledge with the context of the stuffed document.

# Given the following extracted parts of a long document and a question, create a final answer.

# {context}

# {chat_history}
# Human: {question}
# Chatbot:"""
# qa_prompt = PromptTemplate(
#     input_variables=["chat_history", "question", "context"], 
#     template=qa_template
# )

# memory = ConversationBufferMemory(memory_key='chat_history', input_key='question')
# chain = load_qa_chain(llm = llm, chain_type="stuff", prompt = qa_prompt, memory = memory)

# async def chat_with_git(username, access_token, repo_name, websocket: WebSocket):
#     await websocket.accept()
#     selected_file = select_file(username, access_token, repo_name)
#     if selected_file:
#         file_base_name = os.path.splitext(os.path.basename(selected_file))[0]

#         # Construct the new docx path
#         docx_path = f"docstore/doc_{file_base_name}.docx"
#         convert_to_docx(selected_file, docx_path)
#         summary, docs = summarize_pdf(docx_path)
#         await websocket.send_text("Do you want me to analyze and provide suggestions for improvements in your code? (Y/N)")
#         summary_nod = await websocket.receive_text()
#         if summary_nod.lower() == 'y':
#             await websocket.send_text(str(summary))
#         else:
#             pass
#         await websocket.send_text("You are currently chatting with: " + selected_file)
#         while True:
#             question = input("You: ")
#             if question == "quit":
#                 break
#             answer = chain.run(input_documents = docs, question = question)
#             await websocket.send_text(str(answer))
#     else:
#         await websocket.send_text("No file selected. Existing.")

# # chat_with_git()
# # chat_with_git("CenturyLink","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","
# # ")