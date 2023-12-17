from sqlalchemy.orm import Session
import model, schema
import datetime

# メモ一覧取得
def get_memos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Memo).offset(skip).limit(limit).all()

# メモ登録
def create_memo(db: Session, memo: schema.MemoCreatingSchema):
    #db_memo = model.Memo(content = memo.content)
    db_memo = model.Memo(word = memo.word, japanese = memo.japanese,
                         sample_sentence = memo.sample_sentence,sample_sentence_in_japanese = memo.sample_sentence_in_japanese,
                         origin = memo.origin,number_of_correct_answer=0,date_of_correct_answer=datetime.datetime.now(),retention_rate=0.0)

    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo

# テストにおける正答時
def correct_answer(db: Session, word: str):
    #data = db.query(model.Memo).filter(model.Memo.word==word)
    #instance = db.query(model.Memo).filter(model.Memo.word==word).first()
    data = db.query(model.Memo).filter(model.Memo.word==word).first()
    if data:

        data.number_of_correct_answer=data.number_of_correct_answer+1
        data.date_of_correct_answer=datetime.datetime.now()
        data.retention_rate=100.0

    #data.update({
    #    model.Memo.number_of_correct_answer : instance.number_of_correct_answer+1,
    #    model.Memo.date_of_correct_answer:datetime.datetime.now(),
    #    model.Memo.retention_rate:100.0
    #})
    
    db.commit()

    return {"message":"success"}

