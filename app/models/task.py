from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional

class Task(Document):
    task : str = Field(..., max_length=100)
    description:Optional[str] = Field(None, max_length=1000)
    completed : bool = Field(default=False)
    created_at : datetime = Field(default_factory= datetime.utcnow)
    updated_at : datetime = Field(default_factory=datetime.utcnow)

    class Settings():
        name = "tasks"

    class Config():
        json_schema_extra={
            "example":{
                "task":"make a FastAPI project!",
                "description":"this is a Personal task management API project",
                "completed":False
            }
        }


    async def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return await super().save(*args, **kwargs)