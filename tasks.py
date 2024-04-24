from os import getenv
from dotenv import load_dotenv
import requests

load_dotenv()

def send_simple_message(email,username,sub,msg):
        return requests.post(
		"https://api.mailgun.net/v3/sandbox90b20c42ffaa4724846d05fd84388e6f.mailgun.org/messages",
		auth=("api", getenv("MAILGUN_API_KEY")),
		data={"from": "Mailgun Sandbox <postmaster@sandbox90b20c42ffaa4724846d05fd84388e6f.mailgun.org>",
			"to": email,
			"subject": sub,
			"text": msg})


def send_user_register_email(email,username):
        sub = "Registration Successfull"
        msg = f"Hello {username}, Congratulation."
        return send_simple_message(email,username,sub,msg)