from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession


def new_session_maker(db_url: str):
    engine = create_async_engine(
        db_url,
        echo=True
    )

    maker = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
        class_=AsyncSession
    )
    return maker
