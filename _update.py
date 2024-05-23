import json
import os
import sys
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/blogger']
CLIENT_SECRETS_FILE = "credentials.json"
REDIRECT_URI = "http://localhost:8080/"
BLOG_ID = os.environ['BLOG_ID']

def main():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    flow.redirect_uri = REDIRECT_URI

    with open(sys.argv[1], 'r') as file:
        soup = BeautifulSoup(file.read())
        
        for img in soup.findAll('img'):
            img['src'] = 'https://github.com/aakashthakare/blog/blob/main/blogposts/' + sys.argv[2] + '/' + img['src'] + '?raw=true'
        
        postid = soup.find(id = 'atptid').string
        title = soup.find(id = 'titleid').string

        soup.find('span', id="atptid").decompose()
        soup.find('span', id="titleid").decompose()

        body = str(soup.find('div', {"id": "post-main"}))

        credentials = flow.run_local_server(port=8080)
        service = googleapiclient.discovery.build('blogger', 'v3', credentials=credentials)

        postBody = {
            "kind": "blogger#post",
            "title": f"{title}",
            "content": f"{body}"
        }

        print(postBody)

        try:
            posts = service.posts()
            request = posts.update(blogId=BLOG_ID, postId=postid, body=postBody)
            response = request.execute()
        except HttpError as error:
            print(f"An error occurred: {error}")

if __name__ == '__main__':
    main()