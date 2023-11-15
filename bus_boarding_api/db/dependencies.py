import random
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = request.app.state.db_session_factory()

    rand = random.randint(10000000, 99999999)

    try:  # noqa: WPS501
        print('session created v2', rand)
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        print('session finally v2', rand)
        await session.close()
