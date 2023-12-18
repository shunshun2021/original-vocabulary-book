from typing import List
from fastapi import FastAPI, Depends, Request, status
from sqlalchemy.orm import Session
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

import model, schema, crud
from database import SessionLocal, engine

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# https://qiita.com/kurumaebi65/items/74e2edf8a394cf086c9a
@app.exception_handler(RequestValidationError)
async def handler(request:Request, exc:RequestValidationError):
    print(exc)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


# メモ参照
@app.get("/memos", response_model=List[schema.MemoSchema]) # パスオペレーションデコレータを定義
#@app.get("/memos")
async def read_memos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    memos = crud.get_memos(db, skip=skip, limit=limit)
    return memos

# メモ登録
@app.post("/memos", response_model=schema.MemoSchema)
#@app.post("/memos/{word}")
async def create_memo(memo: schema.MemoCreatingSchema, db: Session = Depends(get_db)):
    return crud.create_memo(db=db, memo=memo)


# 英単語テスト正解時
# https://fastapi.tiangolo.com/ja/tutorial/body/
@app.post("/correct/{word}")
async def correct(word: str ,db: Session = Depends(get_db)):
    print("word",word)
    return crud.correct_answer(db=db,word=word)