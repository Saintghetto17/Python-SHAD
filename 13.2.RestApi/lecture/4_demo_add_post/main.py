from fastapi import FastAPI, Request, HTTPException
from fastapi import status
from fastapi.responses import JSONResponse, PlainTextResponse
from pydantic import BaseModel

app = FastAPI(debug=True)


class Post(BaseModel):
    text: str


POSTS = [
    {"text": "Hello world!"},
    {"text": "Some other post"},
]


@app.exception_handler(IndexError)
def index_error_handler(request: Request, exc: IndexError):
    # return JSONResponse(
    #   status_code=404,
    #   content={"message": "No such element"}
    # )
    return PlainTextResponse("No such element", status_code=404)


@app.get("/")
def get_index():
    return "Hello!"


@app.get("/posts")
async def get_posts():
    return {"posts": POSTS}


#@app.post("/posts", status_code=201)
@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    post_dict = post.dict()
    POSTS.append(post_dict)
    return {"message": "Post added"}


@app.get("/posts/mine")
def get_post_mine():
    return {"posts": ["User posts"]}


@app.get("/posts/{post_id}")
async def get_post(post_id: int):
    if post_id == 42:
        raise HTTPException(status_code=418, detail="42 is forbidden.")
    return {"post": POSTS[post_id]}
