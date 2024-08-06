from fastapi import FastAPI

app = FastAPI(debug=True)


POSTS = ["Hello world!", "Some other post"]


@app.get("/")
def get_index():
	return "Hello!"


@app.get("/posts")
async def get_posts():
    return {"posts": POSTS}


@app.get("/posts/mine")
def get_post_mine():
	return {"posts": ["User posts"]}

@app.get("/posts/{post_id}")
async def get_post(post_id: int):
	return {"post": POSTS[post_id]}
