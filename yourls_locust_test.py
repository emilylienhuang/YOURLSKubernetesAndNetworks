from locust import HttpUser, task, between

class YourlsLoadTest(HttpUser):
    wait_time = between(1, 2)  # Simulates user wait time

    @task
    def test_redirect(self):
        self.client.get("/")  # Replace with a valid short URL path if needed
