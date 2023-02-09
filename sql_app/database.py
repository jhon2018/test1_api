from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import URL #CONEXION AL SERVIDOR MICROSOFT

# connection_string = "DRIVER={SQL Server Native Client 11.0};SERVER=JONATHAN;DATABASE=DAP_CR_TDP;UID=sa;PWD=47736559;trusted_connection=Yes"
# connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})#pip install pyodbc

SQLALCHEMY_DATABASE_URL = (
     "mssql+pyodbc://sa:47736559@JONATHAN/test"
     "?driver=ODBC+Driver+17+for+SQL+Server"

)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": False},  # only needed for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
