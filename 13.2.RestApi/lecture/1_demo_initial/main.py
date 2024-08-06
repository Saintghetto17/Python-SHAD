from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get_index():
	return "Hello!"


@app.get("/posts")
async def get_posts():
    return {"posts": ["Hello world!", "Some other post"]}