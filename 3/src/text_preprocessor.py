"""
Text Preprocessing Module
Text normalization, tokenization, and stemming
"""

import re
import string
from typing import List, Set
from collections import Counter

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import PorterStemmer, WordNetLemmatizer
    
    # Download required data
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet', quiet=True)
    
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    print("NLTK not available. Using basic text processing.")


class TextPreprocessor:
    """Preprocess text for indexing and searching"""
    
    def __init__(self, use_stemming: bool = True, use_lemmatization: bool = False,
                 remove_stopwords: bool = True):
        """
        Initialize preprocessor
        
        Args:
            use_stemming: Whether to apply Porter stemming
            use_lemmatization: Whether to apply lemmatization
            remove_stopwords: Whether to remove English stopwords
        """
        self.use_stemming = use_stemming
        self.use_lemmatization = use_lemmatization
        self.should_remove_stopwords = remove_stopwords
        
        if NLTK_AVAILABLE:
            self.stemmer = PorterStemmer()
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
        else:
            self.stop_words = self._basic_stopwords()
        
        # Add custom stopwords
        self.custom_stopwords = {'would', 'could', 'also', 'etc', 'one', 'two'}
        self.stop_words.update(self.custom_stopwords) if hasattr(self, 'stop_words') else None
    
    @staticmethod
    def _basic_stopwords() -> Set[str]:
        """Return basic set of stopwords if NLTK unavailable"""
        return {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'or', 'that',
            'the', 'to', 'was', 'will', 'with', 'this', 'but', 'have', 'not',
            'been', 'can', 'just', 'more', 'than', 'then', 'which', 'who'
        }
    
    def clean_text(self, text: str) -> str:
        """
        Basic text cleaning
        
        Args:
            text: Raw text string
            
        Returns:
            Cleaned text
        """
        # Convert to lowercase
        text = text.lower()
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Remove email addresses
        text = re.sub(r'\S+@\S+', '', text)
        # Remove special characters and digits (keep only letters and spaces)
        text = re.sub(r'[^a-z\s]', ' ', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of tokens
        """
        try:
            if NLTK_AVAILABLE:
                tokens = word_tokenize(text)
            else:
                tokens = text.split()
        except (LookupError, Exception):
            # Fallback if NLTK data is missing
            tokens = text.split()
        
        return [t for t in tokens if t.isalpha()]
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """Remove stopwords from tokens"""
        if not self.should_remove_stopwords:
            return tokens
        
        return [t for t in tokens if t not in self.stop_words]
    
    def stem(self, tokens: List[str]) -> List[str]:
        """Apply Porter stemming"""
        if not self.use_stemming or not NLTK_AVAILABLE:
            return tokens
        
        return [self.stemmer.stem(t) for t in tokens]
    
    def lemmatize(self, tokens: List[str]) -> List[str]:
        """Apply lemmatization"""
        if not self.use_lemmatization or not NLTK_AVAILABLE:
            return tokens
        
        return [self.lemmatizer.lemmatize(t) for t in tokens]
    
    def preprocess(self, text: str) -> List[str]:
        """
        Full preprocessing pipeline
        
        Args:
            text: Raw text
            
        Returns:
            List of processed tokens
        """
        # Clean
        text = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize(text)
        
        # Remove stopwords
        tokens = self.remove_stopwords(tokens)
        
        # Stemming or Lemmatization
        if self.use_stemming:
            tokens = self.stem(tokens)
        elif self.use_lemmatization:
            tokens = self.lemmatize(tokens)
        
        # Remove duplicates while preserving order, remove empty
        return [t for t in tokens if t and len(t) > 1]
    
    def get_term_frequency(self, tokens: List[str]) -> dict:
        """Get term frequency counts"""
        return dict(Counter(tokens))
