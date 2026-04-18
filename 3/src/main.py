"""
NLP Desktop Search Engine
Main application for building and searching indexed documents
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Tuple
from tqdm import tqdm

from document_processor import DocumentProcessor
from search_index import SearchIndex
from search_engine import SearchEngine


class SearchEngineApp:
    """Main application class for desktop search engine"""
    
    def __init__(self, data_dir: str, index_dir: str):
        """
        Initialize the search engine application
        
        Args:
            data_dir: Directory containing documents
            index_dir: Directory to store index
        """
        self.data_dir = data_dir
        self.index_dir = index_dir
        
        self.doc_processor = DocumentProcessor(data_dir)
        self.search_index = SearchIndex(index_dir)
        self.search_engine = None
    
    def build_index(self, rebuild: bool = False) -> bool:
        """
        Build search index from documents
        
        Args:
            rebuild: Force rebuild even if index exists
            
        Returns:
            True if successful
        """
        # Try to load existing index unless rebuild is requested
        if not rebuild and self.search_index.load_index():
            self.search_engine = SearchEngine(self.search_index)
            return True
        
        # Load documents
        print(f"Loading documents from {self.data_dir}...")
        documents = self.doc_processor.load_documents()
        
        if not documents:
            print("No documents found!")
            return False
        
        # Build index
        self.search_index.build_index(documents)
        self.search_engine = SearchEngine(self.search_index)
        
        # Save index
        self.search_index.save_index()
        
        return True
    
    def search(self, query: str, top_k: int = 10, search_type: str = 'tfidf') -> List[Tuple[int, float, str]]:
        """
        Search for documents matching query
        
        Args:
            query: Search query
            top_k: Number of results to return
            search_type: Type of search ('tfidf', 'boolean', 'vector')
            
        Returns:
            List of search results
        """
        if not self.search_engine:
            print("Index not built. Please call build_index() first.")
            return []
        
        results = self.search_engine.search(query, top_k, search_type)
        return results
    
    def display_results(self, results: List[Tuple[int, float, str]], query: str = ""):
        """
        Display search results in formatted way
        
        Args:
            results: Search results
            query: Original query string (for display)
        """
        if not results:
            print(f"\nNo results found for '{query}'")
            return
        
        print(f"\n{'='*80}")
        print(f"Search Results for: '{query}'")
        print(f"Found {len(results)} results")
        print(f"{'='*80}\n")
        
        for rank, (doc_id, score, filename) in enumerate(results, 1):
            print(f"{rank}. [{doc_id:02d}] {filename}")
            print(f"   Score: {score:.4f}")
            # Get additional metadata
            doc_info = self.search_index.doc_info.get(doc_id, {})
            if doc_info:
                print(f"   Length: {doc_info.get('length', 0)} terms")
            print()
    
    def get_stats(self) -> dict:
        """Get search engine statistics"""
        if not self.search_index:
            return {}
        
        stats = self.search_index.get_index_stats()
        stats['search_type'] = 'TF-IDF'
        return stats
    
    def display_stats(self):
        """Display index statistics"""
        stats = self.get_stats()
        
        if not stats:
            print("No index built yet.")
            return
        
        print(f"\n{'='*50}")
        print("Index Statistics")
        print(f"{'='*50}")
        print(f"Total Documents: {stats.get('total_documents', 0)}")
        print(f"Unique Terms: {stats.get('unique_terms', 0)}")
        print(f"Average Document Length: {stats.get('avg_doc_length', 0):.2f} terms")
        print(f"{'='*50}\n")


def main():
    """Main entry point"""
    # Get workspace root
    workspace_root = Path(__file__).parent.parent
    data_dir = workspace_root / 'data'
    index_dir = workspace_root / 'index'
    
    # Initialize app
    app = SearchEngineApp(str(data_dir), str(index_dir))
    
    print("=" * 80)
    print("NLP Desktop Search Engine")
    print("=" * 80)
    
    # Build or load index
    if not app.build_index():
        print("Failed to build index!")
        return
    
    app.display_stats()
    
    # Interactive search loop
    print("Type 'quit' to exit, 'help' for options\n")
    
    while True:
        try:
            query = input("Search > ").strip()
            
            if not query:
                continue
            
            if query.lower() == 'quit':
                print("Goodbye!")
                break
            
            if query.lower() == 'help':
                print("\nSearch Engine Help:")
                print("- Simple query: 'machine learning'")
                print("- AND query: 'deep AND learning'")
                print("- OR query: 'python OR java'")
                print("- NOT query: 'search NOT data'")
                print("- Commands: 'stats' (show statistics), 'rebuild' (rebuild index)")
                print()
                continue
            
            if query.lower() == 'stats':
                app.display_stats()
                continue
            
            if query.lower() == 'rebuild':
                print("Rebuilding index...")
                if app.build_index(rebuild=True):
                    print("Index rebuilt successfully!")
                    app.display_stats()
                continue
            
            # Perform search
            results = app.search(query, top_k=10)
            app.display_results(results, query)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    main()
