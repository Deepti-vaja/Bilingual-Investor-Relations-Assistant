import logging
import sys
from langdetect import detect
from langchain_core.runnables import RunnableLambda

# Local Imports
from _1_load import load_and_clean_data
from _2_chunk import chunk_documents
from _3_vectorstore import get_vectorstores
from _4_prompt import get_chat_prompt, format_docs
from _5_llm import setup_llm, generate_answer
from chat_history import ChatHistoryManager
from models import InferenceRequest

# Set up main console logger
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


def build_conditional_retriever_chain(vectorstore_en, vectorstore_jp):
    """
    Builds a LangChain conditional router to pick the correct retriever based on the detected language.
    This demonstrates an understanding of LangChain Expression Language (LCEL) routing.
    """
    def route_query(inputs: dict) -> list:
        # Pydantic schema validation inside a chain for safety
        req = InferenceRequest(**inputs)
        query = req.query
        
        try:
            lang = detect(query)
            logger.info(f"-> Detected language: {lang}")
        except Exception:
            lang = "en"
            
        if lang == "en":
            return vectorstore_en.similarity_search_with_score(query, k=3)
        else:
            return vectorstore_jp.similarity_search_with_score(query, k=3)
            
    return RunnableLambda(route_query)


def main():
    logger.info("Welcome to the Modular RAG Project Pipeline!")

    # 1. Load Data
    all_docs = load_and_clean_data()
    
    # 2. Chunk Data
    chunked_en, chunked_jp = chunk_documents(all_docs)
    
    # 3. Create VectorStore
    vectorstore_en, vectorstore_jp = get_vectorstores(chunked_en, chunked_jp)

    # 4. Build Conditional LCEL Chain
    # A single chain that handles branching based on language!
    retriever_chain = build_conditional_retriever_chain(vectorstore_en, vectorstore_jp)

    # 5. Initialize Prompt Template & LLM
    prompt_template = get_chat_prompt()
    try:
        llm = setup_llm()
    except Exception as e:
        logger.error(f"Failed to load LLM pipeline: {e}")
        sys.exit(1)

    # 6. Initialize History
    history_manager = ChatHistoryManager()

    logger.info("Pipeline Ready! Type 'exit' to stop.")
    
    # Interactive Loop
    while True:
        try:
            query = input("\nAsk your question (EN/JP): ").strip()
            
            if not query:
                continue
                
            if query.lower() == "exit":
                break

            # 4.1 Route through the Conditional retriever chain
            docs_and_scores = retriever_chain.invoke({"query": query})
            
            # Print chunks and scores safely 
            print("\n--- Retrieved Chunks ---")
            for i, (doc, score) in enumerate(docs_and_scores, 1):
                clean_snippet = doc.page_content.replace('\n', ' ')[:150]
                print(f"Chunk {i} [Score: {score:.4f}]: {clean_snippet}...")
            print("------------------------\n")
            
            context = format_docs(docs_and_scores)
            
            # Simple fallback language detect for prompt instruction
            try:
                lang_str = detect(query) 
            except:
                lang_str = "en"
                
            # 5.1 Format prompt safely via Langchain
            formatted_prompt = prompt_template.format(
                context=context, 
                query=query, 
                language=lang_str
            )

            # 6.1 Generate answer
            print("\nGenerating Answer...")
            answer = generate_answer(llm, formatted_prompt)
            print("="*80)
            print(f"Assistant: \n{answer}")
            print("="*80)

            # 7. Use centralized history struct
            history_manager.add_message("user", query)
            history_manager.add_message("AI", answer)
            
        except KeyboardInterrupt:
            # Handle Ctrl+C safely
            break

    # Once loop is done, print whole history
    history_manager.print_history()

if __name__ == "__main__":
    main()
