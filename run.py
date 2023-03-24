import uvicorn
from api.controllers.urls import app

if __name__ == '__main__':
    uvicorn.run(app=app) 
