"""
Search Engine Configuration
Configurable parameters for the search engine
"""

import json
from pathlib import Path

class Config:
    """Search engine configuration"""
    
    # Text processing parameters
    CLEAN_TEXT = True
    USE_STEMMING = True
    USE_LEMMATIZATION = False
    REMOVE_STOPWORDS = True
    MIN_TOKEN_LENGTH = 2
    
    # Search parameters
    DEFAULT_TOP_K = 10
    DEFAULT_SEARCH_TYPE = 'tfidf'  # 'tfidf', 'vector', 'boolean'
    
    # Index parameters
    SAVE_INDEX = True
    LOAD_EXISTING_INDEX = True
    
    # Document processing
    SUPPORTED_FORMATS = ['.txt', '.docx', '.pdf']
    
    # Output parameters
    DISPLAY_SCORES = True
    DISPLAY_METADATA = True
    
    @staticmethod
    def to_dict():
        """Convert config to dictionary"""
        return {
            'text_processing': {
                'clean_text': Config.CLEAN_TEXT,
                'use_stemming': Config.USE_STEMMING,
                'use_lemmatization': Config.USE_LEMMATIZATION,
                'remove_stopwords': Config.REMOVE_STOPWORDS,
                'min_token_length': Config.MIN_TOKEN_LENGTH,
            },
            'search': {
                'default_top_k': Config.DEFAULT_TOP_K,
                'default_search_type': Config.DEFAULT_SEARCH_TYPE,
            },
            'index': {
                'save_index': Config.SAVE_INDEX,
                'load_existing': Config.LOAD_EXISTING_INDEX,
            },
            'document_processing': {
                'supported_formats': Config.SUPPORTED_FORMATS,
            },
            'output': {
                'display_scores': Config.DISPLAY_SCORES,
                'display_metadata': Config.DISPLAY_METADATA,
            }
        }
    
    @staticmethod
    def save_to_file(filepath):
        """Save configuration to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(Config.to_dict(), f, indent=2)
    
    @staticmethod
    def load_from_file(filepath):
        """Load configuration from JSON file"""
        if not Path(filepath).exists():
            return False
        
        with open(filepath, 'r') as f:
            config_dict = json.load(f)
        
        # Update config values from file
        if 'text_processing' in config_dict:
            tp = config_dict['text_processing']
            Config.CLEAN_TEXT = tp.get('clean_text', Config.CLEAN_TEXT)
            Config.USE_STEMMING = tp.get('use_stemming', Config.USE_STEMMING)
            Config.USE_LEMMATIZATION = tp.get('use_lemmatization', Config.USE_LEMMATIZATION)
            Config.REMOVE_STOPWORDS = tp.get('remove_stopwords', Config.REMOVE_STOPWORDS)
            Config.MIN_TOKEN_LENGTH = tp.get('min_token_length', Config.MIN_TOKEN_LENGTH)
        
        if 'search' in config_dict:
            s = config_dict['search']
            Config.DEFAULT_TOP_K = s.get('default_top_k', Config.DEFAULT_TOP_K)
            Config.DEFAULT_SEARCH_TYPE = s.get('default_search_type', Config.DEFAULT_SEARCH_TYPE)
        
        if 'index' in config_dict:
            i = config_dict['index']
            Config.SAVE_INDEX = i.get('save_index', Config.SAVE_INDEX)
            Config.LOAD_EXISTING_INDEX = i.get('load_existing', Config.LOAD_EXISTING_INDEX)
        
        return True


# Default configuration file
CONFIG_FILE = Path(__file__).parent / 'config.json'

# Initialize config file if it doesn't exist
if not CONFIG_FILE.exists():
    Config.save_to_file(str(CONFIG_FILE))
