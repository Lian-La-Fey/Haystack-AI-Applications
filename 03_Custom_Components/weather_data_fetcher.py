import os
import sys
import requests
import argparse

from typing import List
from haystack import Document, component, Pipeline
from haystack.components.builders import PromptBuilder
from haystack_integrations.components.generators.ollama import OllamaGenerator

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env_config import load_env_variables

@component
class WeatherDataFetcher:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    @component.output_types(articles=List[Document])
    def run(self, locations: List[str]):
        articles = []
        for location in locations:
            response = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?units=metric&q={location}&appid={self.api_key}"
            )
            data = response.json()
            if response.status_code == 200 and "weather" in data:
                description = data["weather"][0]["description"]
                temperature = data["main"]["temp"]
                content = f"Weather in {location}: {description}, Temperature: {temperature}C"
                articles.append(Document(content=content, meta={"location": location}))
            else:
                print(f"Error fetching data for {location}")
        return {"articles": articles}

def main():
    parser = argparse.ArgumentParser(description='Fetch and summarize weather data.')
    parser.add_argument('--locations', type=str, nargs='+', default=["Corum", "Ankara", "Antalya"],
                        help='List of locations to fetch weather data.')
    parser.add_argument('--model', type=str, default="mistral", help='Name of the model')
    args = parser.parse_args()
    
    load_env_variables()
    
    prompt_template = """
    You will be provided with weather data for different locations.  
    For each location, provide a brief summary of the weather.

    Locations:  
    {% for article in articles %}
      Location:\n
      {{ article.meta["location"] }}: {{ article.content }}
    {% endfor %}  
    """
    
    prompt_builder = PromptBuilder(template=prompt_template)
    fetcher = WeatherDataFetcher(api_key=os.getenv("OPENWEATHER_API_KEY"))
    llm = OllamaGenerator(model=args.model, timeout=1200)

    summarizer_pipeline = Pipeline()
    summarizer_pipeline.add_component("fetcher", fetcher)
    summarizer_pipeline.add_component("prompt", prompt_builder)
    summarizer_pipeline.add_component("llm", llm)

    summarizer_pipeline.connect("fetcher.articles", "prompt.articles")
    summarizer_pipeline.connect("prompt", "llm")
    
    summarizer_pipeline.draw("summarizer_pipeline.png")
    
    summaries = summarizer_pipeline.run({"fetcher": {"locations": args.locations}})
    print(summaries["llm"]["replies"][0])

if __name__ == "__main__":
    main()