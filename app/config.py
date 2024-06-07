class Config:
    from sqlalchemy import create_engine

    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:root@localhost:3306/BPTDB"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True) 