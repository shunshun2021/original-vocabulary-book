from pydantic import BaseModel, Field

# メモ参照定義
class MemoSchema (BaseModel):
    memo_id: int = Field()
    content: str = Field(max_length=100)

    class Config:
        orm_mode = True

# メモ登録定義
class MemoCreatingSchema (BaseModel):
    content: str = Field(max_length=100)
    
    class Config:
        orm_mode = True