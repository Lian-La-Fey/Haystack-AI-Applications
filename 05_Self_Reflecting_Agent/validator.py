from typing import List
from colorama import Fore
from haystack import component

@component
class EntitiesValidator:
    @component.output_types(entities_to_validate=str, entities=str)
    def run(self, replies: List[str]):
        if 'DONE' in replies[0]:
            return {"entities": replies[0].replace('DONE', '')}
        
        print(Fore.RED + "Reflecting on entities\n", replies[0])
        return {"entities_to_validate": replies[0]}    
