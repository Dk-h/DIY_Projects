import os
import sys
import json
import smtplib
import logging
from datetime import datetime
from plyer import notification
from email.message import EmailMessage
from email.utils import formataddr
from hr_data_extracter import get_hr_details


# Step 1: Create logs folder in the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(script_dir, "logs")
os.makedirs(log_dir, exist_ok=True)

# Step 2: Create a timestamped log filename in AM/PM format
timestamp = datetime.now().strftime("%Y-%m-%d_%I-%M-%S_%p")  # 12-hour format with AM/PM
log_filename = os.path.join(log_dir, f"cold_email_log_{timestamp}.txt")

# Step 3: Set up logging configuration
# Create custom logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create file handler with UTF-8 support
file_handler = logging.FileHandler(log_filename, encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Create console (stream) handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Define logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Step 4: Log the start of the script (will go to both terminal and file)
logger.info("🚀 Cold Email Bulk Sender started")

# Hr Bulk Emails
FILE_NAME = "hr_emails_with_names.xlsx"
FILE_PATH = os.path.join(os.path.dirname(__file__), FILE_NAME)

# Email credentials
SENDER_EMAIL = "programmingdhruv@gmail.com"
SENDER_PASSWORD = "kpjl mjfo ehup mtvn"  # Use an app password if 2FA is enabled


# JSON file to store failed/remaining HRs
FAILED_EMAILS_FILE = "remaining_hr_emails.json"

#file name
RESUME_NAME = "Dhruv Kumar_cv_June_2025.pdf"

# Path to your resume PDF
resume_path = os.path.join(os.path.dirname(__file__), RESUME_NAME)

# List of demo emails
demo_emails = [
    # {'email': 'dhruvkumar11170@gmail.com', 'first_name': 'Dhruv', 'company': 'Razorpay'},
    # {'email': 'shravankumar11169@gmail.com', 'first_name': 'Shravan', 'company': 'gmail'},
    # {'email': 'dhruv.kumar@razorpay.com', 'first_name': 'Dhruv', 'company': 'Razorpay'},
    # {'email': 'shravankraiml2025@gmail.com', 'first_name': 'Shravan', 'company': 'OXFORD COLLEGE OF ENGINEERING AND TECHNOLOGY'},
    # {'email': 'neokre6922@gmail.com', 'first_name': 'Neokre', 'company': 'Riot Games'},
    # {'email': 'programmingdhruv@gmail.com', 'first_name': 'Dhruv', 'company': 'gmail'},
    # {'email': 'vikramadityajain2001@gmail.com', 'first_name': 'Vikramaditya', 'company': 'gmail'},
    # {'email': 'Vikramaditya@stockal.com', 'first_name': 'Vikramaditya', 'company': 'stockal'},
    # {'email': 'eashagoswami31@gmail.com', 'first_name': 'Esha', 'company': 'Vedantu'},
    {'email': 'pandeyprayagdutt@gmail.com', 'first_name': 'Prayag', 'company': 'Innodata'}
    
]

hr_emails = get_hr_details(FILE_PATH)

# Email content
subject = "Application for SDE Role – Dhruv Kumar"

# body in HTML content
html_template = """
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

def send_bulk_emails(email_list, save_file_name="default_list"):
    global hr_count
    hr_count = 1
    save_file_name = save_file_name + "_savefile.json"
    
    # Get the directory where the current .py file is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    save_file_name = os.path.join(script_dir, save_file_name)

    start_index = 0
    # Resume support
    if os.path.exists(save_file_name):
        with open(save_file_name, "r") as f:
            state = json.load(f)
            start_index = state.get("position", 0)
        logging.info(f"⏯️ Resuming from index {start_index} with HR details: {state.get('failed_at', 'N/A')}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            with open(resume_path, "rb") as f:
                resume_data = f.read()
            logging.info("✅ SMTP connection established and logged in successfully.")

            for i in range(start_index, len(email_list)):
                hr = email_list[i]
                try:
                    send_email(smtp, resume_data, hr["email"], hr["first_name"], hr["company"])
                    hr_count += 1
                    logging.info(f"{i+1}. ✅ Email sent to {hr['email']} at company {hr['company']}!")
                
                except Exception as e:
                    failed_email = email_list[i + 1]['email'] if i + 1 < len(email_list) else "END OF LIST"
                    logging.error(f"❌ Failed to send email to {failed_email} at index {i + 1}: {e}")

                    # Save the index to resume next time
                    with open(save_file_name, "w") as f:
                        json.dump({
                            "position": i+1,    # Save the next index to start from
                            "failed_at": hr,    # Full HR details at which it failed
                        }, f, indent=4)
                    logging.warning(f"⚠️ Resume state saved at index {i+1} in {save_file_name}")

                    # Notify user about the failure
                    notification.notify(
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
            
            # Notify user about successful completion
            logging.info("✅ All emails sent successfully!")

            notification.notify(
                title="✅ All Emails Sent Successfully!",
                message=f"{total_sent} emails sent successfully!",
                timeout=2
            )

    except Exception as e:
        logging.error(f"❌ SMTP connection or login failed: {e}")
        notification.notify(
            title="❌ SMTP Login Failed",
            message="Could not connect or login to Gmail",
            timeout=2
        )
        sys.exit(1)


                    


# Function to send email
def send_email(smtp, resume_data, to_email, first_name, company):
    personal_companies = ["gmail", "yahoo", "hotmail", "outlook"]
    first_name = first_name if first_name else "there"
    company_line = f"at <strong>{company}</strong>" if company.lower() not in personal_companies else "at your company"
    html_body = html_template.format(first_name=first_name, company_line=company_line)

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("Dhruv Kumar | Ex-Razorpay", SENDER_EMAIL))
    msg["To"] = to_email
    msg.add_alternative(html_body, subtype='html')
    msg.add_attachment(resume_data, maintype="application", subtype="pdf", filename=RESUME_NAME)
    
    try:
        smtp.send_message(msg)
        
    except Exception as e:
        logging.error(f"❌ Failed to send email to {to_email}: {e}")


# Sending emails to demo for debugging
send_bulk_emails(demo_emails,"demo_emails")

# Sending emails to HRs from the Excel file
# send_bulk_emails(hr_emails,"hr_emails")
