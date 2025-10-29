"""
Vector Database Utility

This module provides utilities for creating and managing FAISS vector databases
for semantic search and retrieval.
"""

import json
import pickle
import numpy as np
import faiss
from typing import List, Dict, Any, Tuple, Optional
from sentence_transformers import SentenceTransformer
import logging
import os

logger = logging.getLogger(__name__)


class FAISSVectorDB:
    """FAISS Vector Database for semantic search"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', dimension: int = 384):
        """
        Initialize FAISS Vector Database.
        
        Args:
            model_name: Sentence transformer model name
            dimension: Vector dimension (default: 384 for all-MiniLM-L6-v2)
        """
        self.model_name = model_name
        self.dimension = dimension
        self.encoder = SentenceTransformer(model_name)
        self.index = None
        self.metadata = []
        
    def create_index(self, use_gpu: bool = False):
        """
        Create a new FAISS index.
        
        Args:
            use_gpu: Whether to use GPU for indexing (requires faiss-gpu)
        """
        # Create a flat L2 index for exact search
        self.index = faiss.IndexFlatL2(self.dimension)
        
        if use_gpu and faiss.get_num_gpus() > 0:
            logger.info("Using GPU for FAISS index")
            res = faiss.StandardGpuResources()
            self.index = faiss.index_cpu_to_gpu(res, 0, self.index)
        else:
            logger.info("Using CPU for FAISS index")
    
    def encode_texts(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """
        Encode texts into embeddings.
        
        Args:
            texts: List of text strings to encode
            batch_size: Batch size for encoding
            
        Returns:
            Numpy array of embeddings
        """
        logger.info(f"Encoding {len(texts)} texts...")
        embeddings = self.encoder.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=True,
            convert_to_numpy=True
        )
        return embeddings.astype('float32')
    
    def add_texts(
        self,
        texts: List[str],
        metadata: List[Dict[str, Any]],
        batch_size: int = 32
    ):
        """
        Add texts to the FAISS index with metadata.
        
        Args:
            texts: List of text strings to add
            metadata: List of metadata dictionaries for each text
            batch_size: Batch size for encoding
        """
        if self.index is None:
            self.create_index()
        
        # Encode texts
        embeddings = self.encode_texts(texts, batch_size)
        
        # Add to index
        self.index.add(embeddings)
        
        # Store metadata
        self.metadata.extend(metadata)
        
        logger.info(f"Added {len(texts)} texts to index. Total: {self.index.ntotal}")
    
    def search(
        self,
        query: str,
        k: int = 5,
        return_scores: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Search for similar texts in the index.
        
        Args:
            query: Query string
            k: Number of results to return
            return_scores: Whether to include similarity scores
            
        Returns:
            List of results with metadata and optional scores
        """
        if self.index is None or self.index.ntotal == 0:
            logger.warning("Index is empty or not created")
            return []
        
        # Encode query
        query_embedding = self.encode_texts([query])[0]
        
        # Search
        distances, indices = self.index.search(
            query_embedding.reshape(1, -1),
            min(k, self.index.ntotal)
        )
        
        # Prepare results
        results = []
        for i, (distance, idx) in enumerate(zip(distances[0], indices[0])):
            if idx < len(self.metadata):
                result = {
                    'rank': i + 1,
                    'metadata': self.metadata[idx].copy()
                }
                if return_scores:
                    # Convert L2 distance to similarity score (0-1 range)
                    # Lower distance = higher similarity
                    similarity = 1 / (1 + distance)
                    result['score'] = float(similarity)
                    result['distance'] = float(distance)
                results.append(result)
        
        return results
    
    def save(self, index_path: str, metadata_path: str, config_path: str):
        """
        Save FAISS index and metadata to disk.
        
        Args:
            index_path: Path to save FAISS index
            metadata_path: Path to save metadata
            config_path: Path to save configuration
        """
        if self.index is None:
            raise ValueError("No index to save")
        
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Save FAISS index
        faiss.write_index(self.index, index_path)
        logger.info(f"Saved FAISS index to {index_path}")
        
        # Save metadata
        with open(metadata_path, 'wb') as f:
            pickle.dump(self.metadata, f)
        logger.info(f"Saved metadata to {metadata_path}")
        
        # Save configuration
        config = {
            'model_name': self.model_name,
            'dimension': self.dimension,
            'total_vectors': self.index.ntotal
        }
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        logger.info(f"Saved configuration to {config_path}")
    
    def load(self, index_path: str, metadata_path: str, config_path: str):
        """
        Load FAISS index and metadata from disk.
        
        Args:
            index_path: Path to FAISS index
            metadata_path: Path to metadata
            config_path: Path to configuration
        """
        # Load configuration
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        self.model_name = config['model_name']
        self.dimension = config['dimension']
        
        # Reinitialize encoder if model changed
        self.encoder = SentenceTransformer(self.model_name)
        
        # Load FAISS index
        self.index = faiss.read_index(index_path)
        logger.info(f"Loaded FAISS index from {index_path} with {self.index.ntotal} vectors")
        
        # Load metadata
        with open(metadata_path, 'rb') as f:
            self.metadata = pickle.load(f)
        logger.info(f"Loaded metadata from {metadata_path}")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the vector database.
        
        Returns:
            Dictionary with statistics
        """
        if self.index is None:
            return {
                'total_vectors': 0,
                'dimension': self.dimension,
                'model_name': self.model_name,
                'is_trained': False
            }
        
        return {
            'total_vectors': self.index.ntotal,
            'dimension': self.dimension,
            'model_name': self.model_name,
            'is_trained': self.index.is_trained,
            'metadata_count': len(self.metadata)
        }


def build_index_from_intents(
    json_path: str,
    output_dir: str = 'data/vector_db',
    model_name: str = 'all-MiniLM-L6-v2',
    batch_size: int = 32
) -> FAISSVectorDB:
    """
    Build FAISS index from intents JSON file.
    
    Args:
        json_path: Path to intents JSON file
        output_dir: Directory to save the vector database
        model_name: Sentence transformer model name
        batch_size: Batch size for encoding
        
    Returns:
        Configured FAISSVectorDB instance
    """
    # Load data
    logger.info(f"Loading data from {json_path}")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    intents = data.get('intents', [])
    logger.info(f"Found {len(intents)} intents")
    
    # Prepare texts and metadata
    texts = []
    metadata = []
    
    for intent in intents:
        tag = intent.get('tag', 'unknown')
        patterns = intent.get('patterns', [])
        responses = intent.get('responses', [])
        
        # Add each pattern with its metadata
        for pattern in patterns:
            texts.append(pattern)
            metadata.append({
                'tag': tag,
                'pattern': pattern,
                'responses': responses,
                'type': 'pattern'
            })
    
    logger.info(f"Prepared {len(texts)} text entries for indexing")
    
    # Create and build index
    vector_db = FAISSVectorDB(model_name=model_name)
    vector_db.add_texts(texts, metadata, batch_size=batch_size)
    
    # Save to disk
    os.makedirs(output_dir, exist_ok=True)
    index_path = os.path.join(output_dir, 'faiss.index')
    metadata_path = os.path.join(output_dir, 'metadata.pkl')
    config_path = os.path.join(output_dir, 'config.json')
    
    vector_db.save(index_path, metadata_path, config_path)
    
    logger.info("Vector database built successfully!")
    return vector_db

