# Alice Chatbot App ⚡

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/stan0047/Chatbot)
[![Open app(stopped the service as maintaing was really expensive)](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://chatbot-chmyu8ujttvhyvfzjsmrrg.streamlit.app/)


⚡⚡!!!!  I had to halt the project due to the high costs associated with its deployment.  !!!⚡⚡

## 🤔 What is this?

This is an experimental Streamlit chatbot app built for LLaMA2 (or any other LLM). The app includes session chat history and provides an option to select multiple LLaMA2 API endpoints on Replicate.

<img width="1710" alt="llama2 demo" src="Pics/Screenshot 2023-11-25 180703.png">
<img width="710" alt="llama2 demo" src="Pics/Screenshot 2023-11-25 181841.png">
<img width="1710" alt="llama2 demo" src="Pics/255374554-7512cbd3-ef90-4a9f-b9f6-eab5be7a483f.png">

## Features

- Chat history is maintained for each session (if you refresh, chat history clears)
- Option to select between different LLaMA2 chat API endpoints (7B, 13B or 70B). The default is 70B.
- Configure model hyperparameters from the sidebar (Temperature, Top P, Max Sequence Length).
- Includes "User:" and "Assistant:" prompts for the chat conversation.
- Each model (7B, 13B & 70B) runs on Replicate - (7B and 13B run on one A100 40Gb, and 70B runs on one A100 80Gb).
- Docker image included to deploy this app in Fly.io


## Usage

- Start the chatbot by selecting an API endpoint from the sidebar.
- Configure model hyperparameters from the sidebar.
- Type your question in the input field at the bottom of the app and press enter.



## License

- Web chatbot license (this repo): Apache 2.0
- For the LLaMA models license, please refer to the License Agreement from Meta Platforms, Inc.

## Acknowledgements

- Special thanks to the team at Meta AI, Replicate, a16z-infra and the entire open-source community.

## Disclaimer

This is an experimental version of the app. Use at your own risk. While the app has been tested, the authors hold no liability for any kind of losses arising out of using this application. 

## UI Configuration

The app has been styled and configured for a cleaner look. Main menu and footer visibility have been hidden. Feel free to modify this to your custom application.

## Resources

- [Streamlit Cheat Sheet](https://docs.streamlit.io/library/cheatsheet)
- [GitHub to deploy LLaMA2 on Replicate](https://github.com/a16z-infra/cog-llama-template)
