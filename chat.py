import streamlit as st
from streamlit_chat import message
import openai
import os

from database import get_redis_connection
from chatbot import RetrievalAssistant, Message

# Initialise database

## Initialise Redis connection
redis_client = get_redis_connection()

# Set instruction
openai.api_key=st.secrets["OPENAI_API_KEY"]
# System prompt requiring Question and Year to be extracted from the user
system_prompt = '''
You are a helpful HVAC knowledge base assistant. You need to capture a Question and Model Number from each customer.
The Question is their query on HVAC products, and the Model Number is the model number for an applicable product.
If they haven't provided the model number, ask them for it again.
Once you have the model number, say "searching for answers".

Example 1:

User: I'd like the safety guidelines for installing a daikin room air conditioner

Assistant: Certainly, do you have a specific model number?

User: Sure, CTXG09QVJUW

Assistant: Searching for answers.
'''

### CHATBOT APP

st.set_page_config(
    page_title="Example Daikin Chatbot",
    page_icon=":robot:"
)

st.title('Gardiner Daikin Knowledge Base')
st.subheader("Let me help you with your Daikin Product")

if 'generated' not in st.session_state:
    st.session_state['generated'] = []

if 'past' not in st.session_state:
    st.session_state['past'] = []

def query(question):
    response = st.session_state['chat'].ask_assistant(question)
    return response

prompt = st.text_input(f"What do you want to know: ", key="input")

if st.button('Submit', key='generationSubmit'):
    OPENAI_API_KEY="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"
    
    # Initialization
    if 'chat' not in st.session_state:
        st.session_state['chat'] = RetrievalAssistant()
        messages = []
        system_message = Message('system',system_prompt)
        messages.append(system_message.message())
    else:
        messages = []


    user_message = Message('user',prompt)
    messages.append(user_message.message())

    response = query(messages)

    # Debugging step to print the whole response
    #st.write(response)

    st.session_state.past.append(prompt)
    st.session_state.generated.append(response['content'])

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
