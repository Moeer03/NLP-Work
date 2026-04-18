"""
Search Engine Analytics & Reporting
Results analysis and visualization utilities
"""

import json
from typing import List, Dict, Tuple
from pathlib import Path


class SearchAnalytics:
    """Analyze and report on search engine performance"""
    
    def __init__(self):
        """Initialize analytics"""
        self.search_history = []
        self.query_counts = {}
        self.result_clicks = {}
    
    def log_search(self, query: str, results: List[Tuple[int, float, str]], search_type: str = 'tfidf'):
        """Log a search query and its results"""
        entry = {
            'query': query,
            'search_type': search_type,
            'num_results': len(results),
            'top_result': results[0] if results else None,
            'results': results
        }
        self.search_history.append(entry)
        
        # Update query counts
        self.query_counts[query] = self.query_counts.get(query, 0) + 1
    
    def log_click(self, query: str, doc_id: int):
        """Log when user clicks on a search result"""
        key = f"{query}:{doc_id}"
        self.result_clicks[key] = self.result_clicks.get(key, 0) + 1
    
    def get_top_queries(self, top_k: int = 10) -> List[Tuple[str, int]]:
        """Get most frequently searched queries"""
        sorted_queries = sorted(self.query_counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_queries[:top_k]
    
    def get_top_clicked_results(self, top_k: int = 10) -> List[Tuple[str, str, int]]:
        """Get most clicked search results"""
        sorted_clicks = sorted(self.result_clicks.items(), key=lambda x: x[1], reverse=True)
        results = []
        for key, count in sorted_clicks[:top_k]:
            query, doc_id = key.split(':')
            results.append((query, doc_id, count))
        return results
    
    def generate_report(self) -> str:
        """Generate analytics report"""
        report = []
        report.append("="*60)
        report.append("SEARCH ENGINE ANALYTICS REPORT")
        report.append("="*60)
        
        report.append(f"\nTotal Searches: {len(self.search_history)}")
        report.append(f"Unique Queries: {len(self.query_counts)}")
        report.append(f"Total Clicks: {sum(self.result_clicks.values())}")
        
        report.append("\n" + "-"*60)
        report.append("TOP 10 SEARCHED QUERIES")
        report.append("-"*60)
        
        for query, count in self.get_top_queries(10):
            report.append(f"  '{query}': {count} searches")
        
        report.append("\n" + "-"*60)
        report.append("TOP 10 CLICKED RESULTS")
        report.append("-"*60)
        
        for query, doc_id, count in self.get_top_clicked_results(10):
            report.append(f"  Query '{query}' -> Doc {doc_id}: {count} clicks")
        
        report.append("\n" + "="*60)
        
        return "\n".join(report)
    
    def save_history(self, filepath: str):
        """Save search history to JSON file"""
        # Convert to serializable format
        serializable_history = []
        for entry in self.search_history:
            entry_copy = entry.copy()
            if entry_copy['top_result']:
                entry_copy['top_result'] = {
                    'doc_id': entry_copy['top_result'][0],
                    'score': entry_copy['top_result'][1],
                    'filename': entry_copy['top_result'][2]
                }
            serializable_history.append(entry_copy)
        
        with open(filepath, 'w') as f:
            json.dump({
                'search_history': serializable_history,
                'query_counts': self.query_counts,
                'result_clicks': self.result_clicks
            }, f, indent=2)
    
    def load_history(self, filepath: str) -> bool:
        """Load search history from JSON file"""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            self.query_counts = data.get('query_counts', {})
            self.result_clicks = data.get('result_clicks', {})
            return True
        except Exception as e:
            print(f"Error loading history: {e}")
            return False


class ResultRanker:
    """Utilities for ranking and comparing search results"""
    
    @staticmethod
    def rank_by_score(results: List[Tuple[int, float, str]]) -> List[Tuple[int, float, str]]:
        """Rank results by relevance score"""
        return sorted(results, key=lambda x: x[1], reverse=True)
    
    @staticmethod
    def filter_by_threshold(results: List[Tuple[int, float, str]], 
                           threshold: float) -> List[Tuple[int, float, str]]:
        """Filter results by minimum score threshold"""
        return [r for r in results if r[1] >= threshold]
    
    @staticmethod
    def merge_results(results1: List[Tuple[int, float, str]], 
                     results2: List[Tuple[int, float, str]], 
                     weights: Tuple[float, float] = (0.7, 0.3)) -> List[Tuple[int, float, str]]:
        """Merge and weight results from multiple searches"""
        combined = {}
        
        for doc_id, score, filename in results1:
            combined[doc_id] = (weights[0] * score, filename)
        
        for doc_id, score, filename in results2:
            if doc_id in combined:
                combined[doc_id] = (combined[doc_id][0] + weights[1] * score, filename)
            else:
                combined[doc_id] = (weights[1] * score, filename)
        
        merged_results = [(doc_id, score, filename) 
                         for doc_id, (score, filename) in combined.items()]
        
        return ResultRanker.rank_by_score(merged_results)
    
    @staticmethod
    def calculate_mrr(results: List[Tuple[int, float, str]], 
                     relevant_docs: set) -> float:
        """Calculate Mean Reciprocal Rank (MRR) for evaluation"""
        for rank, (doc_id, _, _) in enumerate(results, 1):
            if doc_id in relevant_docs:
                return 1.0 / rank
        return 0.0
    
    @staticmethod
    def calculate_precision_at_k(results: List[Tuple[int, float, str]], 
                                relevant_docs: set, k: int = 10) -> float:
        """Calculate Precision@K"""
        if not results:
            return 0.0
        
        relevant_in_top_k = sum(1 for doc_id, _, _ in results[:k] if doc_id in relevant_docs)
        return relevant_in_top_k / min(k, len(results))
    
    @staticmethod
    def calculate_recall_at_k(results: List[Tuple[int, float, str]], 
                             relevant_docs: set, k: int = 10) -> float:
        """Calculate Recall@K"""
        if not relevant_docs:
            return 0.0
        
        relevant_in_top_k = sum(1 for doc_id, _, _ in results[:k] if doc_id in relevant_docs)
        return relevant_in_top_k / len(relevant_docs)
