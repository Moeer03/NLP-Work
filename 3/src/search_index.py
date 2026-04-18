"""
Search Index Module
Build and manage inverted index with TF-IDF scoring
"""

import json
import math
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict
from text_preprocessor import TextPreprocessor


class SearchIndex:
    """Build and maintain an inverted index for full-text search"""
    
    def __init__(self, index_dir: str = None):
        """
        Initialize search index
        
        Args:
            index_dir: Directory to store index files
        """
        self.index_dir = Path(index_dir) if index_dir else Path('index')
        self.index_dir.mkdir(exist_ok=True)
        
        # Inverted index: term -> {doc_id: frequency}
        self.inverted_index = defaultdict(lambda: defaultdict(int))
        
        # Document info: doc_id -> {filename, length, term_count}
        self.doc_info = {}
        
        # All unique terms
        self.vocabulary = set()
        
        # IDF values: term -> idf
        self.idf = {}
        
        # Preprocessor
        self.preprocessor = TextPreprocessor(use_stemming=True)
        
        self.total_docs = 0
    
    def build_index(self, documents: Dict[int, Tuple[str, str]]):
        """
        Build inverted index from documents
        
        Args:
            documents: Dictionary {doc_id: (filename, content)}
        """
        print("\nBuilding search index...")
        
        for doc_id, (filename, content) in documents.items():
            # Preprocess document
            tokens = self.preprocessor.preprocess(content)
            
            # Get term frequencies in this document
            term_freq = self.preprocessor.get_term_frequency(tokens)
            
            # Update inverted index
            for term, freq in term_freq.items():
                self.inverted_index[term][doc_id] = freq
                self.vocabulary.add(term)
            
            # Store document info
            self.doc_info[doc_id] = {
                'filename': filename,
                'length': len(tokens),
                'term_count': len(term_freq)
            }
            
            self.total_docs += 1
        
        # Calculate IDF values
        self._calculate_idf()
        
        print(f"✓ Index built: {self.total_docs} documents, {len(self.vocabulary)} unique terms")
    
    def _calculate_idf(self):
        """Calculate Inverse Document Frequency for all terms"""
        for term in self.vocabulary:
            # Number of documents containing this term
            doc_frequency = len(self.inverted_index[term])
            
            # IDF = log(N / df) where N = total documents
            self.idf[term] = math.log(self.total_docs / doc_frequency) if doc_frequency > 0 else 0
    
    def get_tf(self, term: str, doc_id: int) -> float:
        """Get Term Frequency"""
        if term in self.inverted_index and doc_id in self.inverted_index[term]:
            # Raw count
            return float(self.inverted_index[term][doc_id])
        return 0.0
    
    def get_tfidf(self, term: str, doc_id: int) -> float:
        """Get TF-IDF score"""
        tf = self.get_tf(term, doc_id)
        idf_val = self.idf.get(term, 0)
        return tf * idf_val
    
    def get_idf(self, term: str) -> float:
        """Get Inverse Document Frequency"""
        return self.idf.get(term, 0)
    
    def find_documents_with_term(self, term: str) -> Set[int]:
        """Get all documents containing a term"""
        preprocessed = self.preprocessor.preprocess(term)
        if not preprocessed:
            return set()
        
        term = preprocessed[0]
        return set(self.inverted_index.get(term, {}).keys())
    
    def save_index(self):
        """Save index to disk"""
        index_file = self.index_dir / 'inverted_index.json'
        metadata_file = self.index_dir / 'metadata.json'
        
        # Prepare data for JSON serialization
        index_data = {
            term: {str(doc_id): freq for doc_id, freq in docs.items()}
            for term, docs in self.inverted_index.items()
        }
        
        metadata = {
            'total_docs': self.total_docs,
            'doc_info': {str(doc_id): info for doc_id, info in self.doc_info.items()},
            'idf': self.idf,
            'vocabulary_size': len(self.vocabulary)
        }
        
        with open(index_file, 'w') as f:
            json.dump(index_data, f, indent=2)
        
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✓ Index saved to {index_file}")
    
    def load_index(self):
        """Load index from disk"""
        index_file = self.index_dir / 'inverted_index.json'
        metadata_file = self.index_dir / 'metadata.json'
        
        if not index_file.exists() or not metadata_file.exists():
            print("Index files not found. Please build index first.")
            return False
        
        # Load index
        with open(index_file, 'r') as f:
            index_data = json.load(f)
            self.inverted_index = defaultdict(lambda: defaultdict(int))
            for term, docs in index_data.items():
                for doc_id_str, freq in docs.items():
                    self.inverted_index[term][int(doc_id_str)] = freq
                    self.vocabulary.add(term)
        
        # Load metadata
        with open(metadata_file, 'r') as f:
            metadata = json.load(f)
            self.total_docs = metadata['total_docs']
            self.doc_info = {int(doc_id): info for doc_id, info in metadata['doc_info'].items()}
            self.idf = metadata['idf']
        
        print(f"✓ Index loaded: {self.total_docs} documents, {len(self.vocabulary)} unique terms")
        return True
    
    def get_index_stats(self) -> Dict:
        """Get index statistics"""
        return {
            'total_documents': self.total_docs,
            'unique_terms': len(self.vocabulary),
            'avg_doc_length': sum(info['length'] for info in self.doc_info.values()) / self.total_docs if self.total_docs > 0 else 0,
            'index_size': len(self.inverted_index)
        }
