import streamlit as st
from utils.functions import send_user_query

st.title("KALEX 🤖")
st.write("Generative AI Chatbot")
st.divider()

if "message_history" not in st.session_state:
  st.session_state["message_history"] =[]
else:
  for msg in st.session_state["message_history"]:
    #print(msg)
    if msg["role"] == "assistant" and "user_feedback" in msg.keys():
      st.chat_message(msg["role"]).write(msg["content"])
    else:
      st.chat_message(msg["role"]).write(msg["content"])

if user_query:= st.chat_input():
  human_message_object = {"role":"user", "content":user_query}
  st.session_state["message_history"].append(human_message_object)
  st.chat_message("user").write(user_query)
  
  kalex_response = send_user_query(user_query)
  st.chat_message("assistant").write(kalex_response)
  kalex_message_object = {"role":"assistant", "content":kalex_response}
  st.session_state["message_history"].append(kalex_message_object)
