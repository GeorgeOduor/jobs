from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from jinja2 import FileSystemLoader, Environment
from googleapiclient.discovery import build
from oauth2client import client
import requests
import pickle
import sys
import os

SCOPES = [
    "https://www.googleapis.com/auth/blogger",
    "https://www.googleapis.com/auth/drive.file",
]
BLOG_ID = "5681066692438244789"
credfile = "./blogspot/test.json"


def get_blogger_service_obj(credfile):
    creds = None
    if os.path.exists("auth_token.pickle"):
        with open("auth_token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credfile, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("auth_token.pickle", "wb") as token:
            pickle.dump(creds, token)
    blog_service = build("blogger", "v3", credentials=creds)
    drive_service = build("drive", "v3", credentials=creds)
    return drive_service, blog_service


def create_blog_post(BLOG_ID, api_handler=None, body_content="", isDraft=True):
    try:
        if not api_handler:
            return None
        blogs = api_handler.posts()
        resp = blogs.insert(
            blogId=BLOG_ID, isDraft=isDraft, fetchImages=True, body=body_content
        ).execute()
        print("The blog post has been created successfully")
        return resp
    except Exception as ex:
        print(str(ex))
        return None


def prep_post_template(template_path, template_name, post_data):
    env = Environment(loader=FileSystemLoader(template_path))
    template = env.get_template(template_name)
    return template.render(
        companylogo=post_data["companylogo"],
        companyname=post_data["companyname"],
        location=post_data["location"],
        postingdate=post_data["postingdate"],
        job_desc=post_data["job_desc"],
        applicationlinks=post_data["applicationlinks"],
        protip_status=False,
    )


def post_body(**res):
    try:
        post_df = {
            "companylogo": res["company_logo"],
            "companyname": res["company"],
            "location": res["location"],
            "postingdate": res["posting_time"],
            "job_desc": f"""{res['details']}""",
            "applicationlinks": res["application_link"],
        }
        return post_df
    except Exception as e:
        print("Post Data erorr", e)
        return None


#

#


# out = create_blog_post(BLOG_ID,blog_handler,body_content,isDraft=True)
