import requests
import time
import concurrent.futures
import statistics
import json
from datetime import datetime
from config import TEST_CONFIG

class StressTest:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.user_id = None
    
    def setup(self):
        """Setup authentication"""
        try:
            response = self.session.post(
                f"{TEST_CONFIG['host']}/login",
                json=TEST_CONFIG['test_user']
            )
            if response.status_code == 200:
                self.user_id = response.json().get('user_id')
                return True
        except Exception as e:
            print(f"Setup failed: {str(e)}")
            return False
    
    def test_endpoint(self, endpoint, method='GET', data=None):
        """Test single endpoint"""
        response_times = []
        success_count = 0
        error_count = 0
        errors = []
        
        def make_request():
            try:
                start_time = time.time()
                
                if method == 'GET':
                    response = self.session.get(f"{TEST_CONFIG['host']}{endpoint}")
                else:
                    response = self.session.post(
                        f"{TEST_CONFIG['host']}{endpoint}",
                        json=data
                    )
                
                end_time = time.time()
                
                return {
                    'success': response.status_code == 200,
                    'time': end_time - start_time,
                    'status_code': response.status_code
                }
            except Exception as e:
                return {
                    'success': False,
                    'error': str(e)
                }
        
        # Execute parallel requests
        with concurrent.futures.ThreadPoolExecutor(
            max_workers=TEST_CONFIG['stress_test']['max_workers']
        ) as executor:
            futures = {
                executor.submit(make_request): i 
                for i in range(TEST_CONFIG['stress_test']['num_requests'])
            }
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result.get('success'):
                    success_count += 1
                    response_times.append(result['time'])
                else:
                    error_count += 1
                    errors.append(result.get('error'))
        
        # Calculate metrics
        return {
            'total_requests': TEST_CONFIG['stress_test']['num_requests'],
            'successful_requests': success_count,
            'failed_requests': error_count,
            'success_rate': (success_count / TEST_CONFIG['stress_test']['num_requests']) * 100,
            'avg_response_time': statistics.mean(response_times) if response_times else 0,
            'median_response_time': statistics.median(response_times) if response_times else 0,
            'min_response_time': min(response_times) if response_times else 0,
            'max_response_time': max(response_times) if response_times else 0,
            'requests_per_second': TEST_CONFIG['stress_test']['num_requests'] / sum(response_times) if response_times else 0,
            'errors': errors[:5]  # Include first 5 errors for debugging
        }

def run_stress_tests():
    """Run stress tests on all endpoints"""
    tester = StressTest()
    if not tester.setup():
        print("Failed to setup stress test")
        return
    
    # Define endpoints to test
    endpoints = [
        {
            'name': 'Login',
            'path': '/login',
            'method': 'POST',
            'data': TEST_CONFIG['test_user']
        },
        {
            'name': 'Dashboard',
            'path': '/recommend',
            'method': 'POST',
            'data': {'user_id': tester.user_id}
        },
        {
            'name': 'Skills',
            'path': '/skills',
            'method': 'GET'
        },
        {
            'name': 'Assessment',
            'path': '/submit_assessment',
            'method': 'POST',
            'data': {
                'user_id': tester.user_id,
                'responses': [{"adjective": "calm", "question_type": "Self-description"}]
            }
        }
    ]
    
    # Run tests and collect results
    results = {}
    for endpoint in endpoints:
        print(f"\nTesting: {endpoint['name']}")
        metrics = tester.test_endpoint(
            endpoint['path'],
            method=endpoint['method'],
            data=endpoint.get('data')
        )
        results[endpoint['name']] = metrics
    
    # Save results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'stress_test_results_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nTest results saved to {filename}")
    print("\nSummary:")
    for name, metrics in results.items():
        print(f"\n{name}:")
        print(f"Success Rate: {metrics['success_rate']:.2f}%")
        print(f"Avg Response Time: {metrics['avg_response_time']*1000:.2f}ms")
        print(f"Requests/second: {metrics['requests_per_second']:.2f}")

if __name__ == "__main__":
    run_stress_tests()