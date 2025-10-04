# Cold Email Bulk Sender

This Python project allows you to send personalized bulk emails (with resume attachments) to HR contacts or demo addresses using Gmail. It features resume-on-failure, desktop notifications, and informative logging for a smooth developer experience.

---

## Features

- **Bulk email sending** with HTML formatting and resume PDF attachment
- **Personalization**: Each HR gets a tailored greeting and company name
- **Resume-on-failure**: If an error occurs, resume from where you left off
- **Desktop notifications** for success/failure
- **Logs** are written to both console and a timestamped file in a `logs/` folder
- **Test mode**: Try with demo emails before sending to real HR contacts
- **Configuration and sensitive data** are stored in external files (no sensitive info in your codebase)
- **HTML email template** is stored in an external file for easy editing

---

## Prerequisites

- Python 3.7+
- A Gmail account with [App Passwords enabled](https://support.google.com/accounts/answer/185833) (if 2FA is on)
- Your resume PDF file
- An Excel file (`.xlsx`) containing HR email contacts

---

## Setup

1. **Clone or download this repository.**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare your files:**
   - Place your resume PDF (e.g., `Dhruv Kumar_cv_June_2025.pdf`) in the project directory.
   - Ensure your Excel file (e.g., `hr_emails_with_names.xlsx`) with HR details is in the project directory.
   - Your Excel file should have at least the columns: `email`, `first_name`, and `company`.

4. **Set up your Gmail App Password:**
   - Go to your Google Account > Security > App Passwords.
   - Generate a new password for "Mail".
   - Create a file named `credentials.json` in the project directory with the following format:
     ```json
     {
       "SENDER_EMAIL": "your_email@gmail.com",
       "SENDER_PASSWORD": "your_app_password"
     }
     ```
   - **Important:** Add `credentials.json` to your `.gitignore` file to avoid committing sensitive info.

5. **Configure demo and HR emails:**
   - Edit the `DEMO_EMAILS` list in the script to add your test emails.
   - Make sure your Excel file is referenced correctly in the script.

6. **Create or edit your HTML email template:**
   - Place your email content in a file named `email_template.html` in the project directory.
   - You can use placeholders like `{first_name}` and `{company_line}` in your template.  
     Example:
     ````html
     <html>
       <body>
         <p>Dear {first_name},</p>
         <!-- ...rest of your template... -->
       </body>
     </html>
     ````

---

## Running the Program

### 1. **Test with Demo Emails (Recommended)**
By default, the script sends emails to addresses in the `DEMO_EMAILS` list.  
To run:
```bash
python bulk_email_sender.py
```
Check your inbox (or the inboxes you listed) to verify the format and attachment.

### 2. **Send to Actual HR List**
- Uncomment the line in the script that calls:
  ```python
  send_bulk_emails(hr_emails, resume_path, "hr_emails")
  ```
- Comment out or remove the line that sends to `DEMO_EMAILS`.

Then run:
```bash
python bulk_email_sender.py
```

---

## How Resume-on-Failure Works

- If an email fails to send (e.g., network error), the script saves progress in a `*_savefile.json`.
- Next time you run the script, it resumes from the failed contact.
- After all emails are sent, this save file is deleted automatically.

---

## Logs and Notifications

- All activity is logged to both the console and a timestamped file in the `logs/` directory.
- Desktop notifications inform you of success or failure (requires `plyer` and a supported OS).

---

## Security Note

- **Never commit your `credentials.json` to a public repository!**
- `.gitignore` should include:
  ```
  credentials.json
  ```
- Consider using environment variables or a `.env` file for credentials in production.

---

## Customizing

- **Email content:** Edit the `email_template.html` file.
- **Subject line:** Edit `EMAIL_SUBJECT` in your script.
- **Resume name:** Change `RESUME_NAME` if your file has a different name.
- **Excel parsing:** The script expects a compatible `get_hr_details()` function and standard columns; adjust if your format differs.

---

## Troubleshooting

- **SMTP Login Failed:** Double-check your email/app password and ensure "Allow less secure apps" (if needed) is set.
- **No notification:** Make sure `plyer` is installed and your OS supports notifications.
- **Excel reading errors:** Make sure your file is `.xlsx` and has required columns.

---

## License

MIT License

---

**Happy bulk emailing!**