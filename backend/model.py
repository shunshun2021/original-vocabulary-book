from sqlalchemy import Column, Integer, String
from database import Base

class Memo(Base):
    __tablename__ = 'memos'

    #memo_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    #content = Column(String, index=True)

    word = Column(String, primary_key=True, index=True)
    japanese = Column(String,index=True)
    sample_sentence = Column(String,index=True)
    sample_sentence_in_japanese = Column(String,index=True)
    origin = Column(String,index=True)