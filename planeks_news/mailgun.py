import requests

def send_simple_message():
	return requests.post(
		"https://api.eu.mailgun.net/v3/mg.dnz144.kiev.ua",
		auth=("api", "f52bddb9ae04dd2d7ea01f398f03d1ee-5645b1f9-bd5b07a5"),
		data={"from": "Excited User <mailgun@mg.dnz144.kiev.ua>",
			"to": ["samoilovartem1989@gmail.com",],
			"subject": "Hello",
			"text": "Testing some Mailgun awesomness!"})
