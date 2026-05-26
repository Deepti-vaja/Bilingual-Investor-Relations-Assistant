from langchain_core.prompts import PromptTemplate

def get_chat_prompt() -> PromptTemplate:
    """
    Returns a generalized LangChain PromptTemplate for answering business queries.
    We pass {context}, {query}, and {language} variables at runtime.
    """
    template = """<|system|>
    You are an expert bilingual financial assistant.

    Rules:
    - Answer ONLY using the provided context. Do NOT guess.
    - Maintain accuracy (finance-sensitive facts).
    - Answer natively in the user's language: {language}
    - Structure answer clearly:
        1. Key Answer in strictly 1 or 2 sentences
        2. Supporting Details (optional, keep short)
        3. Source references
    - If missing info: say "Information not available in the documents"
    </s>
    <|user|>
    Context:
    {context}

    Question:
    {query}
    </s>
    <|assistant|>
    """
    return PromptTemplate(
        input_variables=["context", "query", "language"],
        template=template
    )

def format_docs(docs_and_scores) -> str:
    """Combines retrieved documents into a single contextual string."""
    return "\n\n".join(doc.page_content for doc, _score in docs_and_scores)
