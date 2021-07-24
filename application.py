from fastapi import FastAPI


from apps.posts.router import router as posts_router
from apps.users.router import router as users_router


# Fast api application initialization
app = FastAPI(docs_url='/')
# Including routers for posts and users
app.include_router(posts_router)
app.include_router(users_router)
