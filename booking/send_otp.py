"""
 * Send an SMS message using the Infobip API.
 *
 * This example is already pre-populated with your account data:
 * 1. Your account Base URL
 * 2. Your account API key
 * 3. Your recipient phone number
 *
 * THIS CODE EXAMPLE IS READY BY DEFAULT. HIT RUN TO SEND THE MESSAGE!
 *
 * Send sms API reference: https://www.infobip.com/docs/api#channels/sms/send-sms-message
 * See Readme file for details.
"""

from infobip_channels.sms.channel import SMSChannel

BASE_URL = "https://vv1yd1.api.infobip.com"
API_KEY = "1f9d940b581346389b8b853128de460c-b4c1a547-e85a-42d2-b32f-5ef8696765d0"
RECIPIENT = "919657847644"


def main():
    # Initialize the SMS channel with your credentials.
    channel = SMSChannel.from_auth_params(
        {
            "base_url": BASE_URL,
            "api_key": API_KEY,
        }
    )

    # Send a message with the desired fields.
    sms_response = channel.send_sms_message(
        {
            "messages": [
                {
                    "destinations": [{"to": RECIPIENT}],
                    "text": "Hello, from Python SDK!",
                }
            ]
        }
    )

    # Get delivery reports for the message. It may take a few seconds show the just-sent message.
    query_parameters = {"limit": 10}
    delivery_reports = channel.get_outbound_sms_delivery_reports(query_parameters)

    # See the delivery reports.
    print("message:",delivery_reports)


if __name__ == "__main__":
    main()
