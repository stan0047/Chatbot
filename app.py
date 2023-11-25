import streamlit as st
import replicate
from dotenv import load_dotenv
load_dotenv()
import os
from utils import debounce_replicate_run
from auth0_component import login_button

###Global variables:###
REPLICATE_API_TOKEN = 'r8_4tgQs4SecdiRBaSMGuPMb5zvtHtSnjk4WLFc8'
#Your your (Replicate) models' endpoints:
REPLICATE_MODEL_ENDPOINT7B = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
REPLICATE_MODEL_ENDPOINT13B = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
REPLICATE_MODEL_ENDPOINT70B = 'replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'
PRE_PROMPT = "sorry!! app getting to expensive to maintain."
#Auth0 for auth
AUTH0_CLIENTID = 'Laq7kpTIcHAJXk0XyYCu9kHFk90PqaYa'
AUTH0_DOMAIN = 'dev-tygbdbmgfduqxmi6.us.auth0.com'

if not (REPLICATE_API_TOKEN and REPLICATE_MODEL_ENDPOINT13B and REPLICATE_MODEL_ENDPOINT7B and 
        AUTH0_CLIENTID and AUTH0_DOMAIN):
    st.warning("Add a `.env` file to your app directory with the keys specified in `.env_template` to continue.")
    st.stop()

###Initial UI configuration:###
st.set_page_config(page_title="ALICE Chat(sorry!! app getting to expensive to maintain)", page_icon="🦙", layout="wide")

def render_app():

    # reduce font sizes for input text boxes
    custom_css = """
        <style>
            .stTextArea textarea {font-size: 13px;}
            div[data-baseweb="select"] > div {font-size: 13px !important;}
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    #Left sidebar menu
    st.sidebar.header("Alice Chat")

    #Set config for a cleaner menu, footer & background:
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    #container for the chat history
    response_container = st.container()
    #container for the user's text input
    container = st.container()
    #Set up/Initialize Session State variables:
    if 'chat_dialogue' not in st.session_state:
        st.session_state['chat_dialogue'] = []
    if 'llm' not in st.session_state:
        #st.session_state['llm'] = REPLICATE_MODEL_ENDPOINT13B
        st.session_state['llm'] = REPLICATE_MODEL_ENDPOINT70B
    if 'temperature' not in st.session_state:
        st.session_state['temperature'] = 0.1
    if 'top_p' not in st.session_state:
        st.session_state['top_p'] = 0.9
    if 'max_seq_len' not in st.session_state:
        st.session_state['max_seq_len'] = 512
    if 'pre_prompt' not in st.session_state:
        st.session_state['pre_prompt'] = PRE_PROMPT
    if 'string_dialogue' not in st.session_state:
        st.session_state['string_dialogue'] = ''

    #Dropdown menu to select the model edpoint:
    selected_option = st.sidebar.selectbox('Choose a Alice model:', ['Alice-70B', 'Alice-13B', 'Alice-7B'], key='model')
    if selected_option == 'Alice-7B':
        st.session_state['llm'] = REPLICATE_MODEL_ENDPOINT7B
    elif selected_option == 'Alice-13B':
        st.session_state['llm'] = REPLICATE_MODEL_ENDPOINT13B
    else:
        st.session_state['llm'] = REPLICATE_MODEL_ENDPOINT70B
    #Model hyper parameters:
    st.session_state['temperature'] = st.sidebar.slider('Temperature:', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    st.session_state['top_p'] = st.sidebar.slider('Top P:', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    st.session_state['max_seq_len'] = st.sidebar.slider('Max Sequence Length:', min_value=64, max_value=4096, value=2048, step=8)

    NEW_P = st.sidebar.text_area('Prompt before the chat starts. Edit here if desired:', PRE_PROMPT, height=60)
    if NEW_P != PRE_PROMPT and NEW_P != "" and NEW_P != None:
        st.session_state['pre_prompt'] = NEW_P + "\n\n"
    else:
        st.session_state['pre_prompt'] = PRE_PROMPT

    btn_col1, btn_col2 = st.sidebar.columns(2)

    # Add the "Clear Chat History" button to the sidebar
    def clear_history():
        st.session_state['chat_dialogue'] = []
    clear_chat_history_button = btn_col1.button("Clear History",
                                            use_container_width=True,
                                            on_click=clear_history)

    # add logout button
    def logout():
        del st.session_state['user_info']
    logout_button = btn_col2.button("Logout",
                                use_container_width=True,
                                on_click=logout)
        
    # add links to relevant resources for users to select
    st.sidebar.write(" ")

    text1 = 'Chatbot Demo Code' 
    text2 = 'Alice 70B Model on Replicate' 
    text3 = 'Alice Cog Template'

    text1_link = "https://github.com/a16z-infra/llama2-chatbot"
    text2_link = "https://replicate.com/replicate/llama70b-v2-chat"
    text3_link = "https://github.com/a16z-infra/cog-llama-template"

    logo1 = 'https://storage.googleapis.com/llama2_release/a16z_logo.png'
    logo2 = 'https://storage.googleapis.com/llama2_release/Screen%20Shot%202023-07-21%20at%2012.34.05%20PM.png'

    st.sidebar.markdown(
        "**Resources**  \n"
        f"<img src='{logo2}' style='height: 1em'> [{text2}]({text2_link})  \n"
        f"<img src='{logo1}' style='height: 1em'> [{text1}]({text1_link})  \n"
        f"<img src='{logo1}' style='height: 1em'> [{text3}]({text3_link})",
        unsafe_allow_html=True)

    st.sidebar.write(" ")
    st.sidebar.markdown("*Made with ❤️ by Ayush Kadam.*")

    # Display chat messages from history on app rerun
    for message in st.session_state.chat_dialogue:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Type your question here to talk to Alice((App down,sorry!! app getting to expensive to maintain)"):
        # Add user message to chat history
        st.session_state.chat_dialogue.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            string_dialogue = st.session_state['pre_prompt']
            for dict_message in st.session_state.chat_dialogue:
                if dict_message["role"] == "user":
                    string_dialogue = string_dialogue + "User: " + dict_message["content"] + "\n\n"
                else:
                    string_dialogue = string_dialogue + "Assistant: " + dict_message["content"] + "\n\n"
            print (string_dialogue)
            output = debounce_replicate_run(st.session_state['llm'], string_dialogue + "Assistant: ",  st.session_state['max_seq_len'], st.session_state['temperature'], st.session_state['top_p'], REPLICATE_API_TOKEN)
            for item in output:
                full_response += item
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        # Add assistant response to chat history
        st.session_state.chat_dialogue.append({"role": "assistant", "content": full_response})


if 'user_info' in st.session_state:
# if user_info:
    render_app()
else:
    st.write("Please login to use the app. This is just to prevent abuse, we're not charging for usage.sorry!! app getting to expensive to maintain")
    st.session_state['user_info'] = login_button(AUTH0_CLIENTID, domain = AUTH0_DOMAIN)