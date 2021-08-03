from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
import uploadProceduresNBP

Base = declarative_base()


class Maintable(Base):
    __tablename__ = 'maintable'
    index = Column(Integer, primary_key=True)
    date_id = Column(Integer, ForeignKey('dates.date_id'))
    rate_id = Column(Integer, ForeignKey('rates.rate_id'))
    value = Column(Float)

    def __repr__(self):
        return "<authors(id='{0}', date={1}, value={2})>".format(
            self.id, self.date, self.value)


class Rate(Base):
    __tablename__ = 'rates'
    rate_id = Column(Integer, primary_key=True)
    bank_name = Column(String)
    rate = Column(String)

    def __repr__(self):
        return "<authors(id='{0}', date={1}, value={2})>".format(
            self.id, self.date, self.value)


class Date(Base):
    __tablename__ = 'dates'
    date_id = Column(Integer, primary_key=True)
    date = Column(Date)

    def __repr__(self):
        return "<authors(id='{0}', date={1}, value={2})>".format(
            self.id, self.date, self.value)


engine = uploadProceduresNBP.engine_create()
# Dolar.__table__.create(engine)
Base.metadata.create_all(engine)

# Usuwanie danej tabeli

