from locust import HttpUser, task, between
import random

class DataBenchmarkUser(HttpUser):
    # Wait between 0.1 to 1 second between requests
    wait_time = between(0.1, 1.0)
    
    @task
    def test_aggregation(self):
        # Randomly select a category to prevent caching shortcuts
        category = random.choice(["A", "B", "C", "D", "E"])
        
        # NOTE: To test Pandas, start Locust pointing to http://localhost:8000
        # To test Polars, point Locust to http://localhost:8001
        self.client.get(f"/aggregate/{category}", name="/aggregate/[category]")