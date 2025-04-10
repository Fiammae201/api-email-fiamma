from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email.utils
import os

# 🔧 CREA l'app Flask PRIMA di usarla!
app = Flask(__name__)

@app.route("/send-email", methods=["POST"])

def api_send_email():
    data = request.get_json()

    sender_email = os.environ.get("EMAIL")
    sender_password = os.environ.get("EMAIL_PASSWORD")

    recipient = data.get("email")
    subject = data.get("oggetto")
    body = data.get("corpo")
    allegato_base64 = data.get("allegato_base64")
    filename = data.get("filename", "allegato.pdf")

    try:
        message = MIMEMultipart("mixed")
        message["From"] = f"FiammaE20 <{sender_email}>"
        message["To"] = recipient
        message["Subject"] = subject
        message["Reply-To"] = sender_email
        message["Message-ID"] = f"<{hash(subject)}@gmail.com>"
        message["Date"] = email.utils.formatdate(localtime=True)

        # Parte testuale
        text_part = MIMEText(body, "plain")
        html_part = MIMEText(f"<html><body><p>{body}</p></body></html>", "html")
        alternative = MIMEMultipart("alternative")
        alternative.attach(text_part)
        alternative.attach(html_part)

        message.attach(alternative)

        # Gestione allegato
        if allegato_base64:
            from email.mime.base import MIMEBase
            from email import encoders
            import base64

            pdf_data = base64.b64decode(allegato_base64)
            pdf_part = MIMEBase("application", "pdf")
            pdf_part.set_payload(pdf_data)
            encoders.encode_base64(pdf_part)
            pdf_part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
            message.attach(pdf_part)

        # Invia tramite SMTP Gmail
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)

        return jsonify({"status": "ok", "message": "Email con PDF inviata con successo ✅"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
