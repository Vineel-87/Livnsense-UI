from locust import HttpUser, task, between
import json

class VicasUser(HttpUser):
    wait_time = between(1, 2)  # simulate think time between tasks

    def on_start(self):
        # This runs once per simulated user at start
        self.login()

    def login(self):
        response = self.client.post(
            "/api/authenticate",  # Adjust this endpoint if needed
            headers={"Content-Type": "application/json"},
            data=json.dumps({
                "username": "pydi.vineel",  # replace with actual test username
                "password": "Vineel@lns123"   # replace with actual test password
            })
        )

        if response.status_code == 200:
            self.token = response.json()["vicas_token"]  # Fix: define self.token
        else:
            print("Login failed:", response.status_code)
            self.token = None  # prevent crash

    @task
    def load_dashboard(self):
        if not self.token:
            return  # skip if login failed

        with self.client.get(
            "/api/dashboard",  # Adjust this API path to your real dashboard API
            headers={"Authorization": f"Bearer {self.token}"},
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Dashboard load failed: {response.status_code}")
