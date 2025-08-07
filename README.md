# SGDK Character Creator v1.1.0

直感的なキャラクター作成ツールで、SGDK（SEGA Genesis Development Kit）用のスプライトを簡単に生成できます。

![SGDK Character Creator](https://raw.githubusercontent.com/KG-NINJA/SGDKDOT/main/assets/screenshot.png)

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
- **ファイルダウンロード** - 生成されたファイルを直接ダウンロード

## 使用方法

### Webアプリケーションの起動

```bash
# 依存関係のインストール
pip install flask pillow flask-cors

# アプリケーションの起動
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

1. キャラクター名を入力（英数字とアンダースコアのみ使用可能）
2. "Export to SGDK" ボタンをクリック
3. 以下のファイルが生成されます：
   - `character_name.c` - Cソースファイル
   - `character_name.h` - ヘッダーファイル
   - `character_name.png` - スプライトシート（参照用）
4. 各ファイルの「Download」リンクをクリックしてダウンロード可能

### キャラクターの保存と読み込み

- **Save Character** ボタンをクリックすると、現在のキャラクター設定をJSON形式で保存できます
- **Load Character** ボタンをクリックすると、保存したJSONファイルからキャラクター設定を読み込めます

### ランダムキャラクター生成

- **Random Character** ボタンをクリックすると、ランダムな設定のキャラクターが生成されます
- 肌の色は70%の確率で頭と腕で一致するようになっています

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
├── assets/                  # 画像などのアセット
├── web_app.py               # Webアプリケーション
├── main.py                  # エントリーポイント
└── example_usage.py         # プログラムからの使用例
```

## 技術仕様

- **対応フォーマット**: SGDK SpriteDefinition
- **カラーパレット**: Mega Drive 16色パレット
- **スプライト形式**: 4bpp（4 bits per pixel）
- **タイル単位**: 8x8ピクセル
- **アニメーション**: 正弦波ベースの歩行アニメーション

## 依存関係

```bash
pip install flask pillow flask-cors
```

## プログラムからの使用

`example_usage.py` を参照してください。基本的な使用方法：

```python
from app.core.generator import CharacterGenerator
from app.core.exporter import SGDKExporter

# キャラクター生成
generator = CharacterGenerator()
exporter = SGDKExporter()

# キャラクター設定
character_data = {
    "head_type": "round",
    "body_type": "normal",
    "arm_type": "normal",
    "leg_type": "normal",
    "head_color": "#FFDDAA",
    "body_color": "#0066CC",
    "arm_color": "#FFDDAA",
    "leg_color": "#0066CC",
    "size": 32,
    "animation_frames": 4
}

# プレビュー生成
sprite = generator.generate_character(character_data, frame=0)
sprite.save("preview.png")

# SGDK形式でエクスポート
exporter.export_character(character_data, "output/character.c")
```

## 更新履歴

### v1.1.0
- ファイルダウンロード機能の追加
- エラー処理の改善
- ランダム生成アルゴリズムの改善
- UIの改善（ヘッダー、フッター、スタイル）
- CORS対応

### v1.0.0
- 初回リリース

## ライセンス

このプロジェクトはオープンソースです。SGDK開発者コミュニティでの使用を想定しています。
