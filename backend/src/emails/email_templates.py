def create_welcome_email_template(name: str, client_url: str) -> str:
    """Create welcome email template"""
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            h1 {{
                color: #333;
                text-align: center;
            }}
            p {{
                color: #666;
                line-height: 1.6;
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 4px;
                text-align: center;
            }}
            .footer {{
                margin-top: 20px;
                text-align: center;
                color: #999;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to Chatify!</h1>
            <p>Hello {name},</p>
            <p>Thank you for signing up for Chatify. We're excited to have you on board!</p>
            <p>Chatify is a real-time chat application that allows you to communicate with friends and colleagues instantly.</p>
            <p style="text-align: center;">
                <a href="{client_url}" class="button">Start Chatting</a>
            </p>
            <p>If you have any questions, feel free to reach out to us.</p>
            <div class="footer">
                <p>© 2024 Chatify. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
