import os
import sys
import json
import smtplib
import logging
from datetime import datetime
from plyer import facades
from email.message import EmailMessage
from email.utils import formataddr
from hr_data_extracter import get_hr_details

notifier = facades.Notification()   

# ============================
# CONFIGURATION SECTION
# ============================

# Email credentials (keep secure, do not hardcode in production)
SENDER_EMAIL = "programmingdhruv@gmail.com"
SENDER_PASSWORD = "kpjl mjfo ehup mtvn"  # Use an app password if 2FA is enabled

# File names
HR_EXCEL_FILE = "hr_emails_with_names.xlsx"
RESUME_NAME = "Dhruv Kumar_cv_June_2025.pdf"
FAILED_EMAILS_FILE = "remaining_hr_emails.json"

# Email subject
EMAIL_SUBJECT = "Application for SDE Role – Dhruv Kumar"

# HTML Email template for the body content
HTML_TEMPLATE = """
<html>
  <body style="font-family: Arial, sans-serif; font-size: 15px; color: #333;">
    <p>Dear {first_name},</p>
    <p>I hope you're doing well.</p>
    <p>
      My name is <strong>Dhruv Kumar</strong>, and I’m a <strong>C/C++</strong> and <strong>Python developer</strong> with ~2 years of experience in <strong>product development, system-level programming,</strong> and <strong>automation</strong>.
      At <strong>Razorpay</strong>, I contributed to launch their <strong>UPI Soundbox</strong>—working on <strong>embedded systems, API integration, CI/CD,</strong> and <strong>performance optimization</strong>.
    </p>
    <p>
      I'm currently exploring <strong>SDE opportunities</strong> and would love to contribute to the innovative work being done {company_line}.
      If you're hiring or open to referrals, I'd be grateful for a chance to be considered.
    </p>
    <p>Thanks for your time, and I’d be happy to connect or share more details!</p>
    <p>
      Warm regards,<br>
      <strong>Dhruv Kumar</strong><br>
      Bangalore, India<br>
      +91 91104 89438<br>
      <a href="https://www.linkedin.com/in/dhruv-kumar-8926631b2/" target="_blank">LinkedIn | </a>
      <a href="https://github.com/Dk-h" target="_blank">GitHub</a>
    </p>
    <hr style="margin: 20px 0;">
    <h4 style="color: #444;"> Quick Profile Summary:</h4>
    <ul>
        <li><strong>Name:</strong> Dhruv Kumar</li>
        <li><strong>Total Experience:</strong> ~2 years</li>
        <li><strong>Date of Birth:</strong> 01-10-2001</li>
        <li><strong>Location:</strong> Bangalore</li>
        <li><strong>Work Mode:</strong> Comfortable with Hybrid, Remote, and In-Office roles</li>
        <li><strong>Previous Companies:</strong> Razorpay, ITC</li>
        <li><strong>Notice Period:</strong> Immediately available to join</li>
        <li><strong>Primary Skills:</strong> C++, Python, Java(Basics), MySQL, Implementing REST APIs, Embedded Systems</li>
        <li><strong>Previous Company CTC:</strong> 5.4 LPA</li>
        <li><strong>Education:</strong> B.Tech in Computer Science and Engineering (Graduated in 2023)</li>
    </ul>
    <hr style="margin: 20px 0;">
  </body>
</html>
"""

# List of demo emails for testing
DEMO_EMAILS = [
    {'email': 'pandeyprayagdutt@gmail.com', 'first_name': 'Prayag', 'company': 'Innodata'}
    # Add more dictionaries for further testing
]

# ============================
# LOGGING SETUP
# ============================

