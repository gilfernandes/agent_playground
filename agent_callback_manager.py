from typing import List, Optional, Dict, Any
from langchain.callbacks.base import BaseCallbackManager, BaseCallbackHandler
from uuid import UUID
from langchain.schema import (
    BaseMessage,
)

from log_setup import setup_log

logger = setup_log('wiki-agent-callback-manager')


class AgentCallbackManager(BaseCallbackManager):
    """Base callback manager that can be used to handle callbacks from LangChain."""

    def __init__(
        self,
        handlers: List[BaseCallbackHandler],
        inheritable_handlers: Optional[List[BaseCallbackHandler]] = None,
        parent_run_id: Optional[UUID] = None,
    ) -> None:
        """Initialize callback manager."""
        super().__init__(handlers=handlers, inheritable_handlers=inheritable_handlers, parent_run_id=parent_run_id)

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when LLM starts running."""
        logger.info("LLM starting")

    def on_chat_model_start(
        self,
        serialized: Dict[str, Any],
        messages: List[List[BaseMessage]],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when a chat model starts running."""
        logger.info("Chat model started")

    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when chain starts running."""
        logger.info("Chain started")

    def on_tool_start(
        self,
        serialized: Dict[str, Any],
        input_str: str,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        """Run when tool starts running."""
        logger.info("Tool started")