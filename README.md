# SGDK Character Creator

直感的なキャラクター作成ツールで、SGDK（SEGA Genesis Development Kit）用のスプライトを簡単に生成できます。

## 特徴

- **直感的なWebインターフェース** - ブラウザで簡単にキャラクターを作成
- **リアルタイムプレビュー** - 変更をすぐに確認
- **豊富なカスタマイズオプション**
  - 頭の形状（丸、四角、楕円、三角）
  - 体型（通常、筋肉質、スリム、丸）
  - 腕の種類（通常、筋肉質、細い、長い）
  - 脚の種類（通常、筋肉質、細い、長い）
  - 各部位の色設定
  - スプライトサイズ（16-64px）
  - アニメーションフレーム数（1-8フレーム）
- **アニメーション機能** - 歩行アニメーションのプレビュー
- **SGDK形式出力** - 完全なSGDK互換ファイルを生成
- **キャラクター保存/読み込み** - JSON形式でキャラクターデータを管理
- **ランダム生成** - ワンクリックでランダムキャラクターを作成

## 使用方法

### Webアプリケーションの起動

```bash
cd SGDKDOT
python web_app.py
```

ブラウザで `http://localhost:12000` にアクセスしてください。

### キャラクター作成

1. **Body Parts** セクションで体の各部位の形状を選択
2. **Colors** セクションで各部位の色を設定
3. **Size & Animation** セクションでスプライトサイズとアニメーションフレーム数を調整
4. リアルタイムプレビューで結果を確認
5. アニメーションチェックボックスで歩行アニメーションを再生

### SGDK形式でのエクスポート

1. キャラクター名を入力
2. "Export to SGDK" ボタンをクリック
3. 以下のファイルが生成されます：
   - `character_name.c` - Cソースファイル
   - `character_name.h` - ヘッダーファイル
   - `character_name.png` - スプライトシート（参照用）

### 生成されるファイルの使用方法

SGDKプロジェクトで生成されたファイルを使用する例：

```c
#include "my_character.h"

// スプライトの初期化
Sprite* playerSprite = SPR_addSprite(&my_character_frame0, 
                                    x, y, TILE_ATTR(PAL0, 0, 0, 0));

// アニメーション再生
int currentFrame = 0;
SPR_setDefinition(playerSprite, my_character_animation[currentFrame]);
```

## ファイル構造

```
SGDKDOT/
├── app/
│   ├── core/
│   │   ├── generator.py      # キャラクター生成エンジン
│   │   └── exporter.py       # SGDK形式エクスポート
│   ├── utils/
│   │   └── style.py          # Mega Drive風テーマ
│   └── windows/
│       └── main_window.py    # Tkinter版（非推奨）
├── templates/
│   └── index.html           # Webインターフェース
├── static/
│   └── output/              # 生成ファイル出力先
├── web_app.py               # Webアプリケーション
└── main.py                  # エントリーポイント
```

## 技術仕様

- **対応フォーマット**: SGDK SpriteDefinition
- **カラーパレット**: Mega Drive 16色パレット
- **スプライト形式**: 4bpp（4 bits per pixel）
- **タイル単位**: 8x8ピクセル
- **アニメーション**: 正弦波ベースの歩行アニメーション

## 依存関係

```bash
pip install flask pillow
```

## ライセンス

このプロジェクトはオープンソースです。SGDK開発者コミュニティでの使用を想定しています。
