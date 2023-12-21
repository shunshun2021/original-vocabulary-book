from sqlalchemy.orm import Session
import model, schema
import datetime
from sqlalchemy import desc
import math


def forgetting_carve(number_of_correct_answer:int,date_of_correct_answer: datetime.datetime):
    # 参考：https://en.wikipedia.org/wiki/Forgetting_curve
    if(number_of_correct_answer==0):
        return 0.0

    # 忘却曲線の計算に必要な定数
    c,k = 1.25, 1.84
    EPS=5
    
    # 現在時刻の取得
    now=datetime.datetime.now()
    # 前回の正解時からの時間経過を算出
    time=now-date_of_correct_answer
    # 分単位に直す
    time=time.seconds/60
    # 定着率の計算
    if(time < EPS):
        # 5分以内に回答したものは100%定着とする.(log_10 の計算においてcomplex型を出現させないため)
        b=100
    else:
        b = 100*k/(pow(math.log10(time),c)+k)
    # 1回正解するごとに記憶の減衰率が半分になるようにする。
    forget = (100-b)/pow(2,number_of_correct_answer)
    b = 100-forget
    return b


# メモ一覧取得
def get_memos(db: Session, skip: int = 0, limit: int = 100):
    # 定着率(tetention_rate)の更新
    data = db.query(model.Memo).all()
    for sample in data:
        sample.retention_rate = forgetting_carve(sample.number_of_correct_answer,sample.date_of_correct_answer)
    db.commit()

    # retentn_rate, date_of_correct_answer の昇順でソート
    return db.query(model.Memo).order_by(model.Memo.retention_rate).order_by(model.Memo.date_of_correct_answer).offset(skip).limit(limit).all()


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

