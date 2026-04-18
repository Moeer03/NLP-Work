## Quick Start Guide

### Installation (One Time Only)

```bash
# Navigate to project directory
cd "d:\Data Science\Semester VI\BS DS Morning Sem VI\Data Science Semester VI\NLP\Assignments\3"

# Install dependencies
pip install -r requirements.txt
```

---

## Running the Search Engine

### Option 1: Interactive CLI (Recommended)

```bash
python src/main.py
```

Then try these commands:

```
Search > machine learning
Search > neural AND networks
Search > data OR science
Search > deep NOT learning
Search > stats
Search > rebuild
Search > help
Search > quit
```

### Option 2: Run Tests

```bash
python test_search_engine.py
```

This will:
- Load all 20 documents
- Build the search index
- Test multiple search queries
- Display statistics
- Verify everything is working

### Option 3: View Examples

```bash
python src/examples.py
```

Demonstrates:
- Basic TF-IDF search
- Boolean queries
- Vector space search
- Index statistics
- Analytics and evaluation

---

## Usage Examples

### Example 1: Simple Search

```python
from src.document_processor import DocumentProcessor
from src.search_index import SearchIndex
from src.search_engine import SearchEngine

# Load documents
doc_processor = DocumentProcessor('data')
documents = doc_processor.load_documents()

# Build index
search_index = SearchIndex('index')
search_index.build_index(documents)

# Search
search_engine = SearchEngine(search_index)
results = search_engine.search('machine learning', top_k=5)

# Display results
for doc_id, score, filename in results:
    print(f"{filename}: {score:.4f}")
```

### Example 2: Boolean Search

```python
# AND query - must contain both terms
results = search_engine.boolean_search('deep AND learning')

# OR query - contains either term
results = search_engine.boolean_search('python OR java')

# NOT query - contains first but not second term
results = search_engine.boolean_search('search NOT data')
```

### Example 3: Vector Space Search

```python
# Use cosine similarity instead of TF-IDF
results = search_engine.search('neural networks', 
                               top_k=10, 
                               search_type='vector')
```

### Example 4: View Statistics

```python
stats = search_index.get_index_stats()
print(f"Documents: {stats['total_documents']}")
print(f"Unique Terms: {stats['unique_terms']}")
print(f"Avg Length: {stats['avg_doc_length']:.2f}")
```

---

## Expected Output

### Test Run Output

```
Step 1: Loading documents...
Loading: doc_01.txt
Loading: doc_02.txt
...
✓ Loaded 20 documents

Step 2: Building search index...
✓ Index built: 20 documents, 2547 unique terms

Step 3: Saving index...
✓ Index saved to index/inverted_index.json

Step 4: Index Statistics
  Total Documents: 20
  Unique Terms: 2547
  Average Doc Length: 124.35

Step 5: Testing Search Queries
[Query 1] 'machine learning'
  1. doc_01.txt (Score: 5.2341)
  2. doc_03.txt (Score: 3.1245)
  3. doc_05.txt (Score: 2.8932)
```

### Interactive Search Example

```
================================================================================
NLP Desktop Search Engine
================================================================================

Search > machine learning

================================================================================
Search Results for: 'machine learning'
Found 3 results
================================================================================

1. [01] doc_01.txt
   Score: 5.2341
   Length: 125 terms

2. [03] doc_03.txt
   Score: 3.1245
   Length: 142 terms

3. [05] doc_05.txt
   Score: 2.8932
   Length: 118 terms

Search > quit
Goodbye!
```

---

## Troubleshooting

### Issue: "Module not found" error

**Solution**: Make sure you're in the correct directory and have installed dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "No documents found"

**Solution**: Verify the data folder exists and contains documents:
```bash
dir data
```

### Issue: "Index not found"

**Solution**: Rebuild the index by running:
```bash
python src/main.py
# Then type: rebuild
```

### Issue: NLTK errors

**Solution**: NLTK will automatically download required data on first run. If issues persist:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

---

## File Organization

After first run, the index directory will be created:

```
index/
  ├── inverted_index.json      (35-50 KB)
  └── metadata.json             (5-10 KB)
```

The index is reloaded on subsequent runs for fast initialization.

---

## Project Files Overview

| File | Purpose |
|------|---------|
| `document_processor.py` | Load documents from TXT/DOCX/PDF |
| `text_preprocessor.py` | Clean, tokenize, and normalize text |
| `search_index.py` | Build inverted index with TF-IDF |
| `search_engine.py` | Perform searches with multiple algorithms |
| `config.py` | Configuration management |
| `analytics.py` | Search analytics and evaluation |
| `main.py` | Interactive CLI interface |
| `examples.py` | Code examples and demonstrations |
| `test_search_engine.py` | Automated testing |

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Run test suite to verify installation
3. ✅ Run main.py for interactive searching
4. ✅ Explore examples.py for code patterns
5. ✅ Experiment with different queries
6. ✅ Review source code for implementation details

---

## Support

For detailed information on each module, see:
- `README.md` - Full documentation
- `COMPLETION.md` - Assignment completion details
- `src/examples.py` - Code examples
- Individual source files have comprehensive docstrings

Happy searching! 🔍
