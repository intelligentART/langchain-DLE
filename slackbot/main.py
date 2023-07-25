import os
import importlib.util
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt import App
from dotenv import find_dotenv, load_dotenv
from flask import Flask, request
# from functions import draft_email

# Load environment variables from .env file
_ =load_dotenv(find_dotenv())

# Set Slack API credentials
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
SLACK_BOT_USER_ID = os.environ["SLACK_BOT_USER_ID"]

# Initialize the Slack app
app = App(token=SLACK_BOT_TOKEN)

# Initialize the Flask app
# Flask is a web application framework written in Python
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)


def get_bot_user_id():
    """
    Get the bot user ID using the Slack API.
    Returns:
        str: The bot user ID.
    """
    try:
        # Initialize the Slack client with your bot token
        slack_client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
        response = slack_client.auth_test()
        return response["user_id"]
    except SlackApiError as e:
        print(f"Error: {e}")

# Make the bot capable of obtaining multiple structures
def run_function(module_name, function_name, *args):
    # the path to the module
    path_to_module = f'structures/{module_name}.py'

    # check if the module exists
    if os.path.exists(path_to_module):
        # load the module
        spec = importlib.util.spec_from_file_location(module_name, path_to_module)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # run the function
        return getattr(module, function_name)(*args)
    else:
        # import the default module and run its function
        import structures.default as default
        return getattr(default, function_name)(*args)



def my_function(text):
    """
    Custom function to process the text and return a response.
    In this example, the function converts the input text to uppercase.

    Args:
        text (str): The input text to process.

    Returns:
        str: The processed text.
    """
    response = text.upper()
    return response


@app.event("app_mention")
def handle_mentions(body, say):
    """
    Event listener for mentions in Slack.
    When the bot is mentioned, this function processes the text and sends a response.

    Args:
        body (dict): The event data received from Slack.
        say (callable): A function for sending a response to the channel.
    """
    team_id = body["team_id"] # Get the slack team id for the structure
    text = body["event"]["text"] # Get the user text
    print(body)
    mention = f"<@{SLACK_BOT_USER_ID}>"
    text = text.replace(mention, "").strip()

    say("Sure, I'll get right on that!")

    # Run the function for prediction task
    response = run_function(team_id, 'predict_task', text)
    say(response)
    # Create 
    # response = my_function(text)
    # response = draft_email(text)
    # say(response)

# @app.command("/email")
# def handle_email(ack, say, command):
#     """
#     Command handler for the /email command in Slack.
#     When the /email command is issued, this function parses the input, handles errors, and sends a response.

#     Args:
#         ack (callable): A function for acknowledging the command.
#         say (callable): A function for sending a response to the channel.
#         command (dict): The command data received from Slack.
#     """
#     # Acknowledge the command
#     ack()
    
#     # Initialize the parameters
#     tone = None
#     subject = None
#     email_body = None

#     # Split the commands via **
#     text = command["text"].strip().split('**')

#     params = {}
#     for line in text:
#         if line:
#             parts = line.split(':')
#             if len(parts) != 2:
#                 say("I'm sorry, you have given me an invalid format. Please use the format: \n **tone: words \n **subject: words \n **email_body: words")
#                 return

#             key, value = parts[0].strip(), parts[1].strip()
#             params[key] = value

#     say("Sure, let me draft an email for you.")
#     if 'tone' in params:
#         say(f"The tone of the email: {params['tone']}")
#         tone = params['tone']
#     if 'subject' in params:
#         say(f"The subject of the email: {params['subject']}")
#         subject = params['subject']
#     if 'email_body' in params:
#         email_body = params['email_body']
#         say(f"The email body: {params['email_body']}")

#     print("Generating GPT Response")
#     response = draft_email(tone=tone, subject=subject, email_body=email_body)
#     print("Returning GPT Response")
#     say(response)
#     say(response)
    # say(f"Sure I'll send you an email with the following: Tone: {params['tone']}, Subject: {params['subject']}, Email: {params['email_body']}")

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    """
    Route for handling Slack events.
    This function passes the incoming HTTP request to the SlackRequestHandler for processing.

    Returns:
        Response: The result of handling the request.
    """
    return handler.handle(request)


# Run the Flask app
if __name__ == "__main__":
    flask_app.run()