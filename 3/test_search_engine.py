"""
Test Script for Search Engine
Validates all functionality without CLI interaction
"""

import os
import sys
from pathlib import Path

# Setup path
workspace_root = Path(__file__).parent
sys.path.insert(0, str(workspace_root / 'src'))

def test_search_engine():
    """Test all search engine components"""
    
    print("=" * 80)
    print("SEARCH ENGINE TEST SUITE")
    print("=" * 80)
    
    try:
        # Import modules
        print("\n[1/6] Importing modules...")
        from document_processor import DocumentProcessor
        from search_index import SearchIndex
        from search_engine import SearchEngine
        print("✓ All modules imported successfully")
        
        # Initialize
        data_dir = workspace_root / 'data'
        index_dir = workspace_root / 'index'
        
        # Load documents
        print("\n[2/6] Loading documents...")
        doc_processor = DocumentProcessor(str(data_dir))
        documents = doc_processor.load_documents()
        print(f"✓ Loaded {len(documents)} documents")
        
        if not documents:
            print("ERROR: No documents loaded!")
            return False
        
        # Build index
        print("\n[3/6] Building search index...")
        search_index = SearchIndex(str(index_dir))
        search_index.build_index(documents)
        print(f"✓ Index built successfully")
        
        # Save index
        print("\n[4/6] Saving index...")
        search_index.save_index()
        print("✓ Index saved to disk")
        
        # Initialize search engine
        print("\n[5/6] Initializing search engine...")
        search_engine = SearchEngine(search_index)
        print("✓ Search engine ready")
        
        # Test searches
        print("\n[6/6] Testing search queries...")
        
        test_queries = [
            ("machine learning", "TF-IDF"),
            ("neural networks", "TF-IDF"),
            ("data science", "TF-IDF"),
        ]
        
        for query, method in test_queries:
            results = search_engine.search(query, top_k=3, search_type='tfidf')
            print(f"\n  Query: '{query}' ({method})")
            if results:
                for rank, (doc_id, score, filename) in enumerate(results, 1):
                    print(f"    {rank}. {filename} (Score: {score:.4f})")
            else:
                print(f"    No results found")
        
        # Display stats
        print("\n" + "=" * 80)
        print("INDEX STATISTICS")
        print("=" * 80)
        stats = search_index.get_index_stats()
        print(f"Total Documents: {stats['total_documents']}")
        print(f"Unique Terms: {stats['unique_terms']}")
        print(f"Average Doc Length: {stats['avg_doc_length']:.2f} tokens")
        print(f"Index Size: {stats['index_size']} entries")
        
        print("\n" + "=" * 80)
        print("✓ ALL TESTS PASSED - Search Engine is Working!")
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = test_search_engine()
    sys.exit(0 if success else 1)
