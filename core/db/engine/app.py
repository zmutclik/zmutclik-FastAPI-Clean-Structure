from sqlalchemy.exc import OperationalError, ArgumentError
from core.config import config


def appdb_create_all():
    try:
        from sqlalchemy import create_engine

        data_dbapps = config.REPOSITORY["DBAPPS_URL_DEFAULT"]
        dbapps_engine = create_engine(data_dbapps.datalink.replace("aiomysql", "pymysql"))
        with dbapps_engine.begin() as connection:
            if not dbapps_engine.dialect.has_table(table_name="app", connection=connection):
                from ..base import Base

                Base.metadata.create_all(bind=dbapps_engine)
    except KeyError as err:
        print("\033[33mWARNING\033[0m: ", "REPOSITORY ERROR: ", err)
    except ArgumentError as err:
        print(err)

    except OperationalError as err:
        print("")
        if "1045" in err.args[0]:
            print("\033[33mWARNING\033[0m: ", "DATABASE APPS: 1045 - Access Denied")
        elif "1698" in err.args[0]:
            print("\033[33mWARNING\033[0m: ", "DATABASE APPS: 1698 - Access Denied")
        elif "2003" in err.args[0]:
            print("\033[33mWARNING\033[0m: ", "DATABASE APPS: 2003 - Connection Refused")
        elif "Could not parse SQLAlchemy URL from string" in err.args[0]:
            print("\033[33mWARNING\033[0m: ", "DATABASE APPS: Could not parse SQLAlchemy URL from string - URL Enggine ERROR")
        else:
            raise
