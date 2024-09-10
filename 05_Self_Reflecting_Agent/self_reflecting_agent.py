from haystack import Pipeline
from haystack_integrations.components.generators.ollama import OllamaGenerator

from validator import EntitiesValidator
from template import get_prompt_template

def create_self_reflecting_agent(model: str, timeout: int = 1200):
    prompt_template = get_prompt_template()
    llm = OllamaGenerator(model=model, timeout=timeout)
    entities_validator = EntitiesValidator()

    self_reflecting_agent = Pipeline(max_loops_allowed=10)
    self_reflecting_agent.add_component("prompt_builder", prompt_template)
    self_reflecting_agent.add_component("entities_validator", entities_validator)
    self_reflecting_agent.add_component("llm", llm)

    self_reflecting_agent.connect("prompt_builder.prompt", "llm.prompt")
    self_reflecting_agent.connect("llm.replies", "entities_validator.replies")
    self_reflecting_agent.connect("entities_validator.entities_to_validate", "prompt_builder.entities_to_validate")
    
    self_reflecting_agent.draw("self_reflecting_agent.jpg")

    return self_reflecting_agent
