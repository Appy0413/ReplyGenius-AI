import imaplib
import email
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

import os
load_dotenv(dotenv_path="E:\\ReplyGenius-AI\\.env")
APP_PASSWORD = os.getenv("APP_PASSWORD")
EMAIL = os.getenv("EMAIL")
print("EMAIL:", EMAIL)
print("APP_PASSWORD:", APP_PASSWORD)  


# 🤖 SMART REPLY FUNCTION (FREE + STABLE)
def generate_reply(email_text):
    text = email_text.lower().strip()

    # ✅ RULE-BASED PERFECT RESPONSES
    if "how are you" in text:
        return "I'm doing well, thanks! How about you?"

    if text in ["hi", "hello", "hey"]:
        return "Hi! How are you?"

    if "thank you" in text:
        return "You're welcome! Happy to help."

    if any(word in text for word in ["charged", "refund", "issue", "problem"]):
        return "Sorry about that. We'll check this and resolve it soon."

    if any(word in text for word in ["when", "what", "how", "can you"]):
        return "Thanks for your question. Let me check and get back to you shortly."

    # 🤖 FALLBACK → LOCAL MODEL (OPTIONAL)
    try:
        import ollama

        prompt = f"""
Reply in 1 short sentence only.
No extra text.

Message:
{text}
"""

        response = ollama.chat(
            model="tinyllama",
            messages=[{"role": "user", "content": prompt}]
        )

        reply = response['message']['content'].strip()

        # 🛑 FILTER BAD OUTPUT
        if len(reply) > 100 or "Dear" in reply or "Regards" in reply:
            return "Thanks for reaching out! I'll get back to you shortly."

        return reply

    except:
        return "Thanks for reaching out! I'll get back to you shortly."


# 📤 SEND EMAIL
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


# 📩 READ + REPLY SYSTEM
def read_and_reply():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(EMAIL, APP_PASSWORD)

    mail.select("inbox")

    result, data = mail.search(None, "UNSEEN")
    mail_ids = data[0].split()

    if not mail_ids:
        print("📭 No new emails.")
        return

    for i in mail_ids:
        result, msg_data = mail.fetch(i, "(RFC822)")
        raw_email = msg_data[0][1]

        msg = email.message_from_bytes(raw_email)

        subject = msg["subject"]
        from_email = email.utils.parseaddr(msg["From"])[1]

        print("\n📩 Email from:", from_email)
        print("Subject:", subject)

        # 📄 Extract body
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

        # 👤 USER APPROVAL
        choice = input("\nSend this reply? (yes / no / edit): ").lower()

        if choice == "yes":
            send_email(from_email, subject, reply)
            print("✅ Reply sent!")

        elif choice == "edit":
            new_reply = input("\n✏️ Enter your reply:\n")
            send_email(from_email, subject, new_reply)
            print("✅ Edited reply sent!")

        else:
            print("❌ Skipped.")

        print("=" * 60)


# ▶️ RUN
if __name__ == "__main__":
    read_and_reply()
  