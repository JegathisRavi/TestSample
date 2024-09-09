# from transformers import GPT2LMHeadModel, GPT2Tokenizer
# import torch

# # Load pre-trained model and tokenizer
# model_name = "gpt2-medium"
# model = GPT2LMHeadModel.from_pretrained(model_name)
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# # Function to generate text
# def generate_text(prompt, max_length):
#     # Encode the input text
#     input_ids = tokenizer.encode(prompt, return_tensors='pt')
    
#     # Generate text with adjusted parameters
#     with torch.no_grad():
#         output = model.generate(
#             input_ids,
#             max_length=max_length,
#             num_return_sequences=1,
#             temperature=1,  # Lower temperature for more coherent text
#             top_k=50,         # Use top_k sampling to limit choices
#             top_p=0.9,        # Use nucleus sampling for diversity
#             pad_token_id=tokenizer.eos_token_id  # Ensure proper padding
#         )
    
#     # Decode and return the output
#     return tokenizer.decode(output[0], skip_special_tokens=True)

# # Example usage
# prompt = "Please Correct the grammar of the following sentence: 'Jack not is bad'"
# generated_text = generate_text(prompt, max_length=100)
# print(generated_text)

# import torch
# from transformers import GPT2LMHeadModel, GPT2Tokenizer

# # Check for GPU availability
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# print(f'Using device: {device}')

# # Load pre-trained model and tokenizer
# model_name = 'gpt2-medium'
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)
# model = GPT2LMHeadModel.from_pretrained(model_name).to(device)

# # Define input text with an explicit rephrasing prompt
# input_text = "Explain what is IFU in a electronic device ?"

# # Tokenize input text
# input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)

# # Generate text
# with torch.no_grad():
#     output = model.generate(input_ids, max_length=100, num_return_sequences=1, 
#                             no_repeat_ngram_size=3, temperature=0.9)

# # Decode output
# generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

# print("Rephrased text:")
# print(generated_text)

# import torch
# from transformers import GPT2LMHeadModel, GPT2Tokenizer

# # Check for GPU availability
# device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# print(f'Using device: {device}')

# # Load pre-trained model and tokenizer
# model_name = 'gpt2-medium'
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)
# model = GPT2LMHeadModel.from_pretrained(model_name).to(device)

# def generate_answer(question):
#     # Create prompt
#     prompt = f"Question: {question}\nAnswer:"

#     # Tokenize input text
#     input_ids = tokenizer.encode(prompt, return_tensors='pt').to(device)

#     # Generate text
#     with torch.no_grad():
#         output = model.generate(
#             input_ids, 
#             max_length=100, 
#             num_return_sequences=1, 
#             no_repeat_ngram_size=2, 
#             temperature=0.7,
#             pad_token_id=tokenizer.eos_token_id
#         )

#     # Decode output
#     generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    
#     # Extract answer from the generated text
#     answer = generated_text[len(prompt):].strip()
#     return answer

# # Example questions
# questions = [
#     "What is Data science?",
#     "Correct the following sentence : 'Jack not is good' "
# ]

# for question in questions:
#     answer = generate_answer(question)
#     print(f"Q: {question}\nA: {answer}\n")




import streamlit as st
import msal
import os
import requests

# Configuration
client_id = st.secrets["CLIENT_ID"]
client_secret = st.secrets["CLIENT_SECRET"]
tenant_id = st.secrets["TENANT_ID"]
redirect_uri = st.secrets["URL"]

# Initialize MSAL
authority = f"https://login.microsoftonline.com/{tenant_id}"
app = msal.ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret,
)

# Streamlit App
st.title("Azure Authentication Example")

# Handling the callback
auth_code = st.experimental_get_query_params().get("code")
if auth_code:
    # Exchange the authorization code for an access token
    token_response = app.acquire_token_by_authorization_code(
        auth_code,
        scopes=["Files.ReadWrite.All", "Sites.Read.All", "User.Read"],
        redirect_uri=redirect_uri
    )

    if "access_token" in token_response:
        st.write("Authentication successful!")
        st.session_state["access_token"] = token_response["access_token"]
        # Use the token to access resources
        user_info = requests.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={"Authorization": f"Bearer {st.session_state['access_token']}"}
        ).json()
        st.write("User Info:", user_info)
    else:
        st.write("Authentication failed.")
else:
    st.write("Not authenticated.")
    # Generate the authorization URL
    auth_url = app.get_authorization_request_url(
        scopes=["Files.ReadWrite.All", "Sites.Read.All", "User.Read"],
        redirect_uri=redirect_uri
    )
    st.write(f"[Login]({auth_url})")
