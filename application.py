from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from project.routes.api import router as api_router
from project.common.utility import Utility
from project.constant.status_constant import SUCCESS, FAIL
from fastapi.responses import FileResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from typing import List, Dict, Any
from fastapi.responses import JSONResponse

# This way all the tables can be created in database but cannot be updated for that use alembic migrations
# user.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Remmitance-App", description="Remmitance",version="1.0")

# Custom error response format
def format_error_details(errors: List[Dict[str, Any]]) -> Dict[str, Any]:
    formatted_errors = {}
    for error in errors:
        loc = "->".join(str(i) for i in error["loc"])
        print(loc)
        loc = loc.replace("body->","")
        context = error.get("ctx", {})
        reason =context.get("reason",[])
        formatted_errors[str(loc)] = {
            "message": error["msg"],
            "input": error.get("input", ''),
            #"context": context, #error.get("ctx", {})
            "reason":str(reason)
        }
    return formatted_errors

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    formatted_errors = format_error_details(exc.errors())
    
    return JSONResponse({
        "status":422,
        "message":"Validation Error",
        "errors":formatted_errors,
        "code":"INPUT_VALIDATION_ERROR"

    })

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/")
def read_root():
    try:
        return Utility.json_response(status=SUCCESS, message="Welcome to M-Remitence",
                                     error=[], data={})
    except Exception as E:
        print(E)
        return Utility.json_response(status=FAIL, message="Something went wrong", error=[], data={})


@app.get("/media/images/{image}")
def images( image: str):
    file_location = f"project/media/images/{image}"
    return FileResponse(file_location)

# if __name__ == '__main__':
#     uvicorn.run("application:app", host='localhost', port=8000, log_level="debug", reload=True)
#     print("running")
