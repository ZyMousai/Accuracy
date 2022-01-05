def create_table():
    import asyncio
    from sql_models.db_config import Base

    async def async_main():
        from config import globals_config
        from sqlalchemy.ext.asyncio import create_async_engine

        async_egn = create_async_engine(globals_config.MYSQL_URL)

        async with async_egn.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        await async_egn.dispose()

    asyncio.run(async_main())
