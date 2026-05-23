#!/usr/bin/env python3
"""
AdiZenWorks Cybersecurity Toolkit V2.0 - Test Suite
© 2026 AdiZenWorks Inc.

Basic unit tests for security tools
"""

import sys
import os
import unittest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import tools
try:
    from adizenhash import generate_hash
    from adizenports import scan_ports
    from adizensecurity import audit_security
    TOOLS_AVAILABLE = True
except ImportError:
    TOOLS_AVAILABLE = False
    print("Warning: Tool modules not available for testing")


class TestHashGenerator(unittest.TestCase):
    """Test hash generation functionality"""
    
    @unittest.skipIf(not TOOLS_AVAILABLE, "Tools not available")
    def test_sha256_hash(self):
        """Test SHA-256 hash generation"""
        result = generate_hash("test", "sha256")
        self.assertIn('hash', result)
        self.assertEqual(len(result['hash']), 64)  # SHA-256 is 64 hex chars
    
    @unittest.skipIf(not TOOLS_AVAILABLE, "Tools not available")
    def test_md5_hash(self):
        """Test MD5 hash generation"""
        result = generate_hash("test", "md5")
        self.assertIn('hash', result)
        self.assertEqual(len(result['hash']), 32)  # MD5 is 32 hex chars
    
    @unittest.skipIf(not TOOLS_AVAILABLE, "Tools not available")
    def test_invalid_algorithm(self):
        """Test handling of invalid algorithm"""
        result = generate_hash("test", "invalid")
        self.assertIn('error', result)


class TestPortScanner(unittest.TestCase):
    """Test port scanning functionality"""
    
    @unittest.skipIf(not TOOLS_AVAILABLE, "Tools not available")
    def test_single_port(self):
        """Test scanning a single port"""
        result = scan_ports("localhost", "80")
        self.assertIn('target', result)
        self.assertIn('open_ports', result)
    
    @unittest.skipIf(not TOOLS_AVAILABLE, "Tools not available")
    def test_invalid_hostname(self):
        """Test handling of invalid hostname"""
        result = scan_ports("invalid.hostname.that.does.not.exist", "80")
        self.assertIn('error', result)


class TestSecurityAuditor(unittest.TestCase):
    """Test security auditing functionality"""
    
    @unittest.skipIf(not TOOLS_AVAILABLE, "Tools not available")
    def test_valid_url(self):
        """Test auditing a valid URL"""
        result = audit_security("https://example.com")
        self.assertIn('url', result)
        self.assertIn('score', result)
    
    @unittest.skipIf(not TOOLS_AVAILABLE, "Tools not available")
    def test_invalid_url(self):
        """Test handling of invalid URL"""
        result = audit_security("not-a-valid-url")
        self.assertIn('error', result)


def run_tests():
    """Run all tests"""
    print("=" * 70)
    print("AdiZenWorks Cybersecurity Toolkit V2.0 - Test Suite")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestHashGenerator))
    suite.addTests(loader.loadTestsFromTestCase(TestPortScanner))
    suite.addTests(loader.loadTestsFromTestCase(TestSecurityAuditor))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())