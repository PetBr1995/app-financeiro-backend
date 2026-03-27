import smtplib
from email.message import EmailMessage
from urllib.parse import quote

from flask import current_app


class EmailService:
    @staticmethod
    def is_configured():
        required = [
            current_app.config.get("SMTP_HOST"),
            current_app.config.get("SMTP_FROM_EMAIL"),
        ]
        return all(required)

    @staticmethod
    def build_password_reset_url(token):
        base_url = current_app.config.get("PASSWORD_RESET_FRONTEND_URL", "").strip()
        if "{token}" in base_url:
            return base_url.replace("{token}", quote(token))

        separator = "&" if "?" in base_url else "?"
        return f"{base_url}{separator}token={quote(token)}"

    @staticmethod
    def send_password_reset_email(to_email, token, expires_in_minutes):
        reset_url = EmailService.build_password_reset_url(token)
        from_email = current_app.config["SMTP_FROM_EMAIL"]
        from_name = current_app.config.get("SMTP_FROM_NAME", "Financas API")

        message = EmailMessage()
        message["Subject"] = "Recuperação de senha"
        message["From"] = f"{from_name} <{from_email}>"
        message["To"] = to_email
        message.set_content(
            (
                "Recebemos uma solicitação para redefinir sua senha.\n\n"
                f"Use este link para criar uma nova senha:\n{reset_url}\n\n"
                f"Este link expira em {expires_in_minutes} minutos.\n"
                "Se você não solicitou essa alteração, ignore este email."
            )
        )

        smtp_host = current_app.config["SMTP_HOST"]
        smtp_port = current_app.config["SMTP_PORT"]
        smtp_username = current_app.config.get("SMTP_USERNAME")
        smtp_password = current_app.config.get("SMTP_PASSWORD")
        use_tls = current_app.config.get("SMTP_USE_TLS", True)
        use_ssl = current_app.config.get("SMTP_USE_SSL", False)

        if use_ssl:
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=20) as smtp:
                if smtp_username and smtp_password:
                    smtp.login(smtp_username, smtp_password)
                smtp.send_message(message)
            return

        with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as smtp:
            if use_tls:
                smtp.starttls()
            if smtp_username and smtp_password:
                smtp.login(smtp_username, smtp_password)
            smtp.send_message(message)
