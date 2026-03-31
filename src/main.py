from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.config import settings

print(f"{settings.DB_NAME=}")


app = FastAPI(title="Hotels Booking")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
