LangChain SQL Database Chatbot

An AI-powered SQL Database Chatbot built using LangChain, Groq, Streamlit, SQLite, and MySQL.

This application allows users to interact with structured database information using natural-language questions instead of manually writing SQL queries.

The application uses a LangChain SQL Agent with tool calling to understand the user's question, generate the appropriate SQL query, retrieve information from the database, and return a natural-language response.

🚀 Project Overview

Working with databases traditionally requires users to know SQL syntax. This project provides a conversational interface where users can simply ask questions such as:

"How many employees are there?"

"Show me the employees from the sales department."

"What is the average salary?"

The LangChain SQL Agent interprets the question and interacts with the connected database to generate an appropriate answer.

The application supports two database options:

SQLite – using a local company.db database

MySQL – connecting to a user-provided MySQL database

✨ Features

🤖 Natural-language interaction with SQL databases

🔗 LangChain SQL Agent

🧠 Groq-powered LLM

🗄️ SQLite database support

🐬 MySQL database support

🛠️ SQLDatabaseToolkit for database tools

🔧 Tool-calling agent architecture

💬 Streamlit chat interface

📊 Interactive database querying

🔐 API keys entered securely through Streamlit password fields

📝 Chat history using Streamlit session state

🔄 Clear previous conversation history

📡 LangSmith monitoring and observability

⚡ Dynamic SQL query generation

🏗️ Architecture

                    ┌──────────────────────┐
                    │      User Query      │
                    │ "Show total sales"   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Streamlit       │
                    │    Chat Interface    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    LangChain SQL     │
                    │        Agent         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  SQLDatabaseToolkit  │
                    │   Database Tools     │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    ▼                      ▼
             ┌─────────────┐       ┌─────────────┐
             │   SQLite    │       │    MySQL    │
             │ company.db  │       │   Database  │
             └─────────────┘       └─────────────┘
                    │                      │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │    Query Result      │
                    └──────────┬───────────┘
                               ▼
                    ┌──────────────────────┐
                    │ Natural Language     │
                    │      Response        │
                    └──────────────────────┘

                         ┌──────────────┐
                         │  LangSmith   │
                         │ Monitoring &  │
                         │ Observability │
                         └──────────────┘

🧰 Technologies Used

Technology

Purpose

Python

Core programming language

LangChain

Agent and LLM orchestration

LangChain SQL Agent

Natural-language database interaction

Groq

Large Language Model inference

Streamlit

Web-based user interface

SQLite

Local database

MySQL

External relational database

SQLAlchemy

Database connection and engine management

LangSmith

LLM application monitoring and observability

python-dotenv

Environment variable management

📦 Project Structure

project/
│
├── part3.py
├── company.db
├── .env
├── requirements.txt
└── README.md

⚙️ How It Works

1. Load environment variables

The project uses python-dotenv to load environment variables from the .env file.

load_dotenv()

2. Select a database

The Streamlit sidebar allows the user to choose between:

SQLite3 Database
        OR
MySQL Database

For SQLite, the application connects to the local:

company.db

For MySQL, the user provides:

MySQL hostname

Username

Password

Database name

3. Initialize the LLM

The application uses Groq through LangChain's ChatGroq interface.

model = ChatGroq(
    model="openai/gpt-oss-20b",
    groq_api_key=groq_api,
    temperature=0
)

A temperature of 0 is used to make database-related responses more deterministic.

4. Create the SQL Database Toolkit

LangChain's SQLDatabaseToolkit provides the agent with tools for interacting with the database.

toolkit = SQLDatabaseToolkit(
    db=db,
    llm=model
)

5. Create the SQL Agent

The project creates a tool-calling SQL Agent:

agent = create_sql_agent(
    llm=model,
    toolkit=toolkit,
    verbose=True,
    agent_type="tool-calling"
)

The agent can interpret a user's natural-language question and use database tools to obtain the required information.

6. Ask questions through Streamlit

Users can enter questions through the Streamlit chat interface:

