

from agent_callback_manager import AgentCallbackManager
from agent_callback_handler import AgentCallbackHandler
from streamlit_agent_callback_manager import StreamlitAgentCallbackManager
from streamlit_agent_callback_handler import StreamlitAgentCallbackHandler



def create_agent_manager() -> AgentCallbackManager:
    agent_call_back_handler = AgentCallbackHandler()
    return AgentCallbackManager(handlers=[agent_call_back_handler])

def create_streamlit_agent_manager(st) -> AgentCallbackManager:
    agent_call_back_handler = StreamlitAgentCallbackHandler(st)
    return StreamlitAgentCallbackManager(st, handlers=[agent_call_back_handler])