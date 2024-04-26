from os import getenv
from dotenv import load_dotenv
import requests
import jinja2

load_dotenv()
template_loader=jinja2.FileSystemLoader("templates")
template_env=jinja2.Environment(loader=template_loader)

def render_template(template_filename,**context):
	return template_env.get_template(template_filename).render(**context)

def send_simple_message(email,username,sub,msg,html):
	print("OK")
	return requests.post(
	"https://api.mailgun.net/v3/sandbox90b20c42ffaa4724846d05fd84388e6f.mailgun.org/messages",
	auth=("api", getenv("MAILGUN_API_KEY")),
	data={"from": "Mailgun Sandbox <postmaster@sandbox90b20c42ffaa4724846d05fd84388e6f.mailgun.org>",
		"to": email,
		"subject": sub,
		"text": msg,
		"html":html})


def send_user_register_email(email,username):
	sub = "Registration Successfull"
	msg = f"Hello {username}, Congratulation."
	html = render_template("email/action.html")
	return send_simple_message(email,username,sub,msg,html)