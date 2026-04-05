from langchain.agents import create_agent
from langchain_community.tools import Tool
from langchain_openai import ChatOpenAI
from dotenv.ipython import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_core.tools import create_retriever_tool

load_dotenv(override=True)


chunks = [
   "Je m'appelle Oussama Issib, je suis un ingénieur logiciel dans le département d'ingénierie. Mon adresse e-mail est john.doe@company.com.",
   "Je travaille dans le département d'ingénierie.",
   "En plus de l'ingénierie, je suis également impliqué dans des projets de recherche et développement.",
   "Je suis d origine tunisienne et j'ai étudié à l'Université de Tunis. J'ai une passion pour la technologie et l'innovation, et je suis toujours à la recherche de nouvelles opportunités pour apprendre et grandir dans ma carrière.",
   "Je suis un ingénieur logiciel expérimenté avec une solide expérience dans le développement de logiciels, la gestion de projets et la collaboration interfonctionnelle. J'ai travaillé sur divers projets, allant du développement d'applications web à la création de solutions logicielles personnalisées pour les clients. Je suis également compétent dans plusieurs langages de programmation et frameworks, ce qui me permet de m'adapter rapidement aux nouvelles technologies et de résoudre efficacement les problèmes techniques."
]


embedding_model = OpenAIEmbeddings()

vector_store = Chroma.from_texts(
    texts=chunks,
    embedding=embedding_model,
    collection_name="employee_db"
)


retriever = vector_store.as_retriever()
retriever_tool = create_retriever_tool(
    retriever,
    name="cv_tool",
    description="Get Information about me from my CV. Use this tool to get information about me from my CV. You can ask questions about my background, experience, skills, and any other relevant information that may be included in my CV.")


@tool
def get_employee_info(name: str):
    """Get employee information about a given employee. (e.g. name, position, department, email, salary)"""
    print("Get employee info tool invoked")
    return {
        "name": name,
        "position": "Software Engineer",
        "department": "Engineering",
        "email": f"{name.lower()}@company.com",
        "salary": "$100,000"
    }

@tool
def send_email(email: str, subject: str, content: str):
    """Send an email to a given recipient with a subject and content."""
    print("Sending email tool invoked")
    return f"Email successfully sent to {email} with subject '{subject}' and content '{content}'"



llm=ChatOpenAI(model="gpt-4o", temperature=0)

agent = create_agent(
    model=llm,
    tools=[get_employee_info, send_email, retriever_tool],
    system_prompt="Answer the user query using the provide tools."
)



#response = agent.invoke(
  #  input={"messages": [HumanMessage("What is the email of John Doe?")]}
  #  )
#print(response["messages"][-1].content)