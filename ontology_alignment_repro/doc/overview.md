# オントロジーアライメントプロジェクト概要

## プロジェクトについて

このプロジェクトは、論文「Large Language Models as Oracles for Ontology Alignment（オントロジーアライメントのためのオラクルとしての大規模言語モデル）」の実験を再現するための実装です。

## 背景

### オントロジーアライメントとは

オントロジーアライメントは、異なる知識体系（オントロジー）間で対応する概念を見つけ出すタスクです。例えば：
- 医学オントロジーの「Cell（細胞）」と生物学オントロジーの「Cell」を対応付ける
- マウスの解剖学オントロジーとヒトの解剖学オントロジー間の概念マッピング

### 課題

自動マッチャー（LogMapなど）は高精度なマッピングを生成できますが、不確実なマッピング（Mask）については判断が困難です。

### 本プロジェクトのアプローチ

不確実なマッピングの判断を大規模言語モデル（LLM）に委ねる「オラクル」アプローチを実装・評価します。

## アーキテクチャ

### パイプライン全体の流れ

```
1. 自動マッチャー (LogMap)
   ↓
2. 候補アライメント (MS) と不確実マッピング (Mask) の生成
   ↓
3. Maskに対するプロンプト生成
   ↓
4. オラクル (LLM) による判定 (True/False)
   ↓
5. 判定結果の統合
   ↓
6. 最終アライメントの生成
   ↓
7. 評価（Precision, Recall, F1）
```

### コンポーネント

#### 1. LogMapスタブ (`logmap_stub.py`)

実際のLogMapの代わりに、テスト用のデータを生成します。

**出力**:
- **automatic**: 高信頼度のマッピング（自動的に受理）
- **mask**: 不確実なマッピング（オラクルに問い合わせ）
- **reference**: 正解データ（評価用）

```python
{
  "automatic": [["O1:Cell", "O2:Cell"], ...],
  "mask": [["O1:AlveolusEpithelium", "O2:AlveolarEpithelium", 0.45], ...],
  "reference": [["O1:Cell", "O2:Cell"], ...]
}
```

#### 2. オラクルクライアント (`oracle_clients.py`)

マッピングの真偽を判定するオラクルの実装。

**モード**:
- **simulated**: 参照アライメントを使用した完璧または部分的にノイズのあるオラクル
- **openai**: OpenAI API を使用（実装は placeholder）
- **gemini**: Google Gemini API を使用（実装は placeholder）

**シミュレートされたオラクル**:
```python
def simulated_oracle(mask, reference, error_rate=0.0, seed=42):
    """
    error_rate: 正しい答えを反転させる確率（ノイズ）
    返り値: { (source, target) : bool } の辞書
    """
```

エラーレートの意味：
- `error_rate=0.0`: 完璧なオラクル（Or0）
- `error_rate=0.1`: 10%のエラーを含む（Or10）
- `error_rate=0.2`: 20%のエラーを含む（Or20）
- `error_rate=0.3`: 30%のエラーを含む（Or30）

#### 3. 評価モジュール (`eval.py`)

アライメント結果とオラクルの性能を評価します。

**アライメント評価指標**:
- **Precision（精度）**: TP / (TP + FP) - 提案したマッピングのうち正しいものの割合
- **Recall（再現率）**: TP / (TP + FN) - 正しいマッピングのうち見つけたものの割合
- **F1スコア**: 2 * Precision * Recall / (Precision + Recall) - 調和平均

**オラクル診断指標**:
- **Sensitivity (Se)**: TP / (TP + FN) - 真のマッピングを正しく識別する能力
- **Specificity (Sp)**: TN / (TN + FP) - 偽のマッピングを正しく拒否する能力
- **Youden's index (YI)**: Se + Sp - 1 - オラクルの全体的性能（-1～1の範囲）

#### 4. パイプライン実行 (`run_pipeline.py`)

全体のワークフローを統合・実行します。

**使用方法**:
```bash
python run_pipeline.py \
  --mode toy \
  --oracle simulated \
  --error-rate 0.0 \
  --out run_result_perfect.json
```

