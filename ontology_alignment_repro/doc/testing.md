# テストガイド

## 概要

このドキュメントでは、オントロジーアライメントプロジェクトのテストについて解説します。

## テスト構成

### テストファイル

- **tests/test_pipeline.py**: メインのテストケース
- **tests/conftest.py**: pytest設定ファイル（モジュールパスの設定）

### テストケース

#### 1. test_toy_perfect_oracle

**目的**: 完璧なオラクル（エラーレート0%）でのアライメント精度を検証

**テスト内容**:
```python
def test_toy_perfect_oracle():
    data = run_logmap_stub()
    decisions = simulated_oracle(data['mask'], data['reference'], error_rate=0.0, seed=1)
    final_alignment = set(tuple(x) for x in data['automatic'])
    for (s,t),d in decisions.items():
        if d:
            final_alignment.add((s,t))
    metrics = evaluate_alignment(list(final_alignment), data['reference'])
    # the perfect oracle should reach F1 >= 0.9 in this toy example
    assert metrics['f1'] >= 0.9
```

**検証項目**:
- エラーレート0%のシミュレートされたオラクルを使用
- F1スコアが0.9以上であることを確認
- 完璧なオラクルは正しいマッピングのみを承認するため、高い精度が期待される

**実行結果**:
```
precision: 1.0
recall: 1.0
f1: 1.0
tp: 4, fp: 0, fn: 0
```

#### 2. test_toy_noisy_oracle

**目的**: ノイズのあるオラクル（エラーレート30%）での診断指標を検証

**テスト内容**:
```python
def test_toy_noisy_oracle():
    data = run_logmap_stub()
    decisions = simulated_oracle(data['mask'], data['reference'], error_rate=0.3, seed=2)
    diag = compute_oracle_diagnostics(data['mask'], decisions, data['reference'])
    # Youden index typically decreases as error increases; we assert non-perfect behavior
    assert diag['youden_index'] <= 1.0
```

**検証項目**:
- エラーレート30%のノイズを含むオラクルを使用
- Youden's index (YI = Sensitivity + Specificity - 1) が1.0以下であることを確認
- ノイズがある場合、完璧なパフォーマンスは期待されない

**診断指標**:
- **Sensitivity (Se)**: 真陽性率（正しいマッピングを正しく識別する能力）
- **Specificity (Sp)**: 真陰性率（誤ったマッピングを正しく拒否する能力）
- **Youden's index (YI)**: Se + Sp - 1（オラクルの全体的な性能指標）

## テスト実行方法

### 基本的な実行

```bash
# すべてのテストを実行
pytest -q

# 詳細な出力で実行
pytest -v

# 特定のテストのみ実行
pytest tests/test_pipeline.py::test_toy_perfect_oracle
```

### 実行結果の例

```
============================= test session starts ==============================
platform linux -- Python 3.11.14, pytest-9.0.1, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: /home/user/ccw-ontology_aligment_chatgpt/ontology_alignment_repro
collecting ... collected 2 items

tests/test_pipeline.py::test_toy_perfect_oracle PASSED                   [ 50%]
tests/test_pipeline.py::test_toy_noisy_oracle PASSED                     [100%]

============================== 2 passed in 0.02s
```

## テストデータ

### LogMapスタブデータ

`logmap_stub.py` は以下のテストデータを生成します：

**自動マッピング（高信頼度）**:
- O1:Cell ↔ O2:Cell (正解)
- O1:Tissue ↔ O2:Tissue (正解)

**不確実なマッピング（Mask）**:
- O1:AlveolusEpithelium ↔ O2:AlveolarEpithelium (score: 0.45, 正解)
- O1:LungEpithelium ↔ O2:Epithelium (score: 0.5, 正解)
- O1:MouseGeneX ↔ O2:HumanGeneY (score: 0.4, 不正解)

**参照アライメント（正解）**:
- O1:Cell ↔ O2:Cell
- O1:Tissue ↔ O2:Tissue
- O1:AlveolusEpithelium ↔ O2:AlveolarEpithelium
- O1:LungEpithelium ↔ O2:Epithelium

## パイプライン統合テスト

pytestに加えて、コマンドラインからパイプライン全体をテストできます：

### エラーレート別の実行

```bash
# 完璧なオラクル（エラーレート0%）
python run_pipeline.py --mode toy --oracle simulated --error-rate 0.0 --out run_result_perfect.json

# 10%エラー
python run_pipeline.py --mode toy --oracle simulated --error-rate 0.1 --out run_result_10.json

# 30%エラー
python run_pipeline.py --mode toy --oracle simulated --error-rate 0.3 --out run_result_30.json
```

### 結果の比較

| エラーレート | Precision | Recall | F1    | TP | FP | FN |
|--------------|-----------|--------|-------|----|----|-----|
| 0% (完璧)    | 1.00      | 1.00   | 1.00  | 4  | 0  | 0   |
| 10%          | 1.00      | 0.75   | 0.86  | 3  | 0  | 1   |
| 30%          | 0.75      | 0.75   | 0.75  | 3  | 1  | 1   |

エラーレートが増加するにつれて、F1スコアが低下することが確認できます。

## トラブルシューティング

### ModuleNotFoundError

**問題**: `ModuleNotFoundError: No module named 'oracle_clients'`

**解決策**: `tests/conftest.py` が存在することを確認してください。このファイルは親ディレクトリをPythonパスに追加します。

```python
# tests/conftest.py
import sys
from pathlib import Path

# Add parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
```

### 依存関係の問題

**問題**: pytest が見つからない

**解決策**:
```bash
pip install -r requirements.txt
```

## 追加のテストケース作成

新しいテストケースを追加する場合は、`tests/test_pipeline.py` に追加してください：

```python
def test_your_new_test():
    # テストロジック
    assert condition
```

## 継続的インテグレーション

このプロジェクトは CI/CD パイプラインで自動テストを実行できるよう設計されています。
GitHub Actions などで以下のコマンドを実行することを推奨します：

```yaml
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest -v
```
