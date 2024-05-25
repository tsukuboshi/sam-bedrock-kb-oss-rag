# san-bedrock-kb-oss-rag

## 概要

RAGのサンプルシステムをKnowledge Bases for Amazon Bedrock、Amazon OpenSearch Serverless、Amazon S3を用いて、SAMで実装しています。  

## デプロイ手順

1. 以下コマンドでリポジトリをクローンし、ディレクトリを移動

```bash
git clone https://github.com/tsukuboshi/sam-bedrock-kb-oss-rag
cd sam-bedrock-kb-oss-rag
```

2. 以下コマンドで、SAMアプリをビルド

```bash
sam build
```

3. 以下コマンドで、SAMアプリをデプロイ

```bash
sam deploy 
  [--parameter-overrides]
  [EmbeddingModelId=<Bedrockの埋め込みモデルARN>]
  [OSSCollectionStandbyReplicas=<OSSのコレクションスタンバイレプリカ有効/無効>]
  [OSSDataAccessPrincipalArn=<IAMプリンシパルAEN>]
```

## パラメータ詳細

|パラメータ名|デフォルト値|指定可能な値|説明|
|---|---|---|---|
|EmbeddingModelId|cohere.embed-multilingual-v3|amazon.titan-embed-text-v1/cohere.embed-english-v3/cohere.embed-multilingual-v3/|Bedrockの埋め込みモデルのID|
|OSSCollectionStandbyReplicas|DISABLED|ENABLED/DISABLED|OSSのコレクションスタンバイレプリカの有効/無効|
|OSSDataAccessPrincipalArn|なし|ARN|OSSのデータアクセスプリンシパルのARN|

## 参考文献
