from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent import AgentExecutor

from agent_factory import create_streamlit_agent_manager
from dotenv import load_dotenv

from log_setup import setup_log

import streamlit as st
import traceback

logger = setup_log('wiki-arxiv-agent')

load_dotenv()

class Config():
    model = 'gpt-3.5-turbo-16k'
    # model = 'gpt-4'
    llm = ChatOpenAI(model=model, temperature=0)

cfg = Config()

title = "Wikipedia / Arxiv Agent"
st.set_page_config(page_title=title)
st.header(title)

@st.cache_resource()
def init_agent() -> AgentExecutor:
    tools = load_tools(["wikipedia", "arxiv"], llm=cfg.llm)
    agent = initialize_agent(
        tools, 
        cfg.llm, 
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, 
        verbose=True,
        callback_manager=create_streamlit_agent_manager(st)
    )
    return agent

if __name__ == "__main__":
    agent = init_agent()
    user_question = st.text_input("Your question to wiki / arxiv")
    if user_question:
        with st.spinner('Please wait ...'):
            try:
                res = agent.run(user_question)
                st.write(f"""
### Answer:
{res}                     
""")
            except Exception as e:
                st.error(f"Failed to process: {e}")
                traceback.print_exc()
        