#!/usr/bin/env python3
"""
Build FAISS Vector Database

This script builds a FAISS vector database from the Ibit_data.json file.
The database can be used for semantic search and intent matching.
"""

import argparse
import logging
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.utils.vector_db import build_index_from_intents, FAISSVectorDB

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main function to build vector database"""
    parser = argparse.ArgumentParser(
        description='Build FAISS vector database from intents JSON'
    )
    parser.add_argument(
        '--input',
        type=str,
        default='data/Ibit_data.json',
        help='Path to input JSON file (default: data/Ibit_data.json)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='data/vector_db',
        help='Output directory for vector database (default: data/vector_db)'
    )
    parser.add_argument(
        '--model',
        type=str,
        default='all-MiniLM-L6-v2',
        help='Sentence transformer model (default: all-MiniLM-L6-v2)'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=32,
        help='Batch size for encoding (default: 32)'
    )
    parser.add_argument(
        '--test-query',
        type=str,
        help='Optional test query to run after building'
    )
    
    args = parser.parse_args()
    
    try:
        logger.info("=" * 60)
        logger.info("Building FAISS Vector Database")
        logger.info("=" * 60)
        logger.info(f"Input file: {args.input}")
        logger.info(f"Output directory: {args.output}")
        logger.info(f"Model: {args.model}")
        logger.info(f"Batch size: {args.batch_size}")
        logger.info("=" * 60)
        
        # Build index
        vector_db = build_index_from_intents(
            json_path=args.input,
            output_dir=args.output,
            model_name=args.model,
            batch_size=args.batch_size
        )
        
        # Print statistics
        stats = vector_db.get_stats()
        logger.info("=" * 60)
        logger.info("Vector Database Statistics:")
        logger.info(f"  Total vectors: {stats['total_vectors']}")
        logger.info(f"  Dimension: {stats['dimension']}")
        logger.info(f"  Model: {stats['model_name']}")
        logger.info(f"  Metadata entries: {stats['metadata_count']}")
        logger.info("=" * 60)
        
        # Test query if provided
        if args.test_query:
            logger.info(f"\nTesting query: '{args.test_query}'")
            results = vector_db.search(args.test_query, k=5)
            logger.info(f"\nTop {len(results)} results:")
            for result in results:
                logger.info(f"\n  Rank {result['rank']}:")
                logger.info(f"    Tag: {result['metadata']['tag']}")
                logger.info(f"    Pattern: {result['metadata']['pattern']}")
                logger.info(f"    Score: {result['score']:.4f}")
                logger.info(f"    Distance: {result['distance']:.4f}")
                if result['metadata'].get('responses'):
                    logger.info(f"    Response: {result['metadata']['responses'][0][:100]}...")
        
        logger.info("\n✓ Vector database built successfully!")
        logger.info(f"  Index saved to: {args.output}/faiss.index")
        logger.info(f"  Metadata saved to: {args.output}/metadata.pkl")
        logger.info(f"  Config saved to: {args.output}/config.json")
        
    except FileNotFoundError as e:
        logger.error(f"Error: File not found - {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error building vector database: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()

