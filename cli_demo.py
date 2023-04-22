from configs.model_config import *
from chains.local_doc_qa import LocalDocQA
import os
import nltk
from models.loader.args import parser
import models.shared as shared
from models.loader import LoaderLLM
from models.chatglm_llm import ChatGLM

nltk.data.path = [os.path.join(os.path.dirname(__file__), "nltk_data")] + nltk.data.path

# return top-k text chunk from vector store
VECTOR_SEARCH_TOP_K = 6

# LLM input history length
LLM_HISTORY_LEN = 3

# Show reply with source text from input document
REPLY_WITH_SOURCE = True

if __name__ == "__main__":
    args = None
    args = parser.parse_args()
    args_dict = vars(args)

    shared.loaderLLM = LoaderLLM(args_dict)
    chatGLMLLM = ChatGLM(shared.loaderLLM)
    chatGLMLLM.history_len = LLM_HISTORY_LEN

    local_doc_qa = LocalDocQA()
    local_doc_qa.init_cfg(llm_model=chatGLMLLM,
                          embedding_model=EMBEDDING_MODEL,
                          embedding_device=EMBEDDING_DEVICE,
                          top_k=VECTOR_SEARCH_TOP_K)
    vs_path = None
    while not vs_path:
        filepath = input("Input your local knowledge file path 请输入本地知识文件路径：")
        vs_path, _ = local_doc_qa.init_knowledge_vector_store(filepath)
    history = []
    while True:
        query = input("Input your question 请输入问题：")
        resp, history = local_doc_qa.get_knowledge_based_answer(query=query,
                                                                vs_path=vs_path,
                                                                chat_history=history)
        if REPLY_WITH_SOURCE:
            print(resp)
        else:
            print(resp["result"])
