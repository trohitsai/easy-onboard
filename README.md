# easy-onboard

easy-onboard is a slack based bot app which improves the new employee onbaording in a organisation. It brings in automation and sends greetings across the team using AI generative text via ChatGPT as follow. 

With this app installed in an organisation's slack workspace the HR needs to invite the new employee in slack. Once the new employee accepts the invite

1. The bot will automatically add employee to pre-defined slack channels
   <img width="808" alt="Screenshot 2023-10-01 at 6 38 23 PM" src="https://github.com/trohitsai/easy-onboard/assets/23382685/31d9dd06-2b73-46c8-99c4-ea56f634410c">
   <img width="513" alt="Screenshot 2023-10-01 at 6 41 30 PM" src="https://github.com/trohitsai/easy-onboard/assets/23382685/eb793293-acb7-4e4a-bc50-7c682295e656">


3. The bot will send out personalised greeting to the new new employee asking to complete onbaording
   <img width="957" alt="Screenshot 2023-10-01 at 6 37 41 PM" src="https://github.com/trohitsai/easy-onboard/assets/23382685/30d062b0-128a-4ca3-b068-944c5fac7c79">

4. Bot pass these details to chatgpt and custom welcome message is posted in a predefiend slack team channel on behalf of HR Team
   <img width="742" alt="Screenshot 2023-10-01 at 6 39 07 PM" src="https://github.com/trohitsai/easy-onboard/assets/23382685/1fa2c54d-9984-4afc-a1e5-356662e90173">

6. The bot sends interactive thanks note using AI to employee upon successful completion with important organisation docs to read
   <img width="756" alt="Screenshot 2023-10-01 at 6 39 40 PM" src="https://github.com/trohitsai/easy-onboard/assets/23382685/5228a791-70d2-4b55-8e53-8076d9940b79">

8. The Bot also sends an FYI note to HR in a slack DM with a google sheet link with all the onboarding details for reference
   <img width="802" alt="Screenshot 2023-10-01 at 6 40 04 PM" src="https://github.com/trohitsai/easy-onboard/assets/23382685/48fe8b5e-976e-4237-a87c-098d40b50106">


Tools used:

1. Slack REST API, modals & slack bot app to manage the interactions
2. ChatGPT APIs to creates dynamic interactive messages
3. Google sheets API
