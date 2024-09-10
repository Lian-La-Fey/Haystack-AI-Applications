import argparse

from colorama import Fore
from self_reflecting_agent import create_self_reflecting_agent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default="gemma2:9b", help='Name of the model')
    args = parser.parse_args()
    
    self_reflecting_agent = create_self_reflecting_agent(model=args.model)
    
    text1 = """
    New York City is the most populous city in the United States, located at the southern tip of the state of New York.
    It is known for its significant impact on commerce, finance, media, art, fashion, research, technology, education, 
    and entertainment. The city is home to over 8 million residents across five boroughs. It is one of the most famous 
    cities in the world and a major tourist destination. Famous landmarks include the Statue of Liberty, Central Park, 
    and the Empire State Building."""

    result1 = self_reflecting_agent.run({"prompt_builder": {"text": text1}})
    print(Fore.GREEN + result1['entities_validator']['entities'])
    
    text2 = """
    Alice: Hey team, let's schedule the next product review meeting for September 10th, 2024.
    Bob: Sounds good! I'll be sure to have the financial report ready by then.
    Charlie: Great, I'll also make sure the development team has the new feature demo prepared.
    Dana: Awesome, we should also have the marketing strategy finalized by that date.
    Alice: Thanks everyone! I'll send out the calendar invites shortly, and we'll sync up on Slack before the meeting."""

    result2 = self_reflecting_agent.run({"prompt_builder": {"text": text2}})
    print(Fore.GREEN + result2['entities_validator']['entities'])

if __name__ == "__main__":
    main()