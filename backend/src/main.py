import random
from datetime import datetime
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.constants import RESPONSES
from src.db import sync_engine, get_db, migrate
from src.schemas.message import APIMessage, RestPostCreateMessageJSONRequest
from src.schemas.thread import APIThread, RestGetThreadsJSONResponse
from src.schemas.user import APIUser
from src.seed import seed
from src.models import Thread, Message, MessageSender, User

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    await migrate()
    await seed()


@app.get("/api/users/me")
async def get_my_user(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return APIUser(id=user.id, name=user.name)


@app.get("/api/threads")
async def get_threads(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    user = result.scalars().first()

    result = await db.execute(
        select(Thread)
        .where(Thread.user_id == user.id)
        .options(joinedload(Thread.messages))
        .order_by(Thread.created_at.desc())
    )
    threads = result.scalars().unique().all()

    # fixme: sort in the query
    for thread in threads:
        thread.messages.sort(key=lambda message: message.created_at)


    if threads is None:
        return RestGetThreadsJSONResponse(threads=[])
    return RestGetThreadsJSONResponse(
        threads=[
            APIThread(
                id=thread.id,
                title=thread.title,
                created_at=thread.created_at,
                messages=[
                    APIMessage(
                        id=message.id,
                        thread_id=message.thread_id,
                        sender=message.sender,
                        content=message.content,
                        created_at=message.created_at,
                    )
                    for message in thread.messages
                ],
            )
            for thread in threads
        ]
    )


# todo: thread names will be determine by ai analysis, such as in claude
@app.post("/api/thread")
async def create_thread(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    user = result.scalars().first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    thread = Thread(user_id=user.id)
    db.add(thread)
    await db.commit()
    await db.refresh(thread)

    print(f"Thread created: {thread.id}")

    return APIThread(
        id=thread.id, title=thread.title, created_at=thread.created_at, messages=[]
    )


@app.post("/api/threads/{thread_id}/messages")
async def post_message_to_thread(
    thread_id: int,
    request: RestPostCreateMessageJSONRequest,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Thread).where(Thread.id == thread_id))
    thread = result.scalars().first()

    if thread is None:
        raise HTTPException(status_code=404, detail="Thread not found")

    result = await db.execute(select(User))
    user = result.scalars().first()

    # todo: check that user is the owner of the thread (when we have more users)
    # todo: fetch index of the previous message and add an index field
    message = Message(
        thread_id=thread.id, sender=MessageSender.human, content=request.content
    )
    db.add(message)
    await db.commit()
    await db.refresh(message)

    content = RESPONSES[random.randint(0, len(RESPONSES) - 1)]
    response = Message(
        thread_id=thread.id, sender=MessageSender.system, content=content
    )
    db.add(response)

    await db.commit()
    await db.refresh(response)

    return APIMessage(
        id=response.id,
        thread_id=response.thread_id,
        sender=response.sender,
        content=response.content,
        created_at=response.created_at,
    )
