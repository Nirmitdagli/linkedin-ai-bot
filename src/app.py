from src.database import fetch_pending_posts, approve_post
from src.linkedin_api import post_to_linkedin
from fastapi import FastAPI

app = FastAPI()

@app.get("/pending_posts")
def get_pending_posts():
    return fetch_pending_posts()

@app.get("/approve_post/{post_id}")
def approve_and_post(post_id: int):
    approve_post(post_id)
    
    # Fetch post content
    pending_posts = fetch_pending_posts()
    for post in pending_posts:
        if post[0] == post_id:
            status_code, response = post_to_linkedin(post[1])
            if status_code == 201:
                return {"message": "Post approved and published successfully."}
    return {"error": "Post not found or already approved."}

