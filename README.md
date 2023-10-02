# easy-onboard

easy-onboard is a slack based bot app which improves the new employee onbaording in a organisation. It brings in automation and sends greetings across the team using AI generative text via ChatGPT as follow. 

With this app installed in an organisation's slack workspace the HR needs to invite the new employee in slack. Once the new employee accepts the invite

1. The bot will automatically add employee to pre-defined slack channels
3. The bot will send out personalised greeting to the new new employee asking to complete onbaording
4. Bot pass these details to chatgpt and custom welcome message is posted in a predefiend slack team channel on behalf of HR Team
6. The bot sends interactive thanks note using AI to employee upon successful completion with important organisation docs to read
8. The Bot also sends an FYI note to HR in a slack DM with a google sheet link with all the onboarding details for reference
 
# Tools used:

1. Slack REST API, modals & slack bot app to manage the interactions
2. ChatGPT APIs to creates dynamic interactive messages
3. Google sheets API
4. ngrok

# Setting up Repository

Pull the code from this repo in your local. 
Create a virtual env first and activate it in your local. 
```
mkdir venvs && cd venvs && python -m venv myenv
source myenv/bin/activate
```
Now with the virtual env activated go the easy-onboard repository directory and install all dependencies from requirements file.
```
pip install -r requirements.txt
```

Now start the server using below command ```python runserver.py``` command and you see below output
```
 * Serving Flask app 'runserver'
 * Debug mode: on [2023-10-01 20:57:38,380] INFO {/easy-onboard/lib/python3.9/site-packages/werkzeug/_internal.py:187}
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5002
```

Now Create a .env file under easy-onboard/app/ directory and copy contents from .env.example. We will adding values to this in further steps.

**1. Setting up Google sheets**

Follow this article for setting up GCP account, enabling google sheets & drive api and creating a service account json credentials. Add the downloaded credentials file path in .env file under **GCP_SERVICE_ACC_KEY** = /path/to/json/file.

Also create a sample spread sheet and update the spreadsheet id (you can get in from sheet url in browser) in .env file for **SPREADSHEET_ID** variable

**2. Setting up chatGPT**

Create a trial account in chatGPT and create a API key and update values for **OPENAI_API_KEY** in .env file

**3. Setting up slack**

Once you created a free slack account get your slack workspace id and update **SLACK_WORKSPACE_ID** var in .env file
There are a series of steps to follow in order to create & configure a slack bot app. For this please this article.

**4. Setting up ngrok**

Install ngrok from official website: https://ngrok.com/download
Open terminal and go to the downloaded location. Run the ngrok executable on the same port where the app is running.
```
./ngrok http 5002
```
This will give you a ngrok url which can be accessed anywhere from web. All requests will be forwarded to 5002
