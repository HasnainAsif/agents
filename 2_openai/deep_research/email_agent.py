# This agent will take report and send it as a nicely formatted HTML email.

import os
from typing import Dict

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
import resend
from agents import Agent, function_tool

# @function_tool
# def send_email(subject: str, html_body: str) -> Dict[str, str]:
#     """ Send an email with the given subject and HTML body """
#     sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
#     from_email = Email("ed@edwarddonner.com") # put your verified sender here
#     to_email = To("ed.donner@gmail.com") # put your recipient here
#     content = Content("text/html", html_body)
#     mail = Mail(from_email, to_email, subject, content).get()
#     response = sg.client.mail.send.post(request_body=mail)
#     print("Email response", response.status_code)
#     return {"status": "success"}

@function_tool
def send_html_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send out an email with the given subject and HTML body to all sales prospects """
    resend.api_key = os.environ.get('RESEND_API_KEY')
    
    params = {
        "from": "onboarding@resend.dev",  # Change to your verified sender domain or use a test address provided by resend
        "to": ["hasnainasif52@gmail.com"],  # Change to your recipient
        "subject": subject,
        "html": html_body
    }
    
    response = resend.Emails.send(params)
    return {"status": "success", "id": response.get("id")}

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the 
report converted into clean, well presented HTML with an appropriate subject line."""

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_html_email],
    model="gpt-4o-mini",
)
