from pydantic import BaseModel, Field
import datetime

# メモ参照定義
class MemoSchema (BaseModel):
    #memo_id: int = Field()
    #content: str = Field(max_length=100)

    word : str = Field(max_length=30)
    japanese : str = Field(max_length=30)
    sample_sentence : str = Field(max_length=100)
    sample_sentence_in_japanese : str = Field(max_length=100)
    origin : str = Field(max_length=300)

    number_of_correct_answer : int = Field()
    date_of_correct_answer : datetime.datetime = Field()
    retention_rate : float = Field()

    class Config:
        orm_mode = True


# メモ登録定義
class MemoCreatingSchema (BaseModel):
    #content: str = Field(max_length=100)
    word : str = Field(max_length=30)
    japanese : str = Field(max_length=30)
    sample_sentence : str = Field(max_length=100)
    sample_sentence_in_japanese : str = Field(max_length=100)
    origin : str = Field(max_length=300)

    number_of_correct_answer : int = Field(0)
    date_of_correct_answer : datetime.datetime = Field(datetime.datetime.now())
    retention_rate : float = Field(0.0)
    
    class Config:
        orm_mode = True