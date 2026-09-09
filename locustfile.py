from locust import HttpUser, task, between


class StudentLoadTest(HttpUser):

    wait_time = between(2, 5)

    @task
    def open_homepage(self):
        self.client.get("/", name="Homepage")