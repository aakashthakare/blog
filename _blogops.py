import json
import os
import sys
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/blogger']
TOKEN_FILE = os.environ['TOKEN_FILE']
BLOG_ID = os.environ['BLOG_ID']

def refresh_token():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], SCOPES)
    flow.redirect_uri = os.environ['REDIRECT_URI']
    credentials = flow.run_local_server(port=8080)
    
    with open(TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())

def init():
    service = _init_service_()
    title = sys.argv[2]
    
    post_body = {
        "kind": "blogger#post",
        "title": f'"{title}"'
    }

    try:
        posts = service.posts()
        request = posts.insert(blogId=BLOG_ID, isDraft=True, body=post_body)
        response = request.execute()
        postId = response['id']
        
        folderPath = f'./blogposts/{title}'
        os.mkdir(folderPath)
        os.mkdir(f'{folderPath}/images')
        
        mdfile = open(f"{folderPath}/{title}.md", "w")
        mdfile.write(f"""---
layout: post
permalink: /
title: {title}
post: {postId}
---
""")
        
        print(f"Draft created with ID: {postId}")
    except HttpError as error:
        print(f"An error occurred: {error}")

def update():
    post = _post_()
    service = _init_service_()

    try:
        posts = service.posts()
        request = posts.update(blogId=BLOG_ID, postId=post[0], body=post[1])
        response = request.execute()
    except HttpError as error:
        print(f"An error occurred: {error}")

def _init_service_():
    credentials = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    service = googleapiclient.discovery.build('blogger', 'v3', credentials=credentials)
    return service

def _post_():
    with open(sys.argv[2], 'r') as file:
        soup = BeautifulSoup(file.read(), "html.parser")
            
        for img in soup.findAll('img'):
            img['src'] = 'https://github.com/aakashthakare/blog/blob/main/blogposts/' + sys.argv[2] + '/' + img['src'] + '?raw=true'
        
        postid = soup.find(id = 'atptid').string
        title = soup.find(id = 'titleid').string

        soup.find('span', id="atptid").decompose()
        soup.find('span', id="titleid").decompose()

        body = str(soup.find('div', {"id": "post-main"}))

        post_html = {
            "kind": "blogger#post",
            "title": f"{title}",
            "content": f"{body}"
        }

        return postid, post_html

if __name__ == '__main__':
    globals()[sys.argv[1]]()