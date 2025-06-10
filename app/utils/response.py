from fastapi.responses import JSONResponse

def create_response(data=None, message="Success", status_code=200, code=None,error=False):
    return JSONResponse(
        status_code=status_code,
        content={
            "error": error,
            "message": message,
            "data": data,
            "code": code or status_code,
        }
    )
