from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage
import base64
import os
import re
app = Flask(__name__)


SENDER_EMAIL = os.getenv("SENDER_EMAIL") # Get sender email from environment variable
APP_PASSWORD = os.getenv("EMAIL_PASS")   # Get app password from environment variable

if not SENDER_EMAIL or not APP_PASSWORD:
    raise ValueError("Environment variables not set")

@app.route("/send-mail", methods=["POST"])
def send_mail():

    data = request.json                           # Get JSON data from the request
    
    receiver_email = data.get("receiver_email")   # Get receiver email from the data
    message = data.get("otp")                    # Get message from the data
    email_type = data.get("email_type")          # Get email type from the data
    

    if not receiver_email or not message:
        return jsonify({"error": "Missing data"}), 400
    # Create Email
    msg = EmailMessage()
    msg["Subject"] = "Verificaton OTP for JSRN Bank"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    # msg.set_content(message)                     # Plain text content (optional)
    if email_type == "Birthday":
        msg.add_alternative(f"""
    <html>
    <body style="margin:0;padding:0;background:linear-gradient(135deg,#ff9a9e,#fad0c4);font-family:Arial;">
        
        <table width="100%" height="100%" cellpadding="0" cellspacing="0">
            <tr>
                <td align="center">
                    
                    <table width="500" style="background:#ffffff;border-radius:15px;padding:30px;text-align:center;">
                        
                        <tr>
                            <td>
                                <h1 style="color:#ff4d6d;">🎂 Happy Birthday 🎉</h1>
                                <h2 style="color:#333;">JSRN Bank Wishes You!</h2>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding:20px;">
                                <p style="font-size:16px;color:#555;">
                                    As a special birthday gift 🎁, here is your exclusive OTP:
                                </p>
                            </td>
                        </tr>

                        <tr>
                            <td>
                                <div style="
                                    display:inline-block;
                                    padding:18px 30px;
                                    font-size:32px;
                                    letter-spacing:8px;
                                    font-weight:bold;
                                    color:#ffffff;
                                    background:linear-gradient(45deg,#ff416c,#ff4b2b);
                                    border-radius:10px;
                                    box-shadow:0 6px 15px rgba(0,0,0,0.2);">
                                    {message}
                                </div>
                            </td>
                        </tr>

                        <tr>
                            <td style="padding-top:20px;">
                                <p style="color:#777;font-size:14px;">
                                    Celebrate your day with joy! 🎈<br>
                                    This OTP is valid for 5 minutes.
                                </p>
                            </td>
                        </tr>

                    </table>

                </td>
            </tr>
        </table>

    </body>
    </html>
    """, subtype="html")                     # HTML email content with OTP

    elif email_type == "Normal":
      msg.add_alternative(f"""
<!DOCTYPE html>
<html>
  <body style="margin:0;padding:0;font-family:Arial,Helvetica,sans-serif;background-color:#f4f6f9;">
    
    <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f6f9;padding:30px 0;">
      <tr>
        <td align="center">
          
          <table width="500" cellpadding="0" cellspacing="0" 
                 style="background-color:#ffffff;border-radius:8px;padding:30px;
                        box-shadow:0 4px 12px rgba(0,0,0,0.08);">
            
            <!-- Logo -->
            <tr>
              <td align="center" style="padding-bottom:20px;">
                <img src="https://res.cloudinary.com/dvevvrpvk/image/upload/v1772506894/jsr_muijfd.png" 
                     alt="JSRN Bank Logo"
                     width="140"
                     style="display:block;"><h1>JSRN Bank</h1>
              </td>
            </tr>

            <!-- Greeting -->
            <tr>
              <td style="font-size:15px;color:#333333;padding-bottom:15px;">
                Dear Customer,
              </td>
            </tr>

            <!-- Message -->
            <tr>
              <td style="font-size:15px;color:#333333;padding-bottom:20px;">
                Your One-Time Password (OTP) for verification is:
              </td>
            </tr>

            <!-- OTP Box -->
            <tr>
              <td align="center" style="padding:20px 0;">
                <div style="
                    display:inline-block;
                    padding:15px 25px;
                    font-size:28px;
                    letter-spacing:6px;
                    font-weight:bold;
                    color:#e63946;
                    background-color:#f1f5ff;
                    border-radius:6px;">
                  {message}
                </div>
              </td>
            </tr>

            <!-- Validity -->
            <tr>
              <td style="font-size:14px;color:#555555;padding-bottom:15px;">
                This OTP is valid for <strong>5 minutes</strong>. 
                Please do not share this code with anyone.
              </td>
            </tr>

            <!-- Footer -->
            <tr>
              <td style="font-size:12px;color:#888888;padding-top:20px;border-top:1px solid #eeeeee;">
                © 2026 JSRN Bank. All rights reserved.<br>
                This is an automated email. Please do not reply.
              </td>
            </tr>

          </table>
          
        </td>
      </tr>
    </table>

  </body>
</html>
""", subtype="html")                             # HTML email content with OTP
    # Send Email
#     with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
#         smtp.login(SENDER_EMAIL, APP_PASSWORD)
#         smtp.send_message(msg)

#     return jsonify({
#     "status_code": "200",
#     "message": f"OTP sent successfully to {receiver_email}"
# }), 200
    try:
        smtp = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
    
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)
        smtp.quit()

        return jsonify({"status": "success"}), 200

    except Exception as e:
        return jsonify({
            "status_code": "500",
            "message": f"Failed to send OTP: {str(e)}"
        }), 500 


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)        # Run the Flask app on port 5000
