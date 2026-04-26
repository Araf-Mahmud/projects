import os
from langfuse import get_client, propagate_attributes, Langfuse
from dotenv import load_dotenv

load_dotenv()

_langfuse_client = None
_langfuse_initialized = False
_crewai_instrumented = False

def _ensure_langfuse_initialised():
    
    global _langfuse_client, _langfuse_initialized
    
    if _langfuse_initialized:
        return _langfuse_client

    _langfuse_client = Langfuse(
        public_key = os.getenv('LANGFUSE_PUBLIC_KEY'),
        secret_key = os.getenv('LANGFUSE_SECRET_KEY'),
        host = os.getenv('LANGFUSE_BASE_URL')
    )
        
    _langfuse_initialized = True
    
    return _langfuse_client

def _ensure_crewai_instrumented():
    global _crewai_instrumented
    
    if _crewai_instrumented:
        return
    
    from openinference.instrumentation.crewai import CrewAIInstrumentor
    
    CrewAIInstrumentor().instrument(skip_dep_check = True)
    
    _crewai_instrumented = True
    
    
def get_langfuse_client():
    
    return _ensure_langfuse_initialised()

def get_propagate_attribute():

    return propagate_attributes

class LangfuseMonitoringService:
    
    def __init__(self):
        self.langfuse = get_langfuse_client()
    
    def start_observation(self, name : str, as_type : str, **kwargs):
        if self.langfuse is None:
            return None
        observation = self.client.start_observation(name = name, as_type = as_type)
        return observation
    
    def flush(self):
        if self.langfuse is None:
            return None
        try:
            self.langfuse.flush()
        except Exception as e:
            print(f"Error flushing Langfuse: {e}")