**パラメータ**:
- `--mode`: `toy`（テストモード）または `from_logmap`（実際のLogMap出力を使用）
- `--oracle`: `simulated`, `openai`, `gemini`
- `--error-rate`: シミュレートされたオラクルのエラー率（0.0～1.0）
- `--out`: 結果を保存するJSONファイル

## データセット

### Toyデータセット

プロジェクトに含まれる小規模なテストデータ。オフライン検証用。

**特徴**:
- 2つの簡単なオントロジー（O1, O2）
- 合計4つの正しいマッピング
- 3つの不確実な候補（うち2つが正解）

### 実際のデータセット（論文で使用）

大規模な実験には以下のOAEI（Ontology Alignment Evaluation Initiative）データセットを使用：

- **Anatomy**: マウス-ヒト解剖学
- **Bio-ML**: NCIT-DOID, OMIM-ORDO, SNOMEDバリアント
- **LargeBio**: FMA, NCI, SNOMEDの組み合わせ

これらは別途ダウンロードが必要です（[OAEI公式サイト](http://oaei.ontologymatching.org/)）。

## プロンプトテンプレート

`prompts.txt` に6つの標準的なプロンプトテンプレートが定義されています：

1. **P**: 基本プロンプト（ラベルのみ）
2. **PEC**: 拡張コンテキスト付き（親概念、祖父母概念）
3. **PNLF**: 自然言語フィードバック
4. **PNLF_EC**: 自然言語フィードバック + 拡張コンテキスト
5. **PNLF_S**: 自然言語フィードバック + シノニム
6. **PNLF_EC+S**: すべての情報を含む

**プレースホルダー**:
- `label(e)`: エンティティのラベル
- `synonyms(e)`: 同義語
- `parent(e)`: 直接の親概念
- `parent^2(e)`: 祖父母概念（2階層上）

## 実行例

### 完璧なオラクルでの実行

```bash
python run_pipeline.py --mode toy --oracle simulated --error-rate 0.0 --out result_perfect.json
```

**結果**:
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

### ノイズのあるオラクル（30%エラー）

```bash
python run_pipeline.py --mode toy --oracle simulated --error-rate 0.3 --out result_noisy.json
```

**結果**:
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

## ファイル構成

```
ontology_alignment_repro/
├── README.md                 # プロジェクト概要
├── SPEC.md                   # 詳細仕様
├── RUN_INSTRUCTIONS.md       # 実行手順
├── requirements.txt          # Python依存関係
├── prompts.txt              # プロンプトテンプレート
├── run_pipeline.py          # メインパイプライン
├── logmap_stub.py           # LogMapシミュレーター
├── oracle_clients.py        # オラクル実装
├── eval.py                  # 評価関数
├── tests/
│   ├── conftest.py         # pytest設定
│   └── test_pipeline.py    # テストケース
├── testcases/
│   └── reference.json      # 参照データ
└── doc/
    ├── overview.md         # 本ドキュメント
    ├── testing.md          # テストガイド
    └── quickstart.md       # クイックスタート
```

## 論文との対応

このプロジェクトは以下の論文実験を再現します：

- **Table 2-3**: 各データセットでのF1スコア比較
- **Figure 3-6**: エラーレート別の性能グラフ
- **Oracle diagnostics**: Sensitivity, Specificity, Youden's index の計算

## 今後の拡張

### 実際のLLMとの統合

`oracle_clients.py` の `openai` および `gemini` 関数を実装：

```python
def openai_oracle(mask, prompt_template, api_key):
    # OpenAI API呼び出し
    # "True" または "False" の厳密な出力を解析
    pass
```

### LogMap統合

実際のLogMap出力を読み込む：

```bash
python run_pipeline.py --mode from_logmap --logmap-file output.json
```

### 追加のプロンプトテンプレート

カスタムプロンプトテンプレートの追加と評価。

## 参考資料

- [OAEI (Ontology Alignment Evaluation Initiative)](http://oaei.ontologymatching.org/)
- [LogMap公式サイト](https://www.cs.ox.ac.uk/isg/tools/LogMap/)
- 論文: "Large Language Models as Oracles for Ontology Alignment"

## ライセンス

詳細は `LICENSE` ファイルを参照してください。
