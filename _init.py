import json
import os
import sys
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/blogger']
CLIENT_SECRETS_FILE = "credentials.json"
REDIRECT_URI = "http://localhost:8080/"
BLOG_ID = os.environ['BLOG_ID']

def main():
    title = sys.argv[1].replace(" ", "_")
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    flow.redirect_uri = REDIRECT_URI
    
    credentials = flow.run_local_server(port=8080)

    service = googleapiclient.discovery.build('blogger', 'v3', credentials=credentials)

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


if __name__ == '__main__':
    main()