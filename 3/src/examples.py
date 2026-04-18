"""
Examples & Demonstrations
Sample usage patterns for the Search Engine
"""

import os
import sys
from pathlib import Path

def example_basic_search():
    """Example 1: Basic TF-IDF Search"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic TF-IDF Search")
    print("="*60)
    
    # Add src to path
    sys.path.insert(0, str(Path(__file__).parent))
    
    from document_processor import DocumentProcessor
    from search_index import SearchIndex
    from search_engine import SearchEngine
    
    # Initialize
    workspace = Path(__file__).parent.parent
    doc_processor = DocumentProcessor(str(workspace / 'data'))
    documents = doc_processor.load_documents()
    
    search_index = SearchIndex(str(workspace / 'index'))
    search_index.build_index(documents)
    
    search_engine = SearchEngine(search_index)
    
    # Search
    query = "machine learning"
    results = search_engine.search(query, top_k=5)
    
    print(f"\nQuery: '{query}'")
    print(f"Results:\n")
    for rank, (doc_id, score, filename) in enumerate(results, 1):
        print(f"  {rank}. {filename}")
        print(f"     Score: {score:.4f}")
    
    return results


def example_boolean_search():
    """Example 2: Boolean Queries"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Boolean Search Queries")
    print("="*60)
    
    sys.path.insert(0, str(Path(__file__).parent))
    
    from document_processor import DocumentProcessor
    from search_index import SearchIndex
    from search_engine import SearchEngine
    
    workspace = Path(__file__).parent.parent
    doc_processor = DocumentProcessor(str(workspace / 'data'))
    documents = doc_processor.load_documents()
    
    search_index = SearchIndex(str(workspace / 'index'))
    search_index.build_index(documents)
    
    search_engine = SearchEngine(search_index)
    
    # Boolean AND
    print("\nAND Query: 'neural AND networks'")
    results = search_engine.boolean_search('neural AND networks', top_k=5)
    for rank, (doc_id, _, filename) in enumerate(results, 1):
        print(f"  {rank}. {filename}")
    
    # Boolean OR
    print("\nOR Query: 'python OR java'")
    results = search_engine.boolean_search('python OR java', top_k=5)
    for rank, (doc_id, _, filename) in enumerate(results, 1):
        print(f"  {rank}. {filename}")
    
    # Boolean NOT
    print("\nNOT Query: 'learning NOT machine'")
    results = search_engine.boolean_search('learning NOT machine', top_k=5)
    for rank, (doc_id, _, filename) in enumerate(results, 1):
        print(f"  {rank}. {filename}")


def example_vector_search():
    """Example 3: Vector Space Model (Cosine Similarity)"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Vector Space Search")
    print("="*60)
    
    sys.path.insert(0, str(Path(__file__).parent))
    
    from document_processor import DocumentProcessor
    from search_index import SearchIndex
    from search_engine import SearchEngine
    
    workspace = Path(__file__).parent.parent
    doc_processor = DocumentProcessor(str(workspace / 'data'))
    documents = doc_processor.load_documents()
    
    search_index = SearchIndex(str(workspace / 'index'))
    search_index.build_index(documents)
    
    search_engine = SearchEngine(search_index)
    
    query = "deep neural networks"
    print(f"\nQuery: '{query}'")
    
    results = search_engine.search(query, top_k=5, search_type='vector')
    print(f"\nVector Space Results (Cosine Similarity):")
    for rank, (doc_id, score, filename) in enumerate(results, 1):
        print(f"  {rank}. {filename}")
        print(f"     Similarity: {score:.4f}")


def example_index_statistics():
    """Example 4: Index Statistics & Metadata"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Index Statistics")
    print("="*60)
    
    sys.path.insert(0, str(Path(__file__).parent))
    
    from document_processor import DocumentProcessor
    from search_index import SearchIndex
    
    workspace = Path(__file__).parent.parent
    doc_processor = DocumentProcessor(str(workspace / 'data'))
    documents = doc_processor.load_documents()
    
    search_index = SearchIndex(str(workspace / 'index'))
    search_index.build_index(documents)
    
    stats = search_index.get_index_stats()
    
    print("\nIndex Information:")
    print(f"  Total Documents: {stats['total_documents']}")
    print(f"  Unique Terms: {stats['unique_terms']}")
    print(f"  Average Document Length: {stats['avg_doc_length']:.2f} tokens")
    print(f"  Index Entries: {stats['index_size']}")
    
    print("\nDocument Information:")
    for doc_id, info in search_index.doc_info.items():
        print(f"  Doc {doc_id:02d}: {info['filename']}")
        print(f"           Length: {info['length']} terms")


def example_analytics():
    """Example 5: Search Analytics & Evaluation"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Search Analytics")
    print("="*60)
    
    sys.path.insert(0, str(Path(__file__).parent))
    
    from analytics import SearchAnalytics, ResultRanker
    from document_processor import DocumentProcessor
    from search_index import SearchIndex
    from search_engine import SearchEngine
    
    workspace = Path(__file__).parent.parent
    
    # Setup
    doc_processor = DocumentProcessor(str(workspace / 'data'))
    documents = doc_processor.load_documents()
    
    search_index = SearchIndex(str(workspace / 'index'))
    search_index.build_index(documents)
    
    search_engine = SearchEngine(search_index)
    analytics = SearchAnalytics()
    
    # Perform searches and log them
    queries = ["machine learning", "deep learning", "data science", "neural networks"]
    
    for query in queries:
        results = search_engine.search(query, top_k=5)
        analytics.log_search(query, results)
    
    # Log some clicks (simulated user behavior)
    analytics.log_click("machine learning", 1)
    analytics.log_click("machine learning", 3)
    analytics.log_click("deep learning", 3)
    
    # Generate report
    print(analytics.generate_report())
    
    # Precision and Recall
    print("\nEvaluation Metrics:")
    relevant_docs = {1, 3}  # Relevant documents for "machine learning"
    results = search_engine.search("machine learning", top_k=10)
    
    prec = ResultRanker.calculate_precision_at_k(results, relevant_docs, k=5)
    recall = ResultRanker.calculate_recall_at_k(results, relevant_docs, k=5)
    mrr = ResultRanker.calculate_mrr(results, relevant_docs)
    
    print(f"  Precision@5: {prec:.3f}")
    print(f"  Recall@5: {recall:.3f}")
    print(f"  MRR: {mrr:.3f}")


if __name__ == '__main__':
    print("\n" + "="*60)
    print("SEARCH ENGINE EXAMPLES & DEMONSTRATIONS")
    print("="*60)
    
    try:
        # Run examples
        example_basic_search()
        example_boolean_search()
        example_vector_search()
        example_index_statistics()
        example_analytics()
        
        print("\n" + "="*60)
        print("✓ All examples completed successfully!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error running examples: {e}")
        import traceback
        traceback.print_exc()
