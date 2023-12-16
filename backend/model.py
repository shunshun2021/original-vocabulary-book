from sqlalchemy import Column, Integer, String, DateTime, Float
from database import Base
import datetime

class Memo(Base):
    __tablename__ = 'memos'

    #memo_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    #content = Column(String, index=True)

    word = Column(String, primary_key=True, index=True)
    japanese = Column(String,index=True)
    sample_sentence = Column(String,index=True)
    sample_sentence_in_japanese = Column(String,index=True)
    origin = Column(String,index=True)

    number_of_correct_answer = Column(Integer, index=True)
    date_of_correct_answer = Column(DateTime, index=True)
    retantion_rate = Column(Float,index=True)