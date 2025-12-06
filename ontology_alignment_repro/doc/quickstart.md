# クイックスタートガイド

## 5分で始めるオントロジーアライメント

このガイドでは、プロジェクトのセットアップから最初の実行までを簡潔に説明します。

## 前提条件

- Python 3.7以上
- pip パッケージマネージャー

## セットアップ

### 1. 依存関係のインストール

```bash
cd ontology_alignment_repro
pip install -r requirements.txt
```

**インストールされるもの**:
- pytest: テストフレームワーク

## 基本的な使い方

### オプション1: テストの実行

プロジェクトが正しく動作するか確認します。

```bash
# シンプルな実行
pytest -q

# 詳細な出力
pytest -v
```

**期待される出力**:
```
============================= test session starts ==============================
tests/test_pipeline.py::test_toy_perfect_oracle PASSED                   [ 50%]
tests/test_pipeline.py::test_toy_noisy_oracle PASSED                     [100%]

============================== 2 passed in 0.02s
```

### オプション2: パイプラインの実行

#### 完璧なオラクル（エラーなし）

```bash
python run_pipeline.py \
  --mode toy \
  --oracle simulated \
  --error-rate 0.0 \
  --out result_perfect.json
```

**出力**:
```json
{
  "precision": 1.0,
  "recall": 1.0,
  "f1": 1.0,
  "tp": 4,
  "fp": 0,
  "fn": 0
}
```

#### ノイズのあるオラクル

```bash
# 10%のエラー率
python run_pipeline.py --mode toy --oracle simulated --error-rate 0.1 --out result_10.json

# 20%のエラー率
python run_pipeline.py --mode toy --oracle simulated --error-rate 0.2 --out result_20.json

# 30%のエラー率
python run_pipeline.py --mode toy --oracle simulated --error-rate 0.3 --out result_30.json
```

## コマンドラインオプション

### run_pipeline.py のパラメータ

| パラメータ | 説明 | デフォルト | 選択肢 |
|-----------|------|-----------|--------|
| `--mode` | 実行モード | `toy` | `toy`, `from_logmap` |
| `--oracle` | オラクルタイプ | `simulated` | `simulated`, `openai`, `gemini` |
| `--error-rate` | エラー率（0.0〜1.0） | `0.0` | 任意の小数 |
| `--out` | 出力ファイル | `run_result.json` | 任意のパス |

### 使用例

```bash
# 完璧なオラクルでの実行
python run_pipeline.py --mode toy --oracle simulated --error-rate 0.0

# 高いエラー率での実行
python run_pipeline.py --mode toy --oracle simulated --error-rate 0.5 --out noisy.json
```

## 結果の読み方

### 出力JSON構造

```json
{
  "final_alignment": [
    ["O1:Cell", "O2:Cell"],
    ["O1:Tissue", "O2:Tissue"],
    ...
  ],
  "metrics": {
    "precision": 1.0,
    "recall": 1.0,
    "f1": 1.0,
    "tp": 4,
    "fp": 0,
    "fn": 0
  },
  "oracle_decisions": {
    "O1:AlveolusEpithelium|||O2:AlveolarEpithelium": true,
    "O1:LungEpithelium|||O2:Epithelium": true,
    "O1:MouseGeneX|||O2:HumanGeneY": false
  }
}
```

### メトリクスの意味

- **precision**: 提案されたマッピングのうち正しいものの割合
- **recall**: 正解マッピングのうち見つけられたものの割合
- **f1**: Precision と Recall の調和平均
- **tp** (True Positive): 正しく識別された正のマッピング数
- **fp** (False Positive): 誤って識別された正のマッピング数
- **fn** (False Negative): 見逃された正のマッピング数

### 良い結果とは？

| F1スコア | 評価 |
|---------|------|
| 0.9〜1.0 | 優秀 |
| 0.7〜0.9 | 良好 |
| 0.5〜0.7 | 普通 |
| < 0.5 | 改善が必要 |

## よくある質問

### Q1: ModuleNotFoundError が出る

**A**: `tests/conftest.py` が存在することを確認してください。存在しない場合は作成します：

```python
# tests/conftest.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

### Q2: pytestが見つからない

**A**: 依存関係を再インストールしてください：

```bash
pip install -r requirements.txt
```

### Q3: OpenAI/Gemini オラクルを使いたい

**A**: 現在はプレースホルダー実装です。`oracle_clients.py` を編集してAPIキーと実際のAPI呼び出しを実装してください：

```python
def openai_oracle(mask, reference, api_key):
    # OpenAI APIを呼び出す実装
    pass
```

### Q4: 実際のLogMapデータを使いたい

**A**:
1. LogMapを実行してアライメント結果を生成
2. JSON形式でエクスポート
3. `run_pipeline.py` の `from_logmap` モードを実装

詳細は `SPEC.md` を参照してください。

## 次のステップ

### 詳細を学ぶ

- [overview.md](overview.md) - プロジェクト全体の詳細
- [testing.md](testing.md) - テストの詳細とトラブルシューティング
- [SPEC.md](../SPEC.md) - 完全な仕様

### 実験を拡張する

1. **カスタムテストデータの作成**
   - `logmap_stub.py` を編集して独自のオントロジーペアを追加

2. **プロンプトテンプレートの評価**
   - `prompts.txt` の異なるテンプレートを試す

3. **実際のLLMとの統合**
   - OpenAI API または Gemini API を使った実装

4. **大規模データセットでの実験**
   - OAEI データセットをダウンロードして実行

## トラブルシューティング

### デバッグモード

```bash
# Python デバッグ出力を有効化
python -v run_pipeline.py --mode toy --oracle simulated --error-rate 0.0

# pytest の詳細出力
pytest -vv --tb=long
```

### ログの確認

出力JSONファイルを確認して詳細を把握：

```bash
# 整形して表示
python -m json.tool run_result_perfect.json

# オラクルの決定を確認
jq '.oracle_decisions' run_result_perfect.json
```

## サポート

問題が発生した場合：
1. [testing.md](testing.md) のトラブルシューティングセクションを確認
2. GitHub Issues で報告
3. ドキュメントを確認

## まとめ

```bash
# 最小限の実行手順
cd ontology_alignment_repro
pip install -r requirements.txt
pytest -q
python run_pipeline.py --mode toy --oracle simulated --error-rate 0.0
```

これで基本的な実行は完了です！
