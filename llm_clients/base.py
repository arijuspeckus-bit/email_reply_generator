class BaseLLM:
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError("generate() turi būti implementuotas")