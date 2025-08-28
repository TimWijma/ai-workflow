import httpx
from litellm import completion

class Step:
    def __init__(self, config):
        self.config = config

    def run(self, context):
        raise NotImplementedError

class GetDataFromAPI(Step):
    def run(self, context):
        url = self.config.get('url')
        if not url:
            raise ValueError("API URL is not defined in the step config")
        
        response = httpx.get(url)
        response.raise_for_status()
        context['data'] = response.json()
        return context

class CallLLM(Step):
    def run(self, context):
        prompt = self.config.get('prompt')
        if not prompt:
            raise ValueError("Prompt is not defined in the step config")

        messages = [
            {"role": "user", "content": prompt.format(**context)},
        ]

        response = completion(model="gpt-3.5-turbo", messages=messages)
        context['llm_response'] = response.choices[0].message.content
        return context

STEP_TYPES = {
    'api': GetDataFromAPI,
    'llm': CallLLM,
}

def execute_workflow(flow, steps):
    context = {}
    for step in steps:
        if step.type not in STEP_TYPES:
            raise ValueError(f"Unknown step type: {step.type}")
        step_executor = STEP_TYPES[step.type](step.config)
        context = step_executor.run(context)
    return context
