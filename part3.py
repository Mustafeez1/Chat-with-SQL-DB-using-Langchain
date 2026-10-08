from sqlalchemy import create_engine
import streamlit as st
from dotenv import load_dotenv
from urllib.parse import quote_plus
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_groq import ChatGroq
from langchain_community.callbacks import StreamlitCallbackHandler
from pathlib import Path
import sqlite3

load_dotenv()

st.title("Langchain: Chat with SQL Database")

LOCALDB = "USE_LOCALDB"
MYSQLDB = "USE_MYSQL"

radio_option = ["use SQLite3 Database(company.db)", "Connect to MYSQL Database"]

selected_option = st.sidebar.radio("choose the db you want to chat with:", options=radio_option)

if selected_option == "Connect to MYSQL Database":
    db_uri = MYSQLDB
    mysql_host = st.sidebar.text_input("provide MYSQL Hostname", value="localhost")
    mysql_user = st.sidebar.text_input("provide MYSQL Username", value="root")
    mysql_password = st.sidebar.text_input("provide MYSQL password", type="password")
    mysql_db = st.sidebar.text_input("provide MYSQL Database name")
    encoded_password = quote_plus(mysql_password)
    connection_str = f"mysql+mysqlconnector://{mysql_user}:{encoded_password}@{mysql_host}/{mysql_db}"
else:
    db_uri = LOCALDB

groq_api = st.sidebar.text_input("enter your groq api key", type="password")

if not groq_api:
    st.write("Enter your api key to proceed")
    st.stop()

model = ChatGroq(model="openai/gpt-oss-20b", groq_api_key=groq_api, temperature=0)

@st.cache_resource(ttl=7200)
def configure_db(db_uri, mysql_host=None, mysql_user=None, mysql_password=None, mysql_db=None):
    if db_uri == LOCALDB:
        dbfilepath = (Path(__file__).parent / "company.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri == MYSQLDB:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MYSQL connections")
            st.stop()
        try:
            db = SQLDatabase(create_engine(connection_str))
            st.success("Successfully connected to mysql database")
            return db
        except Exception as e:
            st.error(f"Failed to connect {e}")
            st.stop()

if db_uri == MYSQLDB:
    db = configure_db(db_uri, mysql_host, mysql_user, mysql_password, mysql_db)
else:
    db = configure_db(db_uri)

toolkit = SQLDatabaseToolkit(db=db, llm=model)

agent = create_sql_agent(llm=model, toolkit=toolkit, verbose=True, agent_type="tool-calling")

if "messages" not in st.session_state or st.sidebar.button("clear previous history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

user_query = st.chat_input("Ask anything from the database")

if user_query:
    st.session_state["messages"].append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        st_callback = StreamlitCallbackHandler(st.container())
        response = agent.invoke({"input": user_query}, {"callbacks": [st_callback]})
        st.write(response["output"])
        st.session_state["messages"].append({"role": "assistant", "content": response["output"]})


### Task 9: Observation and insights

# 1. Why are SQL agents better than manual SQL generation?
# SQL agents can understand questions in natural language and automatically generate the 
# necessary SQL queries for the user query. They reduce manual effort, save time, and can 
# work with the database dynamically.


# 2. Difference between SQL Agent and RAG
# A SQL Agent works with structured data stored in databases and generates SQL queries 
# to retrieve the data. RAG (Retrieval-Augmented Generation) retrieves relevant 
# information from documents or other sources and uses it to generate an answer.

# 3. Risks of allowing unrestricted SQL access
# Unrestricted SQL access can lead to unneccessary data modification or deletion, unauthorized 
# access to sensitive information whichyou dont want the user to see, and security problems. 
# SQL agents should have limited permissions and proper access controls.