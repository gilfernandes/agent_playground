from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.agents.agent import AgentExecutor
from langchain.input import get_colored_text

from prompt_toolkit import HTML, prompt, PromptSession
from prompt_toolkit.history import FileHistory
from agent_factory import create_agent_manager
from chat_output_parser import ExtendedChatOutputParser
from langchain.schema import OutputParserException

import re
import sys
import json

from log_setup import setup_log
from dotenv import load_dotenv

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

logger = setup_log('wiki-agent')

load_dotenv()

class Config():
    """
    Contains the configuration of the LLM.
    """
    model = 'gpt-3.5-turbo-16k'
    # model = 'gpt-4'
    llm = ChatOpenAI(model=model, temperature=0)

cfg = Config()


def action_detector_func(text):
    """
    Method which tries to better understand the output of the LLM.
    :param text: the text coming from the LLM response.
    :return a json string with the name of the tool to query next and the input to that tool.
    """
    splits = text.split("```")
    if len(splits) > 1:
        # Original implementation + json snippet removal
        return re.sub(r"^json", "", splits[1])
    else:
        lower_text = text.lower()
        tool_tokens = ["wiki", "arxiv", "duckduckgo"]
        token_tool_mapping = {
            "wiki": "Wikipedia",
            "arxiv": "arxiv",
            "duckduckgo": "duckduckgo_search"
        }
        for token in tool_tokens:
            if token in lower_text:
                return json.dumps({
                    'action': token_tool_mapping[token],
                    'action_input': text
                })
        raise OutputParserException('Could not find wiki or arxiv or duckduckgo action nor the final answer.')
    

def create_agent_executor(cfg: Config, action_detector_func: callable, verbose: bool = False) -> AgentExecutor:
    """
    Sets up the agent with three tools: wikipedia, arxiv, duckduckgo search
    :param cfg The configuration with the LLM.
    :param action_detector_func A more flexible implementation of the output parser, better at guessing the tool from the response.
    :param verbose whether there will more output on the console or not.
    """
    tools = load_tools(["wikipedia", "arxiv", "ddg-search"], llm=cfg.llm)
    agent_executor: AgentExecutor = initialize_agent(
    tools, 
    cfg.llm, 
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=verbose
)
    agent = agent_executor.agent
    agent.output_parser = ExtendedChatOutputParser(action_detector_func)
    return agent_executor


agent_executor: AgentExecutor = create_agent_executor(cfg, action_detector_func)

if __name__ == "__main__":

    session = PromptSession(history=FileHistory(".agent-history-file"))
    while True:
        question = session.prompt(
            HTML("<b>Type <u>Your question</u></b>  ('q' to exit): ")
        )
        if question.lower() == 'q':
            break
        if len(question) == 0:
            continue
        try:
            print(get_colored_text(agent_executor.run(question), "green"))
        except Exception as e:
            print(get_colored_text("Error occurred in agent", "red"), get_colored_text(str(e), "red"))
            # eprint(traceback.format_exc())