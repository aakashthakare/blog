import os
import sys
import google_auth_oauthlib.flow
import googleapiclient.discovery

from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/blogger']
TOKEN_FILE = os.environ['TOKEN_FILE']
BLOG_ID = os.environ['BLOG_ID']

def refresh_token():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(os.environ['GOOGLE_APPLICATION_CREDENTIALS'], SCOPES)
    flow.redirect_uri = os.environ['REDIRECT_URI']
    credentials = flow.run_local_server(port=8080)
    
    with open(TOKEN_FILE, 'w') as token:
        token.write(credentials.to_json())

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
labels:
---
""")
        
        print(f"Draft created with ID: {postId}")
    except HttpError as error:
        print(f"An error occurred: {error}")

def publish():
    post_id = _postid_()
    service = _init_service_()

    draft_posts = service.posts().list(blogId=BLOG_ID, status='DRAFT').execute()

    if 'items' in draft_posts:
        for post in draft_posts['items']:
            if post['id'] == post_id:
                post['status'] = 'LIVE'
                published = service.posts().publish(blogId=BLOG_ID, postId=post_id).execute()
                print(f"Draft post published at: {published['url']}")
    else:
        print(f"No draft posts found with given id : {post_id}.")

def draft():
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

def _postid_():
    with open(sys.argv[2], 'r') as file:
        soup = BeautifulSoup(file.read(), "html.parser")
        postid = soup.find(id = 'atptid').string
        return postid

def _post_():
    with open(sys.argv[2], 'r') as file:
        soup = BeautifulSoup(file.read(), "html.parser")
            
        for img in soup.findAll('img'):
            img['src'] = 'https://github.com/aakashthakare/blog/blob/draft/' + sys.argv[3] + '/blogposts/' + sys.argv[3] + '/' + img['src'] + '?raw=true'
        
        postid = soup.find(id = 'atptid').string
        title = soup.find(id = 'titleid').string

        labelStr = soup.find(id = 'labelsid').string
        labels = []
        if labelStr:
            labels = labelStr.split(",")

        soup.find('span', id="atptid").decompose()
        soup.find('span', id="titleid").decompose()
        soup.find('span', id="labelsid").decompose()

        body = str(soup.find('div', {"id": "post-main"}))

        post_html = {
            "kind": "blogger#post",
            "title": f"{title}",
            "content": f"{body}",
            "labels": labels
        }

        return postid, post_html

if __name__ == '__main__':
    globals()[sys.argv[1]]()