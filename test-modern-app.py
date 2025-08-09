#!/usr/bin/env python3
"""
Comprehensive test script for the modern voting application.
Tests all functionality including UI, API endpoints, and real-time features.
"""

import requests
import time
import json
import sys
import subprocess
from concurrent.futures import ThreadPoolExecutor
import random
import string

class VotingAppTester:
    def __init__(self, vote_url="http://localhost:5000", result_url="http://localhost:5001"):
        self.vote_url = vote_url
        self.result_url = result_url
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message
        })
        
    def test_vote_app_health(self):
        """Test voting app health endpoint"""
        try:
            response = self.session.get(f"{self.vote_url}/api/health", timeout=10)
            success = response.status_code == 200
            data = response.json() if success else {}
            self.log_test("Vote App Health Check", success, 
                         f"Status: {response.status_code}, Redis: {data.get('redis', 'unknown')}")
            return success
        except Exception as e:
            self.log_test("Vote App Health Check", False, str(e))
            return False
            
    def test_result_app_health(self):
        """Test results app health endpoint"""
        try:
            response = self.session.get(f"{self.result_url}/api/health", timeout=10)
            success = response.status_code == 200
            data = response.json() if success else {}
            self.log_test("Result App Health Check", success, 
                         f"Status: {response.status_code}, DB: {data.get('database', 'unknown')}")
            return success
        except Exception as e:
            self.log_test("Result App Health Check", False, str(e))
            return False
            
    def test_vote_submission(self):
        """Test vote submission functionality"""
        try:
            # Test voting for option A
            response = self.session.post(f"{self.vote_url}/", 
                                       data={'vote': 'a'}, 
                                       timeout=10)
            success = response.status_code == 200
            self.log_test("Vote Submission (Option A)", success, 
                         f"Status: {response.status_code}")
            
            # Test voting for option B
            response = self.session.post(f"{self.vote_url}/", 
                                       data={'vote': 'b'}, 
                                       timeout=10)
            success = response.status_code == 200
            self.log_test("Vote Submission (Option B)", success, 
                         f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("Vote Submission", False, str(e))
            return False
            
    def test_vote_stats_api(self):
        """Test vote statistics API"""
        try:
            response = self.session.get(f"{self.vote_url}/api/stats", timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                votes = data.get('votes', {})
                total = votes.get('total', 0)
                self.log_test("Vote Stats API", success, 
                             f"Total votes: {total}, A: {votes.get('a', 0)}, B: {votes.get('b', 0)}")
            else:
                self.log_test("Vote Stats API", success, f"Status: {response.status_code}")
            return success
        except Exception as e:
            self.log_test("Vote Stats API", False, str(e))
            return False
            
    def test_result_api(self):
        """Test results API"""
        try:
            response = self.session.get(f"{self.result_url}/api/votes", timeout=10)
            success = response.status_code == 200
            if success:
                data = response.json()
                current = data.get('current', {})
                total = data.get('total', 0)
                self.log_test("Result API", success, 
                             f"Total: {total}, Current A: {current.get('a', 0)}, B: {current.get('b', 0)}")
            else:
                self.log_test("Result API", success, f"Status: {response.status_code}")
            return success
        except Exception as e:
            self.log_test("Result API", False, str(e))
            return False
            
    def test_ui_accessibility(self):
        """Test UI accessibility features"""
        try:
            # Test modern voting page
            response = self.session.get(f"{self.vote_url}/", timeout=10)
            success = response.status_code == 200
            if success:
                content = response.text
                # Check for accessibility features
                has_aria = 'aria-' in content
                has_alt_text = 'alt=' in content or 'aria-label' in content
                has_semantic_html = '<main>' in content or '<header>' in content or '<nav>' in content
                
                accessibility_score = sum([has_aria, has_alt_text, has_semantic_html])
                self.log_test("UI Accessibility", accessibility_score >= 2, 
                             f"ARIA: {has_aria}, Alt text: {has_alt_text}, Semantic HTML: {has_semantic_html}")
            else:
                self.log_test("UI Accessibility", False, f"Status: {response.status_code}")
            return success
        except Exception as e:
            self.log_test("UI Accessibility", False, str(e))
            return False
            
    def test_responsive_design(self):
        """Test responsive design by checking CSS"""
        try:
            response = self.session.get(f"{self.vote_url}/", timeout=10)
            success = response.status_code == 200
            if success:
                content = response.text
                # Check for responsive design indicators
                has_viewport = 'viewport' in content
                has_media_queries = '@media' in content or 'responsive' in content.lower()
                has_mobile_friendly = 'mobile' in content.lower() or 'touch' in content.lower()
                
                responsive_score = sum([has_viewport, has_media_queries, has_mobile_friendly])
                self.log_test("Responsive Design", responsive_score >= 1, 
                             f"Viewport: {has_viewport}, Media queries: {has_media_queries}, Mobile: {has_mobile_friendly}")
            else:
                self.log_test("Responsive Design", False, f"Status: {response.status_code}")
            return success
        except Exception as e:
            self.log_test("Responsive Design", False, str(e))
            return False
            
    def test_performance(self):
        """Test application performance"""
        try:
            # Measure response times
            start_time = time.time()
            response = self.session.get(f"{self.vote_url}/", timeout=10)
            vote_response_time = time.time() - start_time
            
            start_time = time.time()
            response = self.session.get(f"{self.result_url}/", timeout=10)
            result_response_time = time.time() - start_time
            
            # Performance thresholds (in seconds)
            vote_fast = vote_response_time < 2.0
            result_fast = result_response_time < 2.0
            
            self.log_test("Performance Test", vote_fast and result_fast, 
                         f"Vote: {vote_response_time:.2f}s, Result: {result_response_time:.2f}s")
            return vote_fast and result_fast
        except Exception as e:
            self.log_test("Performance Test", False, str(e))
            return False
            
    def test_concurrent_voting(self):
        """Test concurrent vote submissions"""
        def submit_vote():
            try:
                option = random.choice(['a', 'b'])
                response = requests.post(f"{self.vote_url}/", 
                                       data={'vote': option}, 
                                       timeout=10)
                return response.status_code == 200
            except:
                return False
                
        try:
            # Submit 10 concurrent votes
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(submit_vote) for _ in range(10)]
                results = [future.result() for future in futures]
                
            success_rate = sum(results) / len(results)
            success = success_rate >= 0.8  # 80% success rate
            
            self.log_test("Concurrent Voting", success, 
                         f"Success rate: {success_rate:.1%} ({sum(results)}/{len(results)})")
            return success
        except Exception as e:
            self.log_test("Concurrent Voting", False, str(e))
            return False
            
    def test_error_handling(self):
        """Test error handling"""
        try:
            # Test invalid vote option
            response = self.session.post(f"{self.vote_url}/", 
                                       data={'vote': 'invalid'}, 
                                       timeout=10)
            handles_invalid = response.status_code in [200, 400]  # Should handle gracefully
            
            # Test non-existent endpoint
            response = self.session.get(f"{self.vote_url}/nonexistent", timeout=10)
            handles_404 = response.status_code == 404
            
            success = handles_invalid and handles_404
            self.log_test("Error Handling", success, 
                         f"Invalid vote: {handles_invalid}, 404 handling: {handles_404}")
            return success
        except Exception as e:
            self.log_test("Error Handling", False, str(e))
            return False
            
    def test_security_headers(self):
        """Test security headers"""
        try:
            response = self.session.get(f"{self.vote_url}/", timeout=10)
            headers = response.headers
            
            # Check for security headers
            has_csp = 'Content-Security-Policy' in headers
            has_xframe = 'X-Frame-Options' in headers
            has_xss = 'X-XSS-Protection' in headers or 'X-Content-Type-Options' in headers
            
            security_score = sum([has_csp, has_xframe, has_xss])
            success = security_score >= 1  # At least one security header
            
            self.log_test("Security Headers", success, 
                         f"CSP: {has_csp}, X-Frame: {has_xframe}, XSS Protection: {has_xss}")
            return success
        except Exception as e:
            self.log_test("Security Headers", False, str(e))
            return False
            
    def run_all_tests(self):
        """Run all tests"""
        print("🚀 Starting Modern Voting App Tests")
        print("=" * 50)
        
        # Basic connectivity tests
        vote_healthy = self.test_vote_app_health()
        result_healthy = self.test_result_app_health()
        
        if not (vote_healthy and result_healthy):
            print("\n❌ Basic health checks failed. Please ensure the applications are running.")
            return False
            
        # Functional tests
        tests = [
            self.test_vote_submission,
            self.test_vote_stats_api,
            self.test_result_api,
            self.test_ui_accessibility,
            self.test_responsive_design,
            self.test_performance,
            self.test_concurrent_voting,
            self.test_error_handling,
            self.test_security_headers,
        ]
        
        print("\n🧪 Running functional tests...")
        for test in tests:
            test()
            time.sleep(0.5)  # Brief pause between tests
            
        # Summary
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        success_rate = passed / total if total > 0 else 0
        
        print(f"Tests passed: {passed}/{total} ({success_rate:.1%})")
        
        if success_rate >= 0.8:
            print("🎉 Overall result: EXCELLENT - App is ready for production!")
        elif success_rate >= 0.6:
            print("✅ Overall result: GOOD - Minor issues to address")
        else:
            print("⚠️  Overall result: NEEDS WORK - Several issues to fix")
            
        # Detailed results
        print("\n📋 Detailed Results:")
        for result in self.test_results:
            status = "✅" if result['success'] else "❌"
            print(f"{status} {result['test']}: {result['message']}")
            
        return success_rate >= 0.8

def check_docker_services():
    """Check if Docker services are running"""
    try:
        result = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout
            vote_running = 'vote' in output
            result_running = 'result' in output
            redis_running = 'redis' in output
            postgres_running = 'postgres' in output or 'db' in output
            
            print("🐳 Docker Services Status:")
            print(f"  Vote app: {'✅' if vote_running else '❌'}")
            print(f"  Result app: {'✅' if result_running else '❌'}")
            print(f"  Redis: {'✅' if redis_running else '❌'}")
            print(f"  PostgreSQL: {'✅' if postgres_running else '❌'}")
            
            return vote_running and result_running and redis_running and postgres_running
        else:
            print("❌ Docker is not running or accessible")
            return False
    except FileNotFoundError:
        print("❌ Docker command not found")
        return False

def main():
    """Main test function"""
    print("🔍 Modern Voting App - Comprehensive Test Suite")
    print("=" * 60)
    
    # Check Docker services first
    if not check_docker_services():
        print("\n⚠️  Some Docker services are not running.")
        print("Please run: docker-compose up -d")
        return False
        
    # Wait for services to be ready
    print("\n⏳ Waiting for services to be ready...")
    time.sleep(10)
    
    # Run tests
    tester = VotingAppTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎊 All tests passed! The modern voting app is working perfectly.")
        return True
    else:
        print("\n🔧 Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
