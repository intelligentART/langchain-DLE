from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import find_dotenv, load_dotenv
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

load_dotenv(find_dotenv())


def draft_email(name="Your name here", subject=None, tone=None, email_body=None):
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=1)

    if tone == None:
        tone = 'Keep your reply short and to the point and mimic the style of the email so you reply in a similar manner to match the tone.'
    else:
        tone = f'The tone of your email should be: {tone}'
    if subject == None:
        subject = ""
    else:
        subject = f"The subject of the email is: {subject}"
    
    if email_body != None:
        email_body = f"Base the email that you will craft on this email: {email_body}"
    else:
        email_body = "Please draft a professional email"
    

    template = """
    
    You are a helpful assistant that drafts an email or a reply.
    
    Your goal is to help the user quickly create a perfect email reply.

    {subject}
    
    {tone}
    
    Start your reply by saying: "Here's a draft for you, I hope you like it!". And then proceed with the email on a new line.
    
    Make sure to sign of with {signature}.
    
    """

    signature = f"Kind regards, \n\{name}"
    system_message_prompt = SystemMessagePromptTemplate.from_template(template)

    human_template = "{email_body}"
    human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    chain = LLMChain(llm=chat, prompt=chat_prompt)
    response = chain.run(email_body=email_body, signature=signature, name=name, tone=tone, subject=subject)

    return response