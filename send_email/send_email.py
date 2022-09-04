from django.shortcuts import render

import environ
import smtplib

from email.message import EmailMessage


def send_email(self, subscription, result):
    email_address = environ.Env(DEBUG=(bool, False))("GMAIL_ADDRESS")
    email_password = environ.Env(DEBUG=(bool, False))("GMAIL_PASSWORD")

    msg = EmailMessage()
    msg.set_content(
        f"Flights from {subscription.search.fly_from} to {subscription.search.fly_to} available for "
        f"{result.price} {subscription.curr} on {result.departure_date}!")
    msg["Subject"] = f"Tickets to {subscription.search.fly_from}({subscription.search.fly_to}) " \
                     f"on sale for ${result.price}!"
    msg["From"] = email_address
    msg["To"] = subscription.email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_address, email_password)
        smtp.send_message(msg)
