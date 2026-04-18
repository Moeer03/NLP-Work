"""
Search Engine Module
Perform full-text search with ranking
"""

import math
from typing import Dict, List, Tuple, Set
from text_preprocessor import TextPreprocessor
from search_index import SearchIndex


class SearchEngine:
    """Main search engine for querying indexed documents"""
    
    def __init__(self, search_index: SearchIndex):
        """
        Initialize search engine
        
        Args:
            search_index: SearchIndex instance with built index
        """
        self.index = search_index
        self.preprocessor = TextPreprocessor(use_stemming=True)
    
    def search(self, query: str, top_k: int = 10, search_type: str = 'tfidf') -> List[Tuple[int, float, str]]:
        """
        Search documents by query
        
        Args:
            query: Search query string
            top_k: Number of top results to return
            search_type: Type of search - 'tfidf', 'boolean', or 'vector'
            
        Returns:
            List of (doc_id, score, filename) tuples sorted by relevance
        """
        if not query.strip():
            return []
        
        if search_type == 'boolean':
            return self.boolean_search(query, top_k)
        elif search_type == 'vector':
            return self.vector_search(query, top_k)
        else:  # default to tfidf
            return self.tfidf_search(query, top_k)
    
    def tfidf_search(self, query: str, top_k: int = 10) -> List[Tuple[int, float, str]]:
        """
        TF-IDF based search
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of (doc_id, score, filename)
        """
        # Preprocess query
        query_terms = self.preprocessor.preprocess(query)
        
        if not query_terms:
            return []
        
        # Calculate scores for each document
        scores = {}
        
        for doc_id in self.index.doc_info.keys():
            score = 0.0
            
            for term in query_terms:
                # TF-IDF score for this term in this document
                tfidf = self.index.get_tfidf(term, doc_id)
                score += tfidf
            
            if score > 0:
                scores[doc_id] = score
        
        # Sort by score and get top results
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        results = []
        for doc_id, score in ranked:
            filename = self.index.doc_info[doc_id]['filename']
            results.append((doc_id, score, filename))
        
        return results
    
    def boolean_search(self, query: str, top_k: int = 10) -> List[Tuple[int, float, str]]:
        """
        Boolean search supporting AND, OR, NOT operators
        
        Args:
            query: Boolean query (e.g., "machine AND learning")
            top_k: Number of results to return
            
        Returns:
            List of (doc_id, score, filename)
        """
        # Simple boolean parser
        query_upper = query.upper()
        
        if ' AND ' in query_upper:
            return self._boolean_and(query, top_k)
        elif ' OR ' in query_upper:
            return self._boolean_or(query, top_k)
        elif ' NOT ' in query_upper:
            return self._boolean_not(query, top_k)
        else:
            # Single term search
            return self.tfidf_search(query, top_k)
    
    def _boolean_and(self, query: str, top_k: int) -> List[Tuple[int, float, str]]:
        """AND operation - documents must contain ALL terms"""
        parts = query.split(' AND ')
        all_docs = None
        
        for part in parts:
            docs = self.index.find_documents_with_term(part.strip())
            if all_docs is None:
                all_docs = docs
            else:
                all_docs &= docs  # Intersection
        
        results = []
        if all_docs:
            for doc_id in sorted(all_docs)[:top_k]:
                filename = self.index.doc_info[doc_id]['filename']
                results.append((doc_id, 1.0, filename))
        
        return results
    
    def _boolean_or(self, query: str, top_k: int) -> List[Tuple[int, float, str]]:
        """OR operation - documents containing ANY term"""
        parts = query.split(' OR ')
        all_docs = set()
        
        for part in parts:
            docs = self.index.find_documents_with_term(part.strip())
            all_docs |= docs  # Union
        
        results = []
        for doc_id in sorted(all_docs)[:top_k]:
            filename = self.index.doc_info[doc_id]['filename']
            results.append((doc_id, 1.0, filename))
        
        return results
    
    def _boolean_not(self, query: str, top_k: int) -> List[Tuple[int, float, str]]:
        """NOT operation - exclude documents with term"""
        parts = query.split(' NOT ')
        include_docs = self.index.find_documents_with_term(parts[0].strip()) if len(parts) > 0 else set(self.index.doc_info.keys())
        exclude_docs = self.index.find_documents_with_term(parts[1].strip()) if len(parts) > 1 else set()
        
        result_docs = include_docs - exclude_docs
        
        results = []
        for doc_id in sorted(result_docs)[:top_k]:
            filename = self.index.doc_info[doc_id]['filename']
            results.append((doc_id, 1.0, filename))
        
        return results
    
    def vector_search(self, query: str, top_k: int = 10) -> List[Tuple[int, float, str]]:
        """
        Vector space model search using cosine similarity
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of (doc_id, score, filename)
        """
        # Preprocess query
        query_terms = self.preprocessor.preprocess(query)
        
        if not query_terms:
            return []
        
        # Build query vector
        query_vector = {}
        for term in query_terms:
            query_vector[term] = query_vector.get(term, 0) + 1
        
        # Calculate cosine similarity with each document
        scores = {}
        
        for doc_id in self.index.doc_info.keys():
            # Build document vector
            doc_vector = {}
            for term in query_terms:
                tf_idf = self.index.get_tfidf(term, doc_id)
                if tf_idf > 0:
                    doc_vector[term] = tf_idf
            
            # Calculate cosine similarity
            similarity = self._cosine_similarity(query_vector, doc_vector)
            
            if similarity > 0:
                scores[doc_id] = similarity
        
        # Sort by score
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        results = []
        for doc_id, score in ranked:
            filename = self.index.doc_info[doc_id]['filename']
            results.append((doc_id, score, filename))
        
        return results
    
    @staticmethod
    def _cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        """Calculate cosine similarity between two vectors"""
        # Dot product
        dot_product = sum(vec1.get(k, 0) * vec2.get(k, 0) for k in set(vec1.keys()) | set(vec2.keys()))
        
        # Magnitudes
        mag1 = math.sqrt(sum(v**2 for v in vec1.values())) if vec1 else 0
        mag2 = math.sqrt(sum(v**2 for v in vec2.values())) if vec2 else 0
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return dot_product / (mag1 * mag2)
    
    def get_document(self, doc_id: int) -> Tuple[str, str, Dict]:
        """
        Get document content and metadata
        
        Args:
            doc_id: Document ID
            
        Returns:
            (filename, content_preview, metadata)
        """
        if doc_id not in self.index.doc_info:
            return None, None, None
        
        filename = self.index.doc_info[doc_id]['filename']
        info = self.index.doc_info[doc_id]
        
        return filename, info
