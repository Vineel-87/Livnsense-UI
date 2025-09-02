from locust import HttpUser, task, between
import json

class VicasUser(HttpUser):
    wait_time = between(1, 5)  # Simulate wait time between tasks (like real users)

    def on_start(self):
        """Runs once for each simulated user - Login first"""
        self.login()

    def login(self):
        # Replace with actual login endpoint and credentials
        login_url = "/vicas-backend/api/v1/user/login"  # Update this path to the real login API
        payload = {
            "username": "pydi.vineel",       # Replace with actual username
            "password": "Vineel@lns123"        # Replace with actual password
        }

        headers = {
            "Content-Type": "application/json"
        }

        with self.client.post(login_url, data=json.dumps(payload), headers=headers, catch_response=True) as response:
            if response.status_code == 200 and "token" in response.text:
                self.token = response.json().get("token")
                response.success()
            else:
                response.failure("Login failed")

    @task
    def load_dashboard(self):
        # Simulate accessing dashboard API after login
        dashboard_url = "/vicas-backend/api/v1/dashboard/data"  # Replace with actual endpoint

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        with self.client.get(dashboard_url, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Dashboard load failed: {response.status_code}")
