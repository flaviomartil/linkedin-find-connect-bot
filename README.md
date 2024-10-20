<div align="center">
  <h1>--// Linkedin Connect Bot //--</h1>
</div>

## About

This is a bot that automatically connects to people on LinkedIn. It uses Selenium to automate the process of logging in and connecting to people.

## Prerequisites

- Python 3.6+
- Selenium (`pip install selenium`)
- python-dotenv (`pip install python-dotenv`)
- ChromeDriver (Recommend using driver from this repo as it is already configured to work with the bot or download the latest version [here](https://chromedriver.chromium.org/downloads))

## Usage

1. Clone the Repository
2. Install the prerequisites
3. Copy the `.env.example` file and rename it to `.env` and fill in the required fields
4. Run the bot (`python main.py`)
5. It will open a Chrome window and start connecting to people
6. Once it has finished it will close the Chrome window and stop the bot
7. You can find the people it connected to in the `./connections/role` folder
8. Enjoy!

## Env Variables

- `MY_NAME` - Your name (this is used to send notes to the people you connect to)
- `EMAIL` - Your LinkedIn email
- `PASSWORD` - Your LinkedIn password (this will be stored in plain text in the `.env` file so make sure to keep it safe)
- `KEYWORD` - Your desired KEYWORD to find
- `SEND_WITH_NOTE` - Whether to send a note with the connection request (set to `true` or `false`) (only set to `true` if your account has LinkedIn Premium)
