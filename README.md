# ai-chatbot-demo

### Pre-Requisites
* Python 3.11 - https://www.python.org/downloads/release/python-3110/

### Instructions
**These instructions assume you're using VS Code**
* Open VS Code
* Open your project folder and clone down this repo `git clone https://github.com/vhmarquez/ai-chatbot-demo.git .`
* Open the "Show and Run Commands" panel (  **control + shift + p**  )
* Search for `Python: Select Interpreter`
* Select `Create Virtual Environment...`
* Select `Venv`
* Select `Python 3.11 64 bit`
* Select the `requirements.txt` file
* Duplicate the `.env copy` file and update it with the file posted in the `#ai-ideation` Slack channel, and rename it `.env`
* Open a new terminal (  **control + shift + `**  )
* After all dependencies install, activate the virtual environment: `.venv\Scripts\activate`
* Start the canopy server: `canopy start --host 127.0.0.1 --port 18888`
* Go to the following address in your browser in order to verify it's working: http://127.0.0.1:18888/docs#
* Open a new terminal in VS Code and activate the virtual environment again: `.venv\Scripts\activate`
* Start chainlit app: `chainlit run start-chat.py`
* Test out the bot by asking questions
