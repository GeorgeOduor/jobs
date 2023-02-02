from requests import get, post

api_key = "AIzaSyCpZAfG7Gdeg8hBvzdCk7xXcRtpEU194E8"
blog_id = "5681066692438244789"
url = "https://www.googleapis.com/blogger/v3/blogs/5681066692438244789?key=AIzaSyCpZAfG7Gdeg8hBvzdCk7xXcRtpEU194E8"
access_token = "ya29.a0AVvZVsqWl1iv1T3ii125wmReXcxd3e1xn0vrx-IGHzY8J9fefJ5cYNqea6uFi7tDkvLnpPivwD17lrLSHSsZHTs2EeCzWR4EGz1RnS4_whKJdyOvOv4sTiRalbKgCau7TXmoWJImq26ec-Ziqo-Gt17zlIOmLz0aCgYKAfMSAQASFQGbdwaIXXpBQj2RxIgevRw65Zg4RQ0166"
authcode = "4/0AWtgzh7gVpQ5SSAQ9D_Oe9_PhpHS3UWlBzLbpocyFGSfZrE8yvwNvm6w35vrC5TdIk4CAQ"
resp = get(url=url)

import requests


def create_post(blog_id, access_token, post_data):
    endpoint = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    response = requests.post(endpoint, headers=headers, json=post_data)
    if response.status_code == 200:
        return response.json()
    else:
        return None


post_data = {"title": "Example Post", "content": "Example content"}

result = create_post(blog_id, access_token, post_data)
if result:
    print("Post created successfully")
else:
    print("Error creating post")

