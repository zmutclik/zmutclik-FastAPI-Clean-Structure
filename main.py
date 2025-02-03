if __name__ == "__main__":
    from core.db.engine.core import coredb_create_all
    from core.db.engine.auth import authdb_create_all
    from core.db.engine.menu import menudb_create_all
    from core.db.engine.app import appdb_create_all
    from core.db.engine.security import securitydb_create_all

    coredb_create_all()
    authdb_create_all()
    menudb_create_all()
    appdb_create_all()
    securitydb_create_all()

    import uvicorn
    from core.config import config

    print("")
    print("\033[34mSERVER\033[0m:", config.APP_HOST + ":" + str(config.APP_PORT))
    print("\033[34mDEBUG\033[0m:", config.DEBUG)
    print("\033[34mENV\033[0m:", config.ENV)
    print("")

    uvicorn.run(
        app="app:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True if config.ENV != "production" else False,
        log_level="debug" if config.DEBUG else "warning",
        workers=1,
    )
