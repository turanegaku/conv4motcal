# conv4motocal
元カレ計算機を使うときに所持している装備を入力するのが面倒くさい人向け


## 詳細
- 編成で装備している武器を元カレで使える形式に変換する

### 問題
- 編成してない装備を変換できない
- 通常マグナ攻刃背水とバハ剣刃でしか動作を確認してない
- 今までの編成とか全部破壊して更新する


## 使い方
#### グラブルでやること
- Developer Tools (⌘ + ⌥ + i) とか
- Network タブ
- Filter
- party/deck
- XHR
- グラブルで編成を選ぶ
- Copy > Copy Responce

#### conv4motocalでやること
- 編成がコピーされるので保存する(deck.jsonとか)
- `python main.py deck.json`
- 出力結果をコピーする

#### 元カレでやること
- Developer Tools (⌘ + ⌥ + i) とか
- Console に貼り付け
- リロード
- 保存 > 読込
