#  Import os module to read environment variables securely from the system

import os

# Import logging to record dispatch status and debugging data in production logs
import logging

# Import httpx to make asynchronous HTTP requests to external services (e.g., resend or SendGrid API)
import httpx

# Configure standard logger to output messsages to the console
logger = logging.getLogger(__name__)

async def send_birthday_email(recipient_email: str, subject: str, body: str) -> bool:
    """Asynchronous server-to-server function that communicates with an external email provider API to sned birthday card notifications."""

    # Define the external API endpoint URL (using Resend API as an example)
    api_url = "https://api.resend.com/v1/emails"

    # Retrieve the API key securely from environment variables (ensure it's never hardcoded)
    api_key = os.getenv("RESEND_API_KEY", "YOUR_RESEND_API_KEY")  # Replace with your actual API key or use environment variables for security

    # Construct the HTTP headers required by the external email provider
    headers = {
        "Authorization": f"Bearer {api_key}", # Bearer token authentication schema
        "Content-Type": "application/json", # Instructs the API to expect JSON payload

    }

    # Construct the unique public URL where the recipient can view their card
    card_view_url = f"https://localhost:8000/cards/{card_uuid}"

    # Construct the JSON payload by the email delivery API
    payload = {
        "from": "Birthday Card App <onboarding@resend.dev>", # verified sender email address
        "to": [recipient_email], # Target recipient email address
        "subject": f"You received a birthday card: {card_title}!", # Dynamic email subject line
        "html": f"<p>Hello!</p><p>Somone sent you a birthday card! You can view it by clicking the link below:</p><p><a href='{card_view_url}'>View Your Birthday Card</a></p><p>Best wishes,</p><p>The Birthday Card App Team</p>", # HTML body content with dynamic link

    }

    # Use httpx AsyncClient to execute a non-blocking POST request to the external email service

    async with httpx.AsyncClient() as client:
        try:
            # Send the HTTP POST reequest with a 10-second timeout to prevent hanging threads
            response = await client.post(api_url, json=payload, headers=headers, timeout=10.0)

            # Check if the HTTP status code indicates success ( 200 OK or 201 Created)
            if response.status_code in [200,201]:
                logger.info(f"Succesfuuly send birthday email to {recipient_email} for card '{card_title}'")
                return True # Return True to indicate successful email dispatch
            else:
                # Log an error if the external API returned a non-success status code
                logger.error(f"Failed to send birthday email to {recipient_email}, status code: {response.status_code}, Body: {response.text}")
                return False # Return False to indicate failure in email dispatch
            
        except httpx.RequestError as exc:
            # Catch network-level exceptions (e.g., DNS failure, connection timeout)
            logger.error(f"An error occurred while sending birthday email to {recipient_email}: {exc}")
            return False # Return False to indicate failure in email dispatch