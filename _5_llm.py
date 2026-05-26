import logging
import warnings
import os

# Suppress annoying warnings
warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import transformers
transformers.logging.set_verbosity_error()

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from huggingface_hub import login

from config import HF_TOKEN, LLM_MODEL_NAME

logger = logging.getLogger(__name__)


def setup_llm():
    """
    Initializes the Hugging Face text generation pipeline securely.
    Ensures safe loading via huggingface_hub login.
    """
    if HF_TOKEN:
        try:
            # Login to HF Hub to ensure no 401s on gated models
            login(token=HF_TOKEN, write_permission=False)
            logger.info("Successfully authenticated with Hugging Face Hub.")
        except Exception as e:
            logger.warning(f"Failed HF login: {e}. If the model is public, you might be fine.")
    else:
        logger.warning("No HF_TOKEN found in .env, continuing anonymously.")

    logger.info(f"Loading tokenizer and model: {LLM_MODEL_NAME}...")

    # Load Tokenizer
    tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL_NAME, token=HF_TOKEN)

    # Load Model (on CPU)
    model = AutoModelForCausalLM.from_pretrained(LLM_MODEL_NAME, token=HF_TOKEN)
    model = model.to("cpu")

    logger.info("Setting up text generation pipeline...")
    
    # HuggingFacePipeline wrapper
    llm_pipeline = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=500,
        temperature=0.3, 
        do_sample=True,       # Allows randomness
        pad_token_id=tokenizer.eos_token_id,  # explicitly specify to avoid warnings
        truncation=True,       #  Cuts long input if needed
        return_full_text=False  # generated answer  not whole original prompt


    )

    return llm_pipeline


def generate_answer(llm_pipeline, prompt: str) -> str:
    """
    Takes a raw string prompt and returns the generated text snippet from the pipeline.
    """
    logger.debug("Generating answer via HF Pipeline...")
    
    # We slice out the raw prompt itself to return only the newly generated text
    response = llm_pipeline(prompt, temperature=0.2)
    return response[0]['generated_text'].strip()
