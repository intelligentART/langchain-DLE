# File for utilities
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from utils.default_utils import *

from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import AIMessage, HumanMessage, SystemMessage

load_dotenv(find_dotenv())


def draft_email(user_input, name="<name>", tone=None):
    # Identify the tone to be used
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
    # Identify the user's intended tone for the bot if it exists
    messages = [
    SystemMessage(
        content=f"You are a helpful assistant that identifies the user's intended to be used on the email based on the user's text if they explicitly mentioned a tone profile. Refer to this JSON for the list of tones based on profiles {tone_character} and only output the key of the intended tone and nothing else. If it's unknown or no tone profile was mentioned, simply output `unknown`"
        ),
    HumanMessage(
        content=user_input
        ),
    ]
    tone = chat(messages).content
    print("The Email tone is:", tone)

    # Check if the mentioned tone is in the character
    if tone.lower() in tone_character:
        tone = tone_character[tone]
    else:
        tone = 'efficient and professional'

    print("The Email final tone is:", tone)

    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)
    
    template = """
    
    You are a helpful assistant that drafts an email or a reply.
    
    Your goal is to help the user quickly create a perfect email or reply.
    
    The tone should be {tone}.
    
    Start your reply by saying: "Here's a draft for you, I hope you like it!". And then proceed with the subject on a new line then the email on a next new line.
    
    Make sure to sign of with {signature}.
    
    """

    signature = f"Kind regards, \n\{name}"
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template = "{user_input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    response = chain.run(user_input=user_input, signature=signature, name=name, tone=tone)

    return response

def draft_seo(user_input, tone=None):
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)
    
    template = """
    You are a professional SEO blog writer that writes about a topic that is provided to you.
    You always begin your blogs with a Title (H1 Tag) that creates a catchy and descriptive title that includes the topic name and relevant keywords. 
    You write with a structure that includes Section 1 | Introduction. Section 2 | Topic Overview: Give a brief description about the topic
    Then make your own content for Section 3 to Section 10
    You write with a tone that is warm, enthusiastic, and inviting. It blends practical knowledge with poetic expressions, sharing captivating stories and insights about the topic.
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template = "{user_input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    response = chain.run(user_input=user_input)

    return response

def draft_socmed(user_input, tone=None):
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)
    
    template = """
    You are a professional Social Media Marketer that writes incredible posts based on the user's topic.
    The posts that you create are awe inspiring, informative and very interesting
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template = "{user_input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    response = chain.run(user_input=user_input)

    return response

def default_answer(user_input, tone=None):
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)
    
    template = """
    You are a the best professional assistant that helps the user with their request as long as it is bounded ethically.
    Answer the inquiry or request of the user the best way you can
    """

    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template = "{user_input}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    response = chain.run(user_input=user_input)

    return response

def predict_task(user_input):
    # Get the task needed
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    # Identify the user's intended task for the bot
    messages = [
    SystemMessage(
        content=f"You are a helpful assistant that identifies the user's intended task based on the user's text. Refer to this list of tasks {tasks} and only output the intent task nothing else. If it's unknown, simply output `unknown`"
        ),
    HumanMessage(
        content=user_input
        ),
    ]

    # get the task
    print("The text is:", user_input)
    task = chat(messages).content
    print("The task is:", task)

    # Run the task
    if 'email' in task.lower():
        return draft_email(user_input=user_input)
    if 'seo' in task.lower():
        return draft_seo(user_input=user_input)
    if 'social media' in task.lower():
        return draft_socmed(user_input=user_input)
    else:
        return default_answer(user_input=user_input)

    
    # return f"the task you wanna do is: {task}"


