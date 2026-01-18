from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Simulate think time between actions

    @task
    def load_homepage(self):
        self.client.get("/")

    @task
    def load_leaderboard(self):
        self.client.get("/leaderboard")

    @task
    def login_with_valid_email(self):
        self.client.post("/showSummary", data = {
            "email": "john@simplylift.co"
        })