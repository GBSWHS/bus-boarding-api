import random
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = request.app.state.db_session_factory()

    rand = random.randint(1, 100000000)

    try:  # noqa: WPS501
        print('session created', rand)
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        print('session finally', rand)
        await session.close()
