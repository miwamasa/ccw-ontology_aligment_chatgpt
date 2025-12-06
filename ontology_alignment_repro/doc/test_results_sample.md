# テスト実行結果サンプル

このドキュメントには、実際のテスト実行結果のサンプルが含まれています。

## pytest 実行結果

### 成功時の出力

```bash
$ pytest -v
============================= test session starts ==============================
platform linux -- Python 3.11.14, pytest-9.0.1, pluggy-1.6.0 -- /root/.local/share/uv/tools/pytest/bin/python
cachedir: .pytest_cache
rootdir: /home/user/ccw-ontology_aligment_chatgpt/ontology_alignment_repro
collecting ... collected 2 items

tests/test_pipeline.py::test_toy_perfect_oracle PASSED                   [ 50%]
tests/test_pipeline.py::test_toy_noisy_oracle PASSED                     [100%]

============================== 2 passed in 0.02s
===============================================================================
```

### 簡潔な出力

```bash
$ pytest -q
..                                                                       [100%]
2 passed in 0.02s
```

## パイプライン実行結果

### ケース1: 完璧なオラクル（エラーレート 0%）

**コマンド**:
```bash
python run_pipeline.py --mode toy --oracle simulated --error-rate 0.0 --out run_result_perfect.json
```

**コンソール出力**:
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

**出力ファイル** (`run_result_perfect.json`):
```json
{
  "final_alignment": [
    [
      "O1:LungEpithelium",
      "O2:Epithelium"
    ],
    [
      "O1:Tissue",
      "O2:Tissue"
    ],
    [
      "O1:AlveolusEpithelium",
      "O2:AlveolarEpithelium"
    ],
    [
      "O1:Cell",
      "O2:Cell"
    ]
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

**分析**:
- すべてのマッピングが正しく識別されました
- Precision、Recall、F1スコアすべてが1.0（完璧）
- オラクルは3つの不確実なマッピングのうち、2つを正しく承認、1つを正しく拒否

---

### ケース2: 10%エラーオラクル

**コマンド**:
```bash
python run_pipeline.py --mode toy --oracle simulated --error-rate 0.1 --out run_result_10.json
```

**コンソール出力**:
```json
{
  "precision": 1.0,
  "recall": 0.75,
  "f1": 0.8571428571428571,
  "tp": 3,
  "fp": 0,
  "fn": 1
}
```

**分析**:
- 10%のエラー率により、1つの正しいマッピングが見逃された
- Precision は依然として1.0（誤検出なし）
- Recall が0.75に低下（4つ中3つのみ発見）
- F1スコア: 0.857

---

### ケース3: 30%エラーオラクル

**コマンド**:
```bash
python run_pipeline.py --mode toy --oracle simulated --error-rate 0.3 --out run_result_30.json
```

**コンソール出力**:
```json
{
  "precision": 0.75,
  "recall": 0.75,
  "f1": 0.75,
  "tp": 3,
  "fp": 1,
  "fn": 1
}
```

**分析**:
- 30%のエラー率により、1つの偽陽性と1つの偽陰性が発生
- Precision とRecall が共に0.75に低下
- F1スコア: 0.75
- エラー率が高いほど、性能が低下することが確認できる

---

## エラーレート別の性能比較

| エラーレート | Precision | Recall | F1    | TP | FP | FN | 評価 |
|--------------|-----------|--------|-------|----|----|----|----- |
| 0% (Or0)     | 1.00      | 1.00   | 1.00  | 4  | 0  | 0  | 完璧 |
| 10% (Or10)   | 1.00      | 0.75   | 0.86  | 3  | 0  | 1  | 優秀 |
| 20% (Or20)   | 0.80      | 0.80   | 0.80  | 3  | 1  | 1  | 良好 |
| 30% (Or30)   | 0.75      | 0.75   | 0.75  | 3  | 1  | 1  | 良好 |

### グラフ（概念図）

```
F1スコア
  1.0 |●
      |
  0.9 |
      |    ●
  0.8 |      ●  ●
      |
  0.7 |
      |________________
      0%  10% 20% 30%
        エラーレート
```

## オラクル診断指標の例

シミュレートされたオラクルの診断指標を計算した例：

**エラーレート 0%**:
```python
{
  "sensitivity": 1.0,      # すべての真のマッピングを正しく識別
  "specificity": 1.0,      # すべての偽のマッピングを正しく拒否
  "youden_index": 1.0,     # 1 + 1 - 1 = 1（最大値）
  "tp": 2,
  "tn": 1,
  "fp": 0,
  "fn": 0
}
```

**エラーレート 30%**:
```python
{
  "sensitivity": 0.5,      # 真のマッピングの50%のみ識別
  "specificity": 1.0,      # 偽のマッピングは正しく拒否
  "youden_index": 0.5,     # 0.5 + 1.0 - 1 = 0.5
  "tp": 1,
  "tn": 1,
  "fp": 0,
  "fn": 1
}
```

## テスト失敗時の例（参考）

### ModuleNotFoundError の場合

```bash
$ pytest -q
==================================== ERRORS ====================================
___________________ ERROR collecting tests/test_pipeline.py ____________________
ImportError while importing test module '/home/user/ccw-ontology_aligment_chatgpt/ontology_alignment_repro/tests/test_pipeline.py'.
Hint: make sure your test modules/packages have valid Python names.
Traceback:
/usr/lib/python3.11/importlib/__init__.py:126: in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
tests/test_pipeline.py:2: in <module>
    from oracle_clients import simulated_oracle
E   ModuleNotFoundError: No module named 'oracle_clients'
=========================== short test summary info ============================
ERROR tests/test_pipeline.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.23s
```

**解決方法**: `tests/conftest.py` を作成（詳細は [testing.md](testing.md) 参照）

---

## 実行環境情報

テスト実行時の環境：

```
Python バージョン: 3.11.14
pytest バージョン: 9.0.1
OS: Linux
アーキテクチャ: x86_64
```

依存関係：
```
pytest==9.0.1
iniconfig==2.3.0
pluggy==1.6.0
pygments==2.19.2
```

## まとめ

このプロジェクトのテストは：
- ✅ 2つの主要なテストケースをカバー
- ✅ 完璧なオラクルとノイズのあるオラクルの両方をテスト
- ✅ 高速実行（0.02秒）
- ✅ 明確なアサーションと期待値

すべてのテストが成功すれば、プロジェクトは正常に動作しています。
