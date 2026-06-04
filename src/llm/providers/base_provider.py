from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):

    @abstractmethod
    def extract_intent(
        self,
        prompt: str
    ):
        pass