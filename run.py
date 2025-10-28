import uvicorn

if __name__ == "__main__":
    uvicorn.run(app="main:app",
                workers=7,
                limit_max_requests=180,
                limit_concurrency=180,)