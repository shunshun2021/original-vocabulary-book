from sqlalchemy.orm import Session
import model, schema

# メモ一覧取得
def get_memos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Memo).offset(skip).limit(limit).all()

# メモ登録
def create_memo(db: Session, memo: schema.MemoCreatingSchema):
    #db_memo = model.Memo(content = memo.content)
    db_memo = model.Memo(word = memo.word, japanese = memo.japanese,
                         sample_sentence = memo.sample_sentence,sample_sentence_in_japanese = memo.sample_sentence_in_japanese,
                         origin = memo.origin)

    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo
