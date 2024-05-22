class Config:
    from sqlalchemy import create_engine

    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@localhost:3306/BPTDB"
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True) 