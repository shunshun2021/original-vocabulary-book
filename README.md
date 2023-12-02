# ChatGPT APIを活用した「丸暗記脱却！英単語帳アプリ」

## 概要
英単語を覚える際に、ChatGPT APIを使い
- 覚えたい単語を含んだ例文
- 語の由来

を自動で生成し、英単語と共に単語帳に保存します。
これにより丸暗記ではなく、語の使い方や成り立ちを理解しながら勉強できる自分専用の英単語帳を作ることができます！


## 開発背景
大学院入試の際にTOEFLのスコア提出が要求され、TOEFL用の英単語の勉強をしました。その際
- 市販の単語帳
  - 覚えている単語も載っているため学習効率がやや悪い
  - 文章題に出てきた単語を加えるなどのカスタムができない
- 既存のオリジナル単語帳アプリ
  - 単語とその日本語訳を保持する機能しかないため、丸暗記するほかなく、覚えにくい

と感じました。

これらを解消する方法として「例文や語源による説明を自動で生成してくれる自分専用の単語帳アプリ」の開発を始めました。


## 動作の様子
### 登録画面
<img width="75%" alt="registration_screen" src="https://github.com/shunshun2021/original-vocabulary-book/assets/79389416/8617eac1-1b43-4511-9ba1-7e4f2929b800">
<!-- <img src="![registration_screen](https://github.com/shunshun2021/original-vocabulary-book/assets/79389416/8617eac1-1b43-4511-9ba1-7e4f2929b800)" width="50%"\> -->

### 単語リスト画面
<p>
  <img width="70%" alt="exacerbate" src="https://github.com/shunshun2021/original-vocabulary-book/assets/79389416/d34a5c5e-d403-4ba1-9525-ffb187e37652">
  <img width="70%" alt="disclose" src="https://github.com/shunshun2021/original-vocabulary-book/assets/79389416/2e5d38ba-168b-4a4e-b252-043e23800f81">
</p>
<!-- ![exacerbate](https://github.com/shunshun2021/original-vocabulary-book/assets/79389416/d34a5c5e-d403-4ba1-9525-ffb187e37652)-->
<!-- ![disclose](https://github.com/shunshun2021/original-vocabulary-book/assets/79389416/2e5d38ba-168b-4a4e-b252-043e23800f81)-->

## 主な使用技術
- Streamlit
- FastAPI
- ChatGPT API

------------------------
## ToDo
以下のような機能の追加を考えています.
- 1ページあたりの表示単語数のカスタム機能
- 単語テスト機能
- 単語リストの表示の工夫 (e.g. エビングハウスの忘却曲線に基づく定着率の低いもの順)
