from sqlalchemy.exc import OperationalError, ArgumentError
from core.config import  config


def appdb_create_all():
    try:
        from sqlalchemy import create_engine
        dbapps_engine = create_engine(config.DBAPPS_URL.replace("aiomysql", "pymysql"))
        with dbapps_engine.begin() as connection:
            if not dbapps_engine.dialect.has_table(table_name="app", connection=connection):
                from ..base import Base

                Base.metadata.create_all(bind=dbapps_engine)
    except ArgumentError as err:
        print(err)

    except OperationalError as err:
        if "1045" in err.args[0]:
            print("DATABASE APPS : Access Denied")
        elif "1698" in err.args[0]:
            print("DATABASE APPS : Access Denied")
        elif "2003" in err.args[0]:
            print("DATABASE APPS : Connection Refused")
        elif "Could not parse SQLAlchemy URL from string" in err.args[0]:
            print("DATABASE APPS : URL Enggine ERROR")
        else:
            raise
