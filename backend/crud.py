from sqlalchemy.orm import Session
import model, schema

# メモ一覧取得
def get_memos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.Memo).offset(skip).limit(limit).all()

# メモ登録
def create_memo(db: Session, memo: schema.MemoCreatingSchema):
    db_memo = model.Memo(content = memo.content)
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo
