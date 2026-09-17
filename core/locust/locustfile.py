from locust import HttpUser, task


class HelloWorldUser(HttpUser):

    def on_start(self):
        response = self.client.post(
            "/accounts/api/v1/jwt/create/",
            json={
                "email": "admin@gmail.com",
                "password": "123",
            },
        )



        if response.status_code != 200:
            raise Exception(
                f"Login failed: {response.status_code}"
            )

        data = response.json()

        self.headers = {
            "Authorization": f"Bearer {data['access']}"
        }

    @task
    def hello_world(self):
        response = self.client.get(
            "/task/api/v1/my-task",
            headers=self.headers,
        )

        print("TASK STATUS:", response.status_code)