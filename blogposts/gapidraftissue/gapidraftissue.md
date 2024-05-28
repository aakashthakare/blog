---
layout: post
permalink: /
title: Blogger API fetch drafts
post: 1263537549660620918
labels:
---

Google provides APIs to integrate your system with existing Google services for various purpose. I started exploring APIs related to Blogger for this Blog to automate things and building a convinient system of writing and publishing blog. I came across with one scenario which I would like to share.

While fetching the drafts with the help of [Blogger API v3](https://developers.google.com/blogger/docs/3.0/using), I realized the API was not returning the drafts. Even after supplying the post id or the status it was returning `404 Not Found`. 

```
draft_post = service.posts().get(blogId=blog_id, postId=post_id).execute()
```

This is an intended behavior from the API, for some reason the GET API is not returning the draft post. Following was a loose attempt to make it work, but failed. However, every other source was claiming this to be working, but wasn't.

```
draft_post = service.posts().get(blogId=blog_id, postId=post_id, status='DRAFT').execute()
```

While looking for the solution in different sources, I found this 4 year old thread,

[Unable to retrieve "scheduled" and "draft" posts while using the blooger v3 api](https://support.google.com/blogger/thread/65092593/unable-to-retrieve-scheduled-and-draft-posts-while-using-the-blooger-v3-api?hl=en)


So, I had no option but to switch to this method of fetching the draft post, it's not a cleaner way but still, nothing else I can do about it. The solution looks like this,

```
draft_posts = service.posts().list(blogId=blog_id, status='DRAFT').execute()

if 'items' in draft_posts:
    for post in draft_posts['items']:
        if post['id'] == post_id:
            print("Draft post found.")
else:
    print("No draft posts found")
```

Same thing applies to scheduled post as well, we have to fetch all the posts and filter respectively. It's not something related to the python library, with other languages as well the same result is being returned. 

I spend some time to identify why the API is not returning unpublished post with the help of GET API but couldn't find any official clarification for the same. I feel, it's by design not returning the unpublished ones to avoid any repercussions while doing some operations on the returned post considering them as published.