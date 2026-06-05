import smtplib
from email.message import EmailMessage
from typing import Optional
from src.env import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM, require_env


def send_email(to_address: str, subject: str, body: str, from_address: Optional[str] = None) -> str:
    smtp_host = require_env("SMTP_HOST", SMTP_HOST)
    smtp_port = int(require_env("SMTP_PORT", SMTP_PORT))
    smtp_user = require_env("SMTP_USER", SMTP_USER)
    smtp_password = require_env("SMTP_PASSWORD", SMTP_PASSWORD)
    from_addr = from_address or EMAIL_FROM or smtp_user

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = from_addr
    message["To"] = to_address
    message.set_content(body)

    try:
        # Use SSL for port 465, STARTTLS for 587, otherwise try plain SMTP
        if smtp_port == 465:
            with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=20) as server:
                server.login(smtp_user, smtp_password)
                server.send_message(message)
        else:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
                # Upgrade to TLS for common submission ports
                try:
                    server.starttls()
                except Exception:
                    # Some servers may not support STARTTLS on the given port
                    pass
                server.login(smtp_user, smtp_password)
                server.send_message(message)
    except Exception as exc:
        raise RuntimeError(f"SMTP send failed: {exc}")

    return f"Email sent to {to_address} from {from_addr}."