def setup_logger():
    """Configures logging both to a file and the console."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(script_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p")
    log_filename = os.path.join(log_dir, f"cold_email_log_{timestamp}.txt")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.info("🚀 Cold Email Bulk Sender started")
    return logger

logger = setup_logger()

# ============================
# CORE FUNCTIONS
# ============================

def send_bulk_emails(email_list, resume_path, save_file_prefix="default_list"):
    """
    Sends bulk emails with resume attached. Supports resuming on failure.
    Args:
        email_list (list): List of dicts with keys: 'email', 'first_name', 'company'
        resume_path (str): Path to the PDF resume to attach.
        save_file_prefix (str): Prefix for the resume state file.
    """
    # Prepare save file for resuming state
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_file_name = os.path.join(script_dir, save_file_prefix + "_savefile.json")
    start_index = 0

    # Resume from the last failed email if save file exists
    if os.path.exists(save_file_name):
        with open(save_file_name, "r") as f:
            state = json.load(f)
            start_index = state.get("position", 0)
        logger.info(f"⏯️ Resuming from index {start_index} with HR details: {state.get('failed_at', 'N/A')}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            with open(resume_path, "rb") as res_file:
                resume_data = res_file.read()
            logger.info("✅ SMTP connection established and logged in successfully.")

            for i in range(start_index, len(email_list)):
                hr = email_list[i]
                try:
                    send_email(smtp, resume_data, hr["email"], hr.get("first_name"), hr.get("company"))
                    logger.info(f"{i+1}. ✅ Email sent to {hr['email']} at company {hr['company']}!")
                except Exception as e:
                    failed_email = email_list[i + 1]['email'] if i + 1 < len(email_list) else "END OF LIST"
                    logger.error(f"❌ Failed to send email to {failed_email} at index {i + 1}: {e}")
                    # Save current state for resume
                    with open(save_file_name, "w") as f:
                        json.dump({"position": i+1, "failed_at": hr}, f, indent=4)
                    logger.warning(f"⚠️ Resume state saved at index {i+1} in {save_file_name}")
                    notifier.notify(
                        title="❌ Email Sending Failed",
                        message=f"Failed at {hr['email']} – resume saved",
                        timeout=2
                    )
                    sys.exit(1)

            # All emails sent successfully
            total_sent = len(email_list) - start_index
            logger.info(f"🎉 All {total_sent} emails sent successfully!")

            if os.path.exists(save_file_name):
                os.remove(save_file_name)
                logger.info(f"🗑️ Deleted resume save file: {save_file_name}")

            notifier.notify(
                title="✅ All Emails Sent Successfully!",
                message=f"{total_sent} emails sent successfully!",
                timeout=2
            )

    except Exception as e:
        logger.error(f"❌ SMTP connection or login failed: {e}")
        notifier.notify(
            title="❌ SMTP Login Failed",
            message="Could not connect or login to Gmail",
            timeout=2
        )
        sys.exit(1)

def send_email(smtp, resume_data, to_email, first_name, company):
    """
    Sends a single email with the resume attached.
    Args:
        smtp (smtplib.SMTP_SSL): Authenticated and connected SMTP client.
        resume_data (bytes): Resume PDF data.
        to_email (str): Recipient's email address.
        first_name (str): Recipient's first name.
        company (str): Recipient's company.
    """
    personal_companies = {"gmail", "yahoo", "hotmail", "outlook"}
    first_name = first_name or "there"
    company_line = f"at <strong>{company}</strong>" if company and company.lower() not in personal_companies else "at your company"
    html_body = HTML_TEMPLATE.format(first_name=first_name, company_line=company_line)

    msg = EmailMessage()
    msg["Subject"] = EMAIL_SUBJECT
    msg["From"] = formataddr(("Dhruv Kumar | Ex-Razorpay", SENDER_EMAIL))
    msg["To"] = to_email
    msg.add_alternative(html_body, subtype='html')
    msg.add_attachment(resume_data, maintype="application", subtype="pdf", filename=RESUME_NAME)
    smtp.send_message(msg)

# ============================
# ENTRY POINT
# ============================

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    resume_path = os.path.join(script_dir, RESUME_NAME)
    hr_file_path = os.path.join(script_dir, HR_EXCEL_FILE)

    # Load HR email list from Excel (custom extractor)
    hr_emails = get_hr_details(hr_file_path)

    # For testing: send to demo emails only
    send_bulk_emails(DEMO_EMAILS, resume_path, "demo_emails")

    # For actual HR bulk sending, uncomment below:
    # send_bulk_emails(hr_emails, resume_path, "hr_emails")

if __name__ == "__main__":
    main()

# ============================
# USAGE NOTES
# ============================
# - Configure SENDER_EMAIL and SENDER_PASSWORD securely.
# - Place your resume and HR Excel file in the same directory as this script.
# - For production, use environment variables or a config file for credentials.
# - If interrupted, the script will resume from where it left off.
# - For debugging, use DEMO_EMAILS (single or a few emails).
# - Logging is available in both console and "logs/" folder.