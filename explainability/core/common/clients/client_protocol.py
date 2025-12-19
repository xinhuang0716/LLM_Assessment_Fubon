from typing import Protocol

class LLMClientProtocol(Protocol):
    '''
    LLMClientProtocol 的 Docstring
    '''

    async def generate(self, prompt: str, system: str):
        '''
        Generate response from LLM.
        
        Args:
            prompt: User prompt
            system: Optional system message
        '''
    async def aclose(self):
        '''
        Close client resources.
        '''