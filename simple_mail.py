import imaplib
import email
import smtplib
from email.mime.text import MIMEText
import ollama

import os

EMAIL = os.getenv("EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def generate_reply(email_text):
    prompt = f"""
You are ReplyGenius AI, a professional email assistant.

Write a polite and helpful reply for this email:

{email_text}

Rules:
- Be professional
- Keep it short
- If complaint → apologize and assure resolution
"""

    response = ollama.chat(
        model="tinyllama",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']


def send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg['From'] = EMAIL
    msg['To'] = to_email
    msg['Subject'] = "Re: " + subject

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()


def read_and_reply():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, APP_PASSWORD)

    mail.select("inbox")

    result, data = mail.search(None, "UNSEEN")
    mail_ids = data[0].split()

    for i in mail_ids:
        result, msg_data = mail.fetch(i, "(RFC822)")
        raw_email = msg_data[0][1]

        msg = email.message_from_bytes(raw_email)

        subject = msg["subject"]
        from_email = email.utils.parseaddr(msg["From"])[1]

        print("\n📩 Email from:", from_email)
        print("Subject:", subject)

        body = ""

        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode(errors="ignore")
                    break
        else:
            body = msg.get_payload(decode=True).decode(errors="ignore")

        print("\n📄 Email Body:\n", body[:300])

        # 🤖 Generate reply
        reply = generate_reply(body)

        print("\n🤖 Suggested Reply:\n", reply)

        # 🔥 USER APPROVAL
        choice = input("\nSend this reply? (yes / no / edit): ").lower()

        if choice == "yes":
            send_email(from_email, subject, reply)
            print("✅ Reply sent!")

        elif choice == "edit":
            new_reply = input("\n✏️ Enter your edited reply:\n")
            send_email(from_email, subject, new_reply)
            print("✅ Edited reply sent!")

        else:
            print("❌ Skipped.")

        print("="*60)


if __name__ == "__main__":
    read_and_reply()