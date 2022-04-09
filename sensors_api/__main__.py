import uvicorn

if __name__ == "__main__":
    uvicorn.run("sensors_api:app", debug=True, reload=True, host="0.0.0.0")
