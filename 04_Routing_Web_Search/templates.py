rag_prompt_template = """
Answer the following query given the documents.
If the answer is not contained within the documents, reply with only just using 'no_answer'. Do not write other than the 'no_answer' if the answer is not contained within the documents.
Query: {{query}}
Documents:
{% for document in documents %}
    {{document.content}}
{% endfor %}
"""

websearch_prompt_template = """
Answer the following query given the documents retrieved from the web.
Your answer should indicate that your answer was generated from websearch.
You can also reference the URLs that the answer was generated from

Query: {{query}}
Documents:
{% for document in documents %}
    {{document.content}}
{% endfor %}
"""