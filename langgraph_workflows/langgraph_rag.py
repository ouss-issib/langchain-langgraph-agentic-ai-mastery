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


texts = [
   "Je m'appelle Oussama Issib, je suis un ingénieur logiciel dans le département d'ingénierie. Mon adresse e-mail est john.doe@company.com.",
   "J'ai obtenu mon diplôme en informatique de l'Université de Tunis en 2015 et j'ai plus de 8 ans d'expérience dans le développement de logiciels. J'ai travaillé sur divers projets, notamment le développement d'applications web, la création de solutions logicielles personnalisées pour les clients et la gestion de projets techniques.",
   "Je travaille dans le département d'ingénierie.",
   "En plus de l'ingénierie, je suis également impliqué dans des projets de recherche et développement.",
   "Je suis d origine marocin et j'ai étudié à l'Université de ENSET.",
   "Je suis un ingénieur logiciel expérimenté avec une solide expérience dans le développement de logiciels, la gestion de projets et la collaboration interfonctionnelle. J'ai travaillé sur divers projets, allant du développement d'applications web à la création de solutions logicielles personnalisées pour les clients. Je suis également compétent dans plusieurs langages de programmation et frameworks, ce qui me permet de m'adapter rapidement aux nouvelles technologies et de résoudre efficacement les problèmes techniques."
]


embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")

vector_store = Chroma.from_texts(
    texts=texts,
    embedding=embedding_model,
    collection_name="cv_collection"
)


retriever = vector_store.as_retriever(kwargs={"k": 5})
retriever_tool = create_retriever_tool(
    retriever,
    name="kb_search",
    description="Search Information about me")


@tool
def get_employee_info(name: str):
    """Get employee information about a given employee. (e.g. name, position, department, email, salary)"""
    print("*"*80)
    print("Get employee info tool invoked")
    print("*"*80)
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
    print("*"*80)
    print("Sending email tool invoked")
    print("*"*80)
    return f"Email successfully sent to {email} with subject '{subject}' and content '{content}'"



llm=ChatOpenAI(model="gpt-4o", temperature=0)

graph = create_agent(
    model=llm,
    tools=[get_employee_info, send_email, retriever_tool],
    system_prompt="Answer the user query using the provide tools."
)



response = graph.invoke(
   input={"messages": [HumanMessage("What is the salary of oussama?")]}
   )
print(response["messages"][-1].content)