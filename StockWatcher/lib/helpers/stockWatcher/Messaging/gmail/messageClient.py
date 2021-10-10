import asyncio
import os
import re
from email.message import EmailMessage
import requests
import json

import aiosmtplib

HOST = "smtp.gmail.com"
import smtplib

carriers = {
    "att": "@mms.att.net",
    "tmobile": " @tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@page.nextel.com",
}

CARRIER_MAP = {
    "verizon": "vtext.com",
    "tmobile": "tmomail.net",
    "sprint": "messaging.sprintpcs.com",
    "at&t": "txt.att.net",
    "boost": "smsmyboostmobile.com",
    "cricket": "sms.cricketwireless.net",
    "uscellular": "email.uscc.net",
    "rogers": "mms.rogers.com",
}


class GmailMessage:
    async def send_txt(
        num: str, carrier: str, email: str, pword: str, msg: str, subj: str
    ):
        to_email = CARRIER_MAP[carrier]

        # build message
        message = EmailMessage()
        message["From"] = email
        message["To"] = f"{num}@{to_email}"
        message["Subject"] = subj
        message.set_content(msg)

        # send
        send_kws = dict(
            username=email, password=pword, hostname=HOST, port=587, start_tls=True
        )

        res = await aiosmtplib.send(message, **send_kws)  # type: ignore
        msg = "failed" if not re.search(r"\sOK\s", res[1]) else "succeeded"
        print(msg)
        return res

    def send(self, message):
        print(message)
        # Replace the number with your own, or consider using an argument\dict for multiple people.
        # to_number = '000-000-0000{}'.format(carriers['att'])
        to_number = "+16476404714"
        auth = ("benaimjacob@gmail.com", "Jb100831792!")

        # Establish a secure session with gmail's outgoing SMTP server using your gmail account
        server = smtplib.SMTP("smtp.gmail.com", 465)
        server.starttls()
        server.login(auth[0], auth[1])

        # Send text message through SMS gateway of destination number
        server.sendmail(auth[0], to_number, message)

    def send_message(self, message):
        # >>>>>>>>>>>>>>>>>>> GIVE AN UP VOTE IF YOU LIKED IT <<<<<<<<<<<<<<<<<<<<<

        # Easiest and Readable way to Email
        # through Python SMTPLIB library
        # This works with >>> Gmail.com <<<
        import smtplib
        from email.message import EmailMessage

        EmailAdd = "jacobjbenaim@gmail.com"  # senders Gmail id over here
        Pass = "Jb072775687!#?"  # senders Gmail's Password over here

        msg = EmailMessage()
        msg["Subject"] = "Subject of the Email"  # Subject of Email
        msg["From"] = EmailAdd
        msg["To"] = os.environ["TWILIO_ADMINS_PHONE"]  # Reciver of the Mail
        msg.set_content(message)  # Email body or Content

        #### >> Code from here will send the message << ####
        with smtplib.SMTP_SSL(
            "smtp.gmail.com", 465
        ) as smtp:  # Added Gmails SMTP Server
            smtp.login(
                EmailAdd, Pass
            )  # This command Login SMTP Library using your GMAIL
            smtp.send_message(msg)  # This Sends the message

    def send_text_with_d7(self, message):
        url = "https://d7sms.p.rapidapi.com/secure/send"

        # payload = "{
        #     \"content\": \"Test Message\",
        #     \"from\": \"D7-Rapid\",
        #     \"to\": 971562316353
        # }"

        payload = {
            "content": "Tester mesasge",
            "from": "benaimjacob@gmail.com",
            "to": 16476404714,
        }
        headers = {
            "content-type": "application/json",
            "authorization": "Basic YmVuYWltamFjb2JAZ21haWwuY29tOkpiMTAwODMxNzky",
            "x-rapidapi-host": "d7sms.p.rapidapi.com",
            "x-rapidapi-key": "c3fe4d53bfmsh78a04e937273bbcp1032b7jsn26aa30f05d4e",
        }

        response = requests.request(
            "POST", url, data=json.dumps(payload), headers=headers
        )

        print(response.text)


# G = GmailMessage()

# G.send_text_with_d7("TERST")

# import asyncio
# import re
# from email.message import EmailMessage
# from typing import Tuple, Union

# import aiosmtplib

# HOST = "smtp.gmail.com"
# # https://kb.sandisk.com/app/answers/detail/a_id/17056/~/list-of-mobile-carrier-gateway-addresses
# # https://www.gmass.co/blog/send-text-from-gmail/
# CARRIER_MAP = {
#     "verizon": "vtext.com",
#     "tmobile": "tmomail.net",
#     "sprint": "messaging.sprintpcs.com",
#     "at&t": "txt.att.net",
#     "boost": "smsmyboostmobile.com",
#     "cricket": "sms.cricketwireless.net",
#     "uscellular": "email.uscc.net",
#     "rogers": "mms.rogers.com",
# }


# pylint: disable=too-many-arguments
# async def send_txt(
#     num: Union[str, int], carrier: str, email: str, pword: str, msg: str, subj: str
# ) -> Tuple[dict, str]:
#     to_email = CARRIER_MAP[carrier]

#     # build message
#     message = EmailMessage()
#     message["From"] = email
#     message["To"] = f"{num}@{to_email}"
#     message["Subject"] = subj
#     message.set_content(msg)

#     # send
#     send_kws = dict(
#         username=email, password=pword, hostname=HOST, port=587, start_tls=True
#     )
#     res = await aiosmtplib.send(message, **send_kws)  # type: ignore
#     print(res)
#     msg = "failed" if not re.search(r"\sOK\s", res[1]) else "succeeded"
#     print(msg)
#     return res


EmailAdd = "jacobjbenaim@gmail.com"  # senders Gmail id over here
Pass = "Jb072775687!#?"
ToNum = "+16476404714"
ToEmail = "jacob.benaim@icloud.com"

# if __name__ == "__main__":
#     _num = ToEmail
#     _carrier = "rogers"
#     _email = EmailAdd
#     _pword = Pass
#     _msg = "Dummy msg"
#     _subj = "Dummy subj"
#     coro = send_txt(_num, _carrier, _email, _pword, _msg, _subj)
#     asyncio.run(coro)

# def test_mail_to_sms():
# from django.core.mail import send_mail
# send_mail('','test','',['my_number@mynetwork'])

# send('test')


# gmail = GmailMessage()

# auth = {
# 	'email':'benaimjacob@gmail.com',
# 	'password':'Jb100831792!'
# }

# coro = gmail.send_txt(
# 	carrier="rogers",
# 	email=auth['email'],
# 	pword=auth['password'],
# 	msg='tets',
# 	subj='test sub'
# 	)
# asyncio.run(coro)


# gmail.send('messge')
