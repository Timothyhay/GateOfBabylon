
from typing import Any, Dict, Iterator, List, Mapping, Optional

import requests
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.outputs import GenerationChunk


class AtomChat(LLM):
    """A chat model call Llama Family's Llama 3 based model via API.

    Example:

        .. code-block:: python

            model = AtomChat(n=2)
            result = model.invoke([HumanMessage(content="hello")])
            result = model.batch([[HumanMessage(content="hello")],
                                 [HumanMessage(content="world")]])
    """
    selected_model: str
    api_key: str
    n: int
    max_tokens: int
    temperature: float


    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """Run the LLM on the given input.

        Override this method to implement the LLM logic.

        Args:
            prompt: The prompt to generate from.
            stop: Stop words to use when generating. Model output is cut off at the
                first occurrence of any of the stop substrings.
                If stop tokens are not supported consider raising NotImplementedError.
            run_manager: Callback manager for the run.
            **kwargs: Arbitrary additional keyword arguments. These are usually passed
                to the model provider API call.

        Returns:
            The model output as a string. Actual completions SHOULD NOT include the prompt.
        """
        header = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key
        }

        body = {
            "model": self.selected_model if self.selected_model else "Atom-13B-Chat",
            "messages": [{
                "role": "user",
                "content": prompt
            }],
            "temperature": self.temperature if self.temperature else 0.3,
            "stream": False
        }

        response = requests.post(url="https://api.atomecho.cn/v1/chat/completions", headers=header, data=body, timeout=30, verify=False)

        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        return response

    def _stream(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[GenerationChunk]:
        """Stream the LLM on the given prompt.

        This method should be overridden by subclasses that support streaming.

        If not implemented, the default behavior of calls to stream will be to
        fallback to the non-streaming version of the model and return
        the output as a single chunk.

        Args:
            prompt: The prompt to generate from.
            stop: Stop words to use when generating. Model output is cut off at the
                first occurrence of any of these substrings.
            run_manager: Callback manager for the run.
            **kwargs: Arbitrary additional keyword arguments. These are usually passed
                to the model provider API call.

        Returns:
            An iterator of GenerationChunks.
        """
        for char in prompt[: self.n]:
            chunk = GenerationChunk(text=char)
            if run_manager:
                run_manager.on_llm_new_token(chunk.text, chunk=chunk)

            yield chunk

    @property
    def _identifying_params(self) -> Dict[str, Any]:
        """Return a dictionary of identifying parameters."""
        return {
            "default_model": "Atom-13B-Chat",
            "method": "API",
            "optional_model": ["Atom-13B-Chat", "Atom-7B-Chat", "Atom-1B-Chat", "Llama3-Chinese-8B-Instruct"]
        }

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model. Used for logging purposes only."""
        return "meta-llama/Meta-Llama-3-70B-Instruct"