user_query = st.chat_input(
    "Ask anything from the database"
)

The query is then passed to the SQL Agent:

response = agent.invoke(
    {"input": user_query}
)

The final response is displayed to the user.

📡 LangSmith Monitoring

LangSmith is used for monitoring and observability of the LangChain application.

It can help track:

LLM calls

Agent execution

Tool calls

SQL Agent behavior

Execution traces

Latency

Errors

Token usage

Intermediate steps

This is especially useful for debugging an agent-based application because the developer can inspect what happened between the user's question and the final response.

Typical LangSmith environment configuration can be added to .env:

LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=SQL-Database-Chatbot

Make sure your actual LangSmith configuration matches the version of LangChain/LangSmith packages used in your project.

🔑 Environment Variables

Create a .env file in the project directory.

Example:

GROQ_API_KEY=your_groq_api_key

LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_PROJECT=SQL-Database-Chatbot

Never upload your .env file or API keys to GitHub.

Add this to .gitignore:

.env
__pycache__/
*.pyc

📥 Installation

Clone the repository:

git clone <your-github-repository-url>

Move into the project directory:

cd <project-folder>

Create a virtual environment:

python -m venv venv

Activate it on macOS/Linux:

source venv/bin/activate

Install dependencies:

pip install -r requirements.txt

▶️ Run the Application

Start the Streamlit application:

streamlit run part3.py

The application will open in your browser.

💡 Example Queries

Once connected to a database, users can ask questions such as:

How many employees are in the company?

Show me all employees.

What is the average salary?

Which department has the highest number of employees?

Show employees with a salary greater than 50000.

What is the total number of employees?

The SQL Agent converts the natural-language request into the appropriate database interaction.

🔐 Security Considerations

SQL Agents should not be given unrestricted access to production databases.

Potential risks include:

Accidental data modification

Accidental deletion

Exposure of sensitive information

Unauthorized database access

Generation of unsafe SQL queries

For production applications:

Use read-only database credentials where possible.

Restrict database permissions.

Never expose database passwords in source code.

Store API keys in environment variables or a secrets manager.

Validate and monitor generated queries.

Avoid connecting the agent directly to sensitive production databases.

🧠 Key Concepts Learned

This project demonstrates several important GenAI and LangChain concepts:

SQL Agent

An SQL Agent allows an LLM to interact with a relational database and dynamically determine which database operations are required.

Tool Calling

The agent uses tools to interact with the database rather than generating an answer based only on its internal knowledge.

SQLDatabaseToolkit

LangChain provides database-specific tools that allow the agent to inspect and query SQL databases.

RAG vs SQL Agent

SQL Agent:

Natural Language
       ↓
SQL Agent
       ↓
SQL Query
       ↓
Structured Database
       ↓
Answer

RAG:

User Question
       ↓
Retriever
       ↓
Relevant Documents
       ↓
LLM
       ↓
Answer

A SQL Agent is particularly useful for structured data stored in relational databases, while RAG is commonly used for retrieving information from documents and other unstructured or semi-structured sources.

📊 Project Insights

Why are SQL Agents better than manual SQL generation?

SQL Agents allow users to ask questions in natural language instead of manually writing SQL queries. They can dynamically generate the necessary database queries, reducing manual effort and making database interaction more accessible.

Difference between SQL Agent and RAG

A SQL Agent works with structured data stored in databases and generates SQL queries to retrieve information.

RAG retrieves relevant information from documents or other sources and uses that information to generate an answer.

Risks of unrestricted SQL access

Unrestricted SQL access can result in:

Unnecessary data modification

Data deletion

Unauthorized access to sensitive information

Security vulnerabilities

Therefore, SQL Agents should be provided with appropriate permissions and access controls.



⭐ Project Highlights

✔ LangChain SQL Agent
✔ Natural Language → SQL
✔ Groq LLM
✔ SQLite + MySQL
✔ Streamlit UI
✔ Tool Calling
✔ LangSmith Monitoring
✔ Database Security Considerations

