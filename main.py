import uvicorn
from core import config

if __name__ == "__main__":
    print("")
    print("ENV = ", config.ENV)
    print("")
    
    uvicorn.run(
        app="app:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True if config.ENV != "production" else False,
        workers=1,
    )
