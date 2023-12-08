# Fast API
from fastapi import FastAPI, HTTPException, status, Response
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating : Optional[int] = None


my_posts = [
    {"title": "Hello guys", "content": "Bigges youtube channel", "id": 1},
    {"title": "Sai Baba", "content": "Bigges channel", "id": 2},
]


# Get Id from the my_post array
def get_id(id):
    for p in my_posts:
        if p["id"] == id:
            return p


# Get Index from the my_post array
def get_post_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"Message": "Eniola"}


# Getting all post
@app.get("/posts")
async def get_posts():
    return {"data": my_posts}


# Creating a post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = randrange(0, 10000)
    my_posts.append(post_dict)
    return {"data": post_dict}


# Getting an Individual post
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = get_id(id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} not found"
        )
    return {"data": post}


# Deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # Deleting a post
    index = get_post_index(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with this {id} has been deleted",
        )
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Updating a Post     
@app.put("/posts/{id}")
def update_posts(id: int, post: Post):
    index = get_post_index(id)
    if index == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with this {id} not found",
        )
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
    