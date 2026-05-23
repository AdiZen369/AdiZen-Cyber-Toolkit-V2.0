#!/usr/bin/env python3
"""
AdiZenWorks Hash Generator
Cryptographic hash generation tool
Company: AdiZenWorks Inc.
"""

import hashlib
from datetime import datetime
from typing import Dict


class AdiZenHash:
    """Hash generator class"""
    
    def __init__(self):
        self.supported_algorithms = ['md5', 'sha1', 'sha256', 'sha512']
    
    def generate_hash(self, text: str, algorithm: str = "sha256") -> str:
        """
        Generate cryptographic hash
        
        Args:
            text: string to hash
            algorithm: hash algorithm (md5, sha1, sha256, sha512)
        
        Returns:
            hex digest string
        """
        if algorithm not in self.supported_algorithms:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        
        text_bytes = text.encode('utf-8')
        
        if algorithm == "md5":
            hash_obj = hashlib.md5(text_bytes)
        elif algorithm == "sha1":
            hash_obj = hashlib.sha1(text_bytes)
        elif algorithm == "sha256":
            hash_obj = hashlib.sha256(text_bytes)
        elif algorithm == "sha512":
            hash_obj = hashlib.sha512(text_bytes)
        
        return hash_obj.hexdigest()


# Keep backward compatibility
def generate_hash(text, algorithm="sha256"):
    """
    Legacy function for backward compatibility
    
    Args:
        text: string to hash
        algorithm: hash algorithm (md5, sha1, sha256, sha512)
    
    Returns:
        dict with hash results
    """
    results = {
        "input_text": text,
        "algorithm": algorithm,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        text_bytes = text.encode('utf-8')
        
        if algorithm == "md5":
            hash_obj = hashlib.md5(text_bytes)
        elif algorithm == "sha1":
            hash_obj = hashlib.sha1(text_bytes)
        elif algorithm == "sha256":
            hash_obj = hashlib.sha256(text_bytes)
        elif algorithm == "sha512":
            hash_obj = hashlib.sha512(text_bytes)
        else:
            results["error"] = f"Unsupported algorithm: {algorithm}"
            return results
        
        results["hash"] = hash_obj.hexdigest()
        results["hash_length"] = len(results["hash"])
    
    except Exception as e:
        results["error"] = str(e)
    
    return results


if __name__ == "__main__":
    # Test
    print("AdiZenWorks Hash Generator Test")
    print("-" * 40)
    
    hasher = AdiZenHash()
    text = "AdiZenWorks2026"
    
    for algo in ["md5", "sha1", "sha256", "sha512"]:
        hash_result = hasher.generate_hash(text, algo)
        print(f"{algo.upper()}: {hash_result}")
