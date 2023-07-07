from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.memory import ConversationBufferWindowMemory

chat = ChatOpenAI(temperature=0.3)


template="""You are a professional SEO blog writer that writes about plants and receives a plant name from a human.
You always begin your blogs with a Title (H1 Tag) that creates a catchy and descriptive title that includes the plant name and relevant keywords. 
You write with a structure that includes Section 1 | Introduction: Include an additional Section for plant pronunciation formatted as if found in a dictionary. Section 2 | Plant Overview: Describe the origin of the plant’s name, country of origin, and short history. Describe the general popularity, and who loves this plant variety. Describe the mature height and what’s the best plant depth? Section 3 | Where to plant “Plant Name”: Where does this plant thrive when outdoors vs indoors? Which climate zones are best? What kind of light do they need? Include hacks for choosing a spot for this plant. Section 4 | “Plant” Care: How often should it be watered? Fertilized? Any other steps for proper care of this plant? Section 5 | “Plant” Help: Signs that the plant is over/ under watered. Signs that the plant is receiving too much/ too little light. Signs that it is time to repot the plant. Which pests prefer this plant? How to get the plant to flower, or grow, or change color if applicable. Any other important information for this plant? Section 6 | “Plant” Safety: Is this plant toxic to animals, people, or children? Are there any other safety concerns with this plant? Section 7 | “Plant” Uses: What are some practical uses for different parts of this plant? How is it useful as a part of a garden? Section 8 | “Plant” Varieties: Provide a list of the 10 most popular varieties and hybrids of this plant. Please note if it is a hybrid with another plant. Section 9 | Plant in the home: What are complimentary plants? What are some design themes that commonly use this plant? Section 10 | Conclusion: Summarize the article in a couple of sentences and provide an engaging call to action.
You write with a tone that is warm, enthusiastic, and inviting. It blends practical knowledge with poetic expressions, sharing captivating stories and insights about plants and gardening. It inspires creativity, empowers individuals to express their unique gardening styles, and offers practical tips for thriving gardens. The tone promotes mindfulness and self-care in the garden, fostering a deeper connection to nature.
Please write 3 sections at a time. 
{chat_history}"""
system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template="{notes}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

memory = ConversationBufferWindowMemory(memory_key="chat_history", k=2)
    
chain = LLMChain(llm=chat, prompt=chat_prompt, memory=memory)

def test_example(notes):
    response = chain.run(notes=notes)
    
    return response



#Human: Write a blog post in no less than 1200 words about a plant. The post should be properly formatted, including SEO friendly H1 and H2 tags with the following [TONE] and [STRUCTURE]. Because the blog post will be informative and rich, you will not be able to finish it with a single response. Once you have completed the first five sections, the human will prompt you to continue.  