import streamlit as st
import requests
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

credentials = Credentials(
    url = "https://us-south.ml.cloud.ibm.com",
    api_key = "my-api-key")

client = APIClient(credentials)

model = ModelInference(
  model_id="meta-llama/llama-3-405b-instruct",
  api_client=client,
  space_id="my-space-id",
  params = {
      "max_new_tokens": 100
  }
)

# Set up Streamlit page
st.title("Chat App with watsonx.ai")

# Chat interface
st.write("Chat with watsonx.ai")

# User input
user_input = st.text_input("You:", key="user_input")
print(user_input)

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []


# Handle user input and display chat history
if st.button("Send") and user_input:
    # Display user input
    st.session_state["chat_history"].append(("User", user_input))
    
    # Generate response
    full_prompt = "\n".join([f"{role}: {message}" for role, message in st.session_state["chat_history"]])
    response = model.generate_text(full_prompt)
    st.session_state["chat_history"].append(("Model", response))

# Display chat history
for role, message in st.session_state["chat_history"]:
    if role == "User":
        st.write(f"**You:** {message}")
    else:
        st.write(f"**Model:** {message}")
