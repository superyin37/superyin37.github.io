# 建築設計企画支援AIシステム  
### Architecture Design Planning AI Assistant

殷 晗陽  
Role: Product Design / System Architecture / Core Developer  

Keywords: LLM · RAG · OCR · PPT Generation · AWS · Docker

---

# 1. 企画概要

## Background

建築設計の企画初期段階では、設計者は多くの情報を参照する必要がある。  
例えば、建築事例、建築規範、設計ガイドラインなどである。しかしこれらの情報は多くの場合、PDF文書、CAD図面、個別資料などに分散しており、必要な情報を迅速に取得することは容易ではない。さらに、企画段階では設計コンセプトの整理やプレゼンテーション資料（PPT）の作成にも多くの時間が必要となる。

近年、大規模言語モデル（LLM）および Retrieval-Augmented Generation（RAG）の発展により、専門知識を統合したインテリジェントな設計支援システムを構築することが可能になった。本プロジェクトでは、LLM・RAG・OCR技術を統合し、建築企画段階における情報探索・設計支援・成果物生成を一体化する **建築設計企画支援AIシステム** を開発した。

---

## Objective

本システムの目的は、建築設計の企画段階において以下の支援を提供することである。

- 建築知識および建築規範に関する **専門QA（RAG）**
- 対話型インターフェースによる **企画案生成**
- 建築企画資料（PPT）の **自動生成**
- CAD図面から建築規範を検索する **インテリジェント検索**

これにより、設計者は **情報検索・企画立案・成果物生成を一つのAIシステム内で実行可能** となる。

---

## System Overview

![System Overview](images/system_overview.png)

本システムは主に以下の3つのAI機能モジュールから構成される。

### 1. 建築知識RAG検索システム

建築事例データベースおよび建築規範データベースを対象とした  
RAGベースの専門QAシステムを構築した。

ユーザーの質問は、意図認識・知識検索・LLM生成を組み合わせたパイプラインを通して回答生成される。

本モジュールでは **RAG検索パイプライン設計、Vector DB構築、FastAPIバックエンド開発、フロントエンド実装、Dockerデプロイ** を担当した。

---

### 2. 建築企画案生成（PPT Generator）

ユーザーの設計要件を対話的に収集し、建築企画案を生成する機能である。

主な機能：

- 設計要件収集
- 建築事例マッチング
- コンセプト生成
- 建築企画PPT生成

本モジュールでは **企画生成ワークフロー設計およびPrompt設計に参加** した。

---

### 3. CAD建築規範検索システム

CAD図面のスクリーンショットから建築規範番号を抽出し、  
対応する規範PDFページを自動取得するシステムを開発した。

OCR解析と規範番号抽出アルゴリズムを組み合わせることで、  
従来手動で行われていた規範検索作業を自動化した。

本モジュールは **機能設計・OCR処理・API実装・クラウドデプロイまでを単独で担当** した。

---

## My Contributions

本プロジェクトでは、主にAIシステムの設計および実装を担当した。

### RAG建築規範検索システム（主担当）

- RAG検索パイプライン設計
- Vector Database構築
- FastAPIバックエンドAPI開発
- Webフロントエンド実装
- Dockerによるサービスデプロイ

---

### CAD建築規範解析システム（主担当）

- CAD OCR解析
- 建築規範番号抽出アルゴリズム設計
- 規範ページインデックス構築
- REST API開発
- AWS環境でのクラウドデプロイ

---

### PPT生成システム（共同設計）

- 企画生成フロー設計
- Promptテンプレート設計
- PPT生成ロジック設計

---

## Results & Technical Challenges

### Results

本プロジェクトにより以下を実現した。

- 建築知識を対象としたRAG検索システム
- CAD図面からの建築規範自動検索
- 建築企画案の自動生成
- DockerおよびAWS環境で運用可能なAIシステム

---

### Technical Challenges

**RAG検索精度**

建築規範文書には多くのノイズが含まれるため、  
多段検索および再ランキングを導入した。

**CAD OCR認識精度**

CAD図面の文字形式が不規則であるため、  
OCRとLLM補正を組み合わせて認識精度を向上させた。

**ユーザー入力の不完全性**

企画段階では要件が曖昧であるため、  
対話型の要件収集フローを設計した。

---

\newpage

# 2. System Architecture

![System Architecture](images/system_architecture.png)

本システムは **Frontend・API Gateway・AI Services・Data Layer** の4層アーキテクチャを採用している。

---

## User Input / Output

### User Input

ユーザーは以下の入力を行う。

- 建築設計に関する質問
- 建築企画要件
- CAD図面スクリーンショット

---

### System Output

システムは以下の出力を生成する。

- 建築知識QA回答
- 建築企画提案
- 建築企画PPT
- 建築規範PDFページ

---

## AI Processing Pipeline

![AI Pipeline](images/ai_pipeline.png)

ユーザーリクエストは以下のAI処理パイプラインを通して処理される。

- 意図分類（Intent Detection）
- RAG知識検索
- LLMによる回答生成

CAD規範検索では以下の処理が行われる。

- OCR文字認識
- 規範番号抽出
- 規範ページ検索
- PDF取得

---

## Key Components

### RAG Engine

建築知識検索を担当するモジュール。

- Embedding生成
- Vector検索
- Document rerank
- LLM回答生成

---

### CAD Regulation Analyzer

CAD図面から規範番号を抽出するモジュール。

- OCR解析
- 規範番号抽出
- 規範ページインデックス検索

---

### PPT Generator

建築企画案を生成するモジュール。

- Promptテンプレート
- LLMコンテンツ生成
- PPT構造生成

---

## Cloud Architecture

本システムはAWS環境上で運用されている。

- **AWS EC2**  
  FastAPIサーバーおよびAIサービス

- **AWS S3**  
  PDF文書およびファイル保存

- **PostgreSQL**  
  メタデータ管理

- **Vector Database**  
  RAG知識検索

- **Docker**  
  コンテナ化によるデプロイ

---

## Security & Operations

### Authentication

ユーザーアクセス制御を実装。

---

### Logging

APIリクエストおよびLLMレスポンスをログとして保存。

---

### Monitoring

クラウド環境におけるサービス監視およびログ分析を実施。

---