from gmail_reader import get_emails

if __name__ == "__main__":
    emails = get_emails()

    if not emails:
        print("No emails found.")
    else:
        for i, email in enumerate(emails):
            print(f"\n📩 Email {i+1}")
            print("Subject:", email["subject"])
            print("Body:", email["body"][:200])
            print("="*50)