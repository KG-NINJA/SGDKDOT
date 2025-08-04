#!/usr/bin/env python3
"""
SGDK Character Creator - 使用例

このスクリプトは、プログラムからキャラクターを生成し、
SGDK形式でエクスポートする方法を示します。
"""

from app.core.generator import CharacterGenerator
from app.core.exporter import SGDKExporter
import os

def create_sample_characters():
    """サンプルキャラクターを作成してエクスポートします。"""
    
    generator = CharacterGenerator()
    exporter = SGDKExporter()
    
    # 出力ディレクトリを作成
    output_dir = "sample_characters"
    os.makedirs(output_dir, exist_ok=True)
    
    # サンプルキャラクター1: ヒーロー
    hero_data = {
        "head_type": "round",
        "body_type": "muscular",
        "arm_type": "muscular",
        "leg_type": "normal",
        "head_color": "#FFDDAA",
        "body_color": "#0066CC",
        "arm_color": "#FFDDAA",
        "leg_color": "#0066CC",
        "size": 32,
        "animation_frames": 4
    }
    
    print("Creating hero character...")
    exporter.export_character(hero_data, os.path.join(output_dir, "hero.c"))
    
    # サンプルキャラクター2: 敵キャラクター
    enemy_data = {
        "head_type": "triangle",
        "body_type": "slim",
        "arm_type": "long",
        "leg_type": "thin",
        "head_color": "#FF6666",
        "body_color": "#660000",
        "arm_color": "#FF6666",
        "leg_color": "#660000",
        "size": 24,
        "animation_frames": 3
    }
    
    print("Creating enemy character...")
    exporter.export_character(enemy_data, os.path.join(output_dir, "enemy.c"))
    
    # サンプルキャラクター3: NPCキャラクター
    npc_data = {
        "head_type": "oval",
        "body_type": "round",
        "arm_type": "normal",
        "leg_type": "normal",
        "head_color": "#DDAA88",
        "body_color": "#66FF66",
        "arm_color": "#DDAA88",
        "leg_color": "#66FF66",
        "size": 28,
        "animation_frames": 2
    }
    
    print("Creating NPC character...")
    exporter.export_character(npc_data, os.path.join(output_dir, "npc.c"))
    
    print(f"\nSample characters created in '{output_dir}' directory!")
    print("Generated files:")
    for filename in os.listdir(output_dir):
        print(f"  - {filename}")

def preview_character():
    """キャラクターのプレビューを生成します。"""
    
    generator = CharacterGenerator()
    
    # テストキャラクター
    test_data = {
        "head_type": "square",
        "body_type": "normal",
        "arm_type": "normal",
        "leg_type": "normal",
        "head_color": "#FFDDAA",
        "body_color": "#0066CC",
        "arm_color": "#FFDDAA",
        "leg_color": "#0066CC",
        "size": 64,
        "animation_frames": 1
    }
    
    print("Generating character preview...")
    sprite = generator.generate_character(test_data, 0)
    
    # プレビューを保存
    sprite.save("character_preview.png")
    print("Preview saved as 'character_preview.png'")

if __name__ == "__main__":
    print("SGDK Character Creator - Usage Example")
    print("=" * 40)
    
    # サンプルキャラクターを作成
    create_sample_characters()
    
    print()
    
    # プレビューを生成
    preview_character()
    
    print("\nDone! You can now use these files in your SGDK project.")