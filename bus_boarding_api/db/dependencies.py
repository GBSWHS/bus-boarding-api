from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request


async def get_db_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    session: AsyncSession = request.app.state.db_session_factory()

    try:  # noqa: WPS501
        print('session created')
        yield session
    except Exception as e:
        # logger.error(f"An error occurred: {e}")
        print(e)
        print('session error')
        await session.rollback()
        raise
    finally:
        print('session finally')
        await session.close()
