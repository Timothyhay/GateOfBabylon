
import requests
import user_token
import corpus.bubbletea_menu as bbt
from typing import Any, Dict, Iterator, List, Mapping, Optional

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.llms import LLM
from langchain_core.outputs import GenerationChunk


class Llama3_70BRev(LLM):
    """A custom chat model that echoes the first `n` characters of the input.

    Example:

        .. code-block:: python

            model = CustomChatModel(n=2)
            result = model.invoke([HumanMessage(content="hello")])
            result = model.batch([[HumanMessage(content="hello")],
                                 [HumanMessage(content="world")]])
    """

    n: int
    """The number of characters from the last message of the prompt to be echoed."""
    max_tokens: int
    temperature: float
    top_p: float


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
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        return prompt[: self.n]

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
            "model_name": "meta-llama/Meta-Llama-3-70B-Instruct",
            "method": "API"
        }

    @property
    def _llm_type(self) -> str:
        """Get the type of language model used by this chat model. Used for logging purposes only."""
        return "meta-llama/Meta-Llama-3-70B-Instruct"


system_prompt = "你是一个奶茶店店长，可以礼貌地根据用户需求推荐他们的产品。并将结果翻译成中文。"
menu_prompt = "店内产品和介绍如下：" + bbt.coco_menu_raw
final_system_prompt = system_prompt + menu_prompt

user_prompt = "我想喝带巨峰葡萄和柠檬的水水！"

data = {
    "messages": [
        {
            "role": "system",
            "content": final_system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ],
    "model": "meta-llama/Meta-Llama-3-70B-Instruct",
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.9
}

response = requests.post(user_token.url, headers=user_token.headers, json=data)
answer_json = response.json()
print(answer_json)
print(answer_json["choices"][0]["message"]["content"])