import time

from fastapi import Request, Response, HTTPException

from modules.logger import logger


async def log_middleware(request: Request, call_next):
    log_dict = {
        'url': request.url.path,
        'method': request.method,
    }

    try:
        start_time = time.time()
        response: Response = await call_next(request)
        request_time = time.time() - start_time
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(status_code=500, detail="Internal server error")
    
    log_dict['status_code'] = response.status_code
    log_dict['request_time'] = request_time

    logger.info(log_dict, extra=log_dict)

    return response