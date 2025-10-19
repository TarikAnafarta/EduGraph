import datetime


def generate_verification_code():
    """Generate a random 6-digit code."""
    from random import randint

    return f"{randint(100000, 999999)}"


def get_password_reset_email_template(user_name, reset_url):
    """Generate both plain text and HTML email templates for password reset."""
    # Plain text version
    plain_text_message = f"""Hello {user_name},

We received a request to reset your password for your MyCoach account. Click the link below to reset your password:

{reset_url}

If you didn't request a password reset, you can safely ignore this email.

If the link above doesn't work, copy and paste it into your browser.

This link will expire in 30 minutes.

Best regards,
The MyCoach Team
"""

    # HTML version (your existing template)
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Reset Your Password</title>
        <style>
            body {{
                line-height: 1.2;
                color: #333333;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }}
            .container {{
                font-family: 'Roboto', sans-serif;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                padding-bottom: 20px;
                border-bottom: 1px solid #eeeeee;
            }}
            .logo {{
                width: 100px;
            }}
            .content {{
                padding: 30px 20px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 24px;
                background-color: #3B83F7;
                color: #ffffff !important;
                text-decoration: none;
                border-radius: 4px;
                font-weight: 500;
                margin: 20px 0;
                text-align: center;
            }}
            .footer {{
                text-align: center;
                font-size: 12px;
                color: #757575;
                padding-top: 20px;
                border-top: 1px solid #eeeeee;
            }}
            .link {{
                word-break: break-all;
                color: #6200ea;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="content">
                <p>Hello {user_name},</p>
                <p>We received a request to reset your password for your MyCoach account.
                Click the button below to reset your password:</p>

                <div style="text-align: center;">
                    <a href="{reset_url}" class="button">Reset Password</a>
                </div>

                <p>If you didn't request a password reset,
                you can safely ignore this email.</p>

                <p>If the button above doesn't work,
                copy and paste the following link into your browser:</p>
                <p><a href="{reset_url}" class="link">{reset_url}</a></p>

                <p>This link will expire in 30 minutes.</p>

                <p>Best regards,<br>The MyCoach Team</p>
            </div>
            <div class="footer">
                <p>&copy; {datetime.datetime.now().year} MyCoach.
                All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    return plain_text_message, html_message


def get_verification_email_template(user_name, code):
    """Generate both plain text and HTML email templates for verification."""
    # Plain text version
    plain_text = f"""Hello {user_name},

Your verification code for your MyCoach account is: {code}

Please enter this code to activate your account.

This code will expire in 30 minutes.

Best regards,
The MyCoach Team
"""

    # HTML version matching password reset style
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Account Verification</title>
        <style>
            body {{
                line-height: 1.2;
                color: #333333;
                margin: 0;
                padding: 0;
                background-color: #f5f5f5;
            }}
            .container {{
                font-family: 'Roboto', sans-serif;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                padding-bottom: 20px;
                border-bottom: 1px solid #eeeeee;
            }}
            .logo {{
                width: 100px;
            }}
            .content {{
                padding: 30px 20px;
            }}
            .verification-code {{
                background-color: #f5f5f5;
                padding: 15px;
                border-radius: 4px;
                font-size: 24px;
                font-weight: bold;
                letter-spacing: 2px;
                text-align: center;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                font-size: 12px;
                color: #757575;
                padding-top: 20px;
                border-top: 1px solid #eeeeee;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="content">
                <p>Hello {user_name},</p>
                <p>Your verification code for your MyCoach account is:</p>

                <div class="verification-code">
                    {code}
                </div>

                <p>Please enter this code to activate your account.</p>
                <p>This code will expire in 30 minutes.</p>

                <p>Best regards,<br>The MyCoach Team</p>
            </div>
            <div class="footer">
                <p>&copy; {datetime.datetime.now().year} MyCoach. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    return plain_text, html
