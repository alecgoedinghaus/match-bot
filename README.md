# Match Bot Com

HackSC 2021 Project :smile:

## Description

Discord bot that facilitates new connections in the workplace and among social groups. Have great conversations with like-minded colleagues you may have otherwise never met.

## Authors

Jason Lim (@jlimcode), Alec Goedinghaus (@alecgoedinghaus), and Gaurav Kale (@gkale15). 

## Usage

After cloning the git repository, run the following commands:

(For first time `pipenv` use)
```bash
pip install pipenv
```

Followed by:

```bash
cd match-bot
pipenv install
```

You'll need to have a couple environment variables set up before running. You can put these in a `.env` file.

```python
BOT_TOKEN= # Discord bot key
SERVICE_ACCOUNT_KEY= # Google Cloud service account key (usually given as a JSON file, enter here as a string)
```

Once your environment is set up, you can start the venv and run the bot.

```bash
pipenv shell
python match_bot.py
```
