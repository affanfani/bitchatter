#!/usr/bin/env python3
"""
Verification Script for IBIT Chatbot

This script verifies that all components are properly set up and working.
"""

import sys
import os
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("📦 Checking dependencies...")
    required = [
        'flask', 'flask_cors', 'flask_sqlalchemy', 'flasgger',
        'faiss', 'sentence_transformers', 'openai', 'sqlalchemy'
    ]
    
    missing = []
    for pkg in required:
        try:
            __import__(pkg.replace('-', '_').replace('_cpu', ''))
            print(f"  ✓ {pkg}")
        except ImportError:
            print(f"  ✗ {pkg} - MISSING")
            missing.append(pkg)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✓ All dependencies installed")
    return True


def check_vector_database():
    """Check if vector database is built and working"""
    print("\n🗄️  Checking vector database...")
    
    vector_db_dir = Path('data/vector_db')
    required_files = ['faiss.index', 'metadata.pkl', 'config.json']
    
    for file in required_files:
        if not (vector_db_dir / file).exists():
            print(f"  ✗ {file} - NOT FOUND")
            print("\n❌ Vector database not built")
            print("Run: python build_vector_db.py")
            return False
        print(f"  ✓ {file}")
    
    # Test loading and searching
    try:
        from app.utils.vector_db import FAISSVectorDB
        
        vdb = FAISSVectorDB()
        vdb.load(
            str(vector_db_dir / 'faiss.index'),
            str(vector_db_dir / 'metadata.pkl'),
            str(vector_db_dir / 'config.json')
        )
        
        stats = vdb.get_stats()
        print(f"\n  📊 Vector Database Stats:")
        print(f"     - Total vectors: {stats['total_vectors']}")
        print(f"     - Dimension: {stats['dimension']}")
        print(f"     - Model: {stats['model_name']}")
        
        # Test search
        results = vdb.search("What is IBIT?", k=3)
        if results:
            print(f"\n  🔍 Search Test (query: 'What is IBIT?'):")
            for i, result in enumerate(results[:3], 1):
                tag = result['metadata']['tag']
                score = result['score']
                print(f"     {i}. {tag} (score: {score:.3f})")
            print("\n✓ Vector database working perfectly!")
            return True
        else:
            print("\n⚠️  Vector database loaded but search returned no results")
            return False
            
    except Exception as e:
        print(f"\n❌ Error testing vector database: {e}")
        return False


def check_database():
    """Check if SQLite database is initialized"""
    print("\n🗄️  Checking SQLite database...")
    
    db_path = Path('instance/app.db')
    if not db_path.exists():
        print(f"  ✗ Database file not found")
        print("\n❌ Database not initialized")
        print("Run: python -c \"from app.main import create_app; from app.database import db; app = create_app(); app.app_context().push(); db.create_all()\"")
        return False
    
    print(f"  ✓ Database file exists ({db_path.stat().st_size} bytes)")
    
    # Check tables
    try:
        from app.main import create_app
        from app.database import db
        from sqlalchemy import inspect
        
        app = create_app()
        with app.app_context():
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if tables:
                print(f"\n  📊 Tables found:")
                for table in tables:
                    print(f"     - {table}")
                print("\n✓ Database properly initialized")
                return True
            else:
                print("\n⚠️  Database exists but no tables found")
                print("Run setup again to initialize tables")
                return False
                
    except Exception as e:
        print(f"\n❌ Error checking database: {e}")
        return False


def check_config():
    """Check if configuration is set up"""
    print("\n⚙️  Checking configuration...")
    
    env_file = Path('.env')
    if not env_file.exists():
        print("  ✗ .env file not found")
        print("\n⚠️  Configuration not set up")
        print("Copy env.example to .env and add your API key")
        return False
    
    print("  ✓ .env file exists")
    
    # Check for API key
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENROUTER_API_KEY') or os.getenv('OpenAPI')
    
    if not api_key:
        print("  ✗ OPENROUTER_API_KEY not set")
        print("\n⚠️  API key not configured")
        print("Add your OpenRouter API key to .env file")
        return False
    
    if api_key in ['your-api-key-here', 'your-openrouter-api-key-here']:
        print("  ✗ API key is still placeholder")
        print("\n⚠️  Please set a real API key in .env")
        return False
    
    print(f"  ✓ API key configured ({api_key[:10]}...)")
    print("✓ Configuration looks good")
    return True


def check_data_file():
    """Check if data file exists"""
    print("\n📄 Checking data file...")
    
    data_file = Path('data/Ibit_data.json')
    if not data_file.exists():
        print("  ✗ Ibit_data.json not found")
        return False
    
    print(f"  ✓ Data file exists ({data_file.stat().st_size} bytes)")
    
    # Check content
    try:
        import json
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            intents = data.get('intents', [])
            print(f"  ✓ {len(intents)} intents loaded")
            return True
    except Exception as e:
        print(f"  ✗ Error reading data file: {e}")
        return False


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("🔍 IBIT Chatbot - Setup Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Data File", check_data_file),
        ("Vector Database", check_vector_database),
        ("SQLite Database", check_database),
        ("Configuration", check_config),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print(f"\n❌ Unexpected error in {name}: {e}")
            results[name] = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results.items():
        status = "✓" if passed else "✗"
        print(f"  {status} {name}")
        if not passed:
            all_passed = False
    
    print()
    
    if all_passed:
        print("🎉 All checks passed! You're ready to run the chatbot!")
        print("\nTo start the application:")
        print("  python run.py")
        print("\nThen open: http://localhost:5000")
        return 0
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("\nFor help, see:")
        print("  - QUICKSTART.md")
        print("  - README.md")
        return 1


if __name__ == '__main__':
    sys.exit(main())

