from typing import Callable
from databases import Database
from fastapi import FastAPI
from sshtunnel import SSHTunnelForwarder

async def connect_server(app: FastAPI):
    config = app.state.config
    server_started = False
    server = None
    try:
        server = SSHTunnelForwarder(
            (config.SSH_ADDR, 22),
            ssh_username=config.SSH_USER,
            ssh_password=config.SSH_PASSWORD,
            ssh_private_key_password=config.PKEY_PASS,
            remote_bind_address=('localhost', 5432)
        )
        print('connecting...')
        server.start()
        is_active = server.is_active
        if is_active:
            print("server connected")
            server_started = True
            return server
        else:
            return None
    except Exception:
        if server_started:
            server.stop()
        raise


async def _get_db_url(app: FastAPI) -> str:
    config = app.state.config
    db_url = None

    if config.ENV == 'local':
        try:
            server = await connect_server(app=app)
            if server is not None:
                app.state.server = server
                db_url = app.state.config.get_db_url(app.state.server.local_bind_port)
        except Exception as e:
            raise RuntimeError from e
    elif config.ENV == 'prod':
        db_url = config.DATABASE_URL

    return db_url


def create_db(app: FastAPI) -> Callable:
    async def _create_db_connection() -> None:
        config = app.state.config
        print(f'env: {config.ENV}')

        db_url = await _get_db_url(app=app)

        if db_url:
            app.state.database = Database(
                url=db_url,
                min_size=config.MIN_DB_POOL_SIZE,
                max_size=config.MAX_DB_POOL_SIZE
            )
            await app.state.database.connect()

    return _create_db_connection


def close_db(app: FastAPI) -> Callable:
    async def _close_db_connection() -> None:
        await app.state.database.disconnect()
        if app.state.config.ENV == 'local':
            if app.state.server.is_active:
                app.state.server.stop()
                print('server stopped')
    return _close_db_connection
