import os
import sys
import uvicorn


def runserver():
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


def makemigrations():
    print("Alembic migrations would run here.")


def migrate():
    from app.infrastructure.db.tables import Base
    from app.infrastructure.db.session import engine
    import asyncio

    async def init():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("Database tables created successfully.")

    asyncio.run(init())


if __name__ == "__main__":
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    if len(sys.argv) < 2:
        print("Usage: python manage.py [runserver|migrate]")
        exit(1)

    cmd = sys.argv[1]

    if cmd == "runserver":
        runserver()
    elif cmd == "migrate":
        migrate()
    else:
        print(f"Unknown command: {cmd}")
