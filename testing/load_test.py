from locust import HttpUser, task, between
from config import TEST_CONFIG

class CareerGuideLoadTest(HttpUser):
    wait_time = between(1, 3)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = None
    
    def on_start(self):
        """Login at the start of each user session"""
        response = self.client.post("/login", json={
            "email": TEST_CONFIG["test_user"]["email"],
            "password": TEST_CONFIG["test_user"]["password"]
        })
        if response.status_code == 200:
            self.user_id = response.json().get('user_id')
    
    @task(1)
    def view_dashboard(self):
        """Test dashboard endpoint"""
        if self.user_id:
            with self.client.get(
                "/recommend",
                json={"user_id": self.user_id},
                catch_response=True
            ) as response:
                if response.status_code != 200:
                    response.failure(f"Failed to load dashboard: {response.text}")
    
    @task(2)
    def submit_assessment(self):
        """Test assessment submission"""
        if self.user_id:
            payload = {
                "user_id": self.user_id,
                "responses": [
                    {"adjective": "calm", "question_type": "Self-description"},
                    {"adjective": "organized", "question_type": "Expected"}
                ]
            }
            with self.client.post(
                "/submit_assessment",
                json=payload,
                catch_response=True
            ) as response:
                if response.status_code != 200:
                    response.failure(f"Failed to submit assessment: {response.text}")
    
    @task(3)
    def get_skills(self):
        """Test skills endpoint"""
        with self.client.get("/skills", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get skills: {response.text}")

def run_load_test():
    """Run load test using configuration"""
    import subprocess
    import os
    
    cmd = (
        f"locust -f {os.path.realpath(__file__)} "
        f"--headless "
        f"--users {TEST_CONFIG['load_test']['users']} "
        f"--spawn-rate {TEST_CONFIG['load_test']['spawn_rate']} "
        f"--run-time {TEST_CONFIG['load_test']['duration']}s "
        f"--host={TEST_CONFIG['host']} "
        "--html=load_test_report.html"
    )
    
    subprocess.call(cmd.split())

if __name__ == "__main__":
    run_load_test()