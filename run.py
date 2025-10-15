import uvicorn

if __name__ == "__main__":
    uvicorn.run(app="main:app",
                reload=True,
                limit_max_requests=200,
                limit_concurrency=200,
                timeout_keep_alive=5)