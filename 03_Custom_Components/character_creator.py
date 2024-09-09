import argparse

from haystack import component, Pipeline
from haystack.components.builders import PromptBuilder
from haystack_integrations.components.generators.ollama import OllamaGenerator

@component
class CharacterCreator:
    @component.output_types(character_profile=str)
    def run(self, user_name: str, role: str, trait: str):
        profile = f"{user_name} is a {role} known for their {trait}. They are embarking on a great adventure."
        return {"character_profile": profile}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default="mistral")
    parser.add_argument('--user_name', type=str, default="Efren", help="The name of the hero")
    parser.add_argument('--role', type=str, default="warrior", help="The role of the hero in the adventure")
    parser.add_argument('--trait', type=str, default="bravery", help="A key trait of the hero")
    parser.add_argument('--scenario', type=str, default="a mysterious forest", help="Starting scenario for the adventure")
    args = parser.parse_args()
    
    template = """You are the hero of this adventure. 
    Your journey begins in {{ scenario }}.
    Character Details: {{ character_profile }}
    
    Here is the beginning of your adventure:
    What happens next:
    """
    
    character_creator = CharacterCreator()
    prompt = PromptBuilder(template=template)
    llm = OllamaGenerator(model=args.model, timeout=1200)
    
    adventure_pipeline = Pipeline()
    adventure_pipeline.add_component("character_creator", character_creator)
    adventure_pipeline.add_component("prompt", prompt)
    adventure_pipeline.add_component("llm", llm)
    adventure_pipeline.connect("character_creator.character_profile", "prompt.character_profile")
    adventure_pipeline.connect("prompt", "llm")
    
    adventure_pipeline.draw("adventure_pipeline.png")
    
    adventure = adventure_pipeline.run({
        "character_creator": {
            "user_name": args.user_name, 
            "role": args.role, 
            "trait": args.trait
        }, 
        "prompt": {
            "scenario": args.scenario
        }
    })
    print(adventure["llm"]["replies"][0])

if __name__ == "__main__":
    main()