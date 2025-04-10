from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email.utils
import os

app = Flask(__name__)

@app.route("/send-email", methods=["POST"])
def api_send_email():
    data = request.get_json()

    sender_email = os.environ.get("EMAIL")
    sender_password = os.environ.get("EMAIL_PASSWORD")

    recipient = data.get("email")
    subject = data.get("oggetto")
    body = data.get("corpo")

    try:
        message = MIMEMultipart("alternative")
        message["From"] = f"FiammaE20 <{sender_email}>"
        message["To"] = recipient
        message["Subject"] = subject
        message["Reply-To"] = sender_email
        message["Message-ID"] = f"<{hash(subject)}@gmail.com>"
        message["Date"] = email.utils.formatdate(localtime=True)

        # Parte testuale e HTML
        text_part = MIMEText(body, "plain")
        html_part = MIMEText(f"<html><body><p>{body}</p></body></html>", "html")

        message.attach(text_part)
        message.attach(html_part)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)

        return jsonify({"status": "ok", "message": "Email inviata con successo ✅"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
