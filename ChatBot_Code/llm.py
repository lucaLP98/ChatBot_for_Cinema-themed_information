import streamlit as st
from langchain_cohere.chat_models import ChatCohere
from langchain_cohere import CohereEmbeddings
import os

os.environ["COHERE_API_KEY"] = "COHERE_API_KEY"

llm = ChatCohere()

cohere_embeddings = CohereEmbeddings(model="embed-english-v3.0")