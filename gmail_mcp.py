from mcp.server.fastmcp import FastMCP
import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("GmailSender")

GMAIL_USER = os.getenv("GMAIL_USER")  # your gmail
GMAIL_PASS = os.getenv("GMAIL_PASS")  # app password (not real password)

@mcp.tool()
def sendMail(to: str, subject: str, body: str):
    print('sending email mcp')
    """Send an email using Gmail"""
    try:
        msg = MIMEText(body)
        msg["From"] = GMAIL_USER
        msg["To"] = to
        msg["Subject"] = subject
        print('reached here----')

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASS)
            server.sendmail(GMAIL_USER, [to], msg.as_string())

        # ✅ return dict (LangGraph expects this)
        return {"result": f"✅ Email sent to {to} with subject '{subject}'"}

    except Exception as e:
        return {"error": f"❌ Error sending email: {e}"}


if __name__ == "__main__":
    mcp.run()
