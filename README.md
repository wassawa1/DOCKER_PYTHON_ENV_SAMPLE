# このリポジトリについて (Docker の使い方)

このプロジェクトはDocker + pip だけでpython動作確認を行うサンプルです。
ここでは Docker を使ったビルド・実行・デバッグ方法にフォーカスします。

前提
- Docker がインストールされていること

重要なファイル
- `Dockerfile` - アプリケーションのイメージ定義（pip による依存インストール）
- `requirements.txt` - pip がインストールする Python 依存
- `main.py` - サンプルアプリケーション（起動確認用）
- `.dockerignore` - ビルドコンテキストから除外するファイル

クイックスタート

1) ビルド

```bash
cd /path/to/docker-python-condaenv
docker build -t my-python-app .
```

2) 実行（標準実行）

```bash
docker run --rm my-python-app
```

3) 対話的に入る（デバッグ／インスペクト用）

```bash
docker run --rm -it --entrypoint /bin/bash my-python-app
```

依存関係の編集
- `requirements.txt` を編集したら再ビルドしてください。

```bash
# 依存変更後
docker build -t my-python-app .
```

ローカル開発: ソースをマウントして実行
- イメージの再ビルドを避けて素早く確認したい場合（開発モード）:

```bash
docker run --rm -v "$(pwd):/app" -w /app python:3.13-slim python main.py
```

（注意）この方法ではイメージの requirements が反映されないため、手動で `pip install -r requirements.txt` するか、開発専用のコンテナを作ると良いです。

ログ・デバッグ
- コンテナのログ確認:

```bash
docker logs <container-id-or-name>
```
- 実行中コンテナに入る:

```bash
docker exec -it <container-id-or-name> /bin/bash
```

イメージサイズ最適化のヒント
- ベースイメージに `python:X.Y-slim` を使う
- 不要な build-time ツールは multi-stage build で分離する
- キャッシュを減らすため `--no-cache-dir` を pip install に付ける
- 可能なら OS レベルの不要なパッケージは削る

セキュリティと実行ユーザー
- 現在の Dockerfile は root ユーザーでパッケージをインストールしています。セキュリティとファイル権限管理のため、以下を行うことを検討してください:
	- Dockerfile 内で非 root ユーザーを作成し、そのユーザーでアプリを実行する
	- 必要に応じてファイル/ディレクトリの所有権を chown する

例（Dockerfile での非 root ユーザー作成の要点）

```dockerfile
RUN useradd --create-home appuser
WORKDIR /app
COPY --chown=appuser:appuser . /app
USER appuser
```

pyinstaller やビルド専用依存について
- `pyinstaller` のようなビルド専用ツールは、アプリの実行ステージに含めたくない場合が多いです。multi-stage build を使うと、ビルド時にだけ必要な依存を含むステージで実行し、最終ステージにはランタイムのみをコピーできます。

トラブルシューティング（よくある問題）
- numpy/pandas などのパッケージでネイティブ依存が必要な場合: `build-essential`, `libatlas-base-dev` や `libpq-dev` などの OS パッケージが必要になることがあります。エラーが出たら Dockerfile に apt-get で追加してください。
- ビルドが失敗する場合は、まずはエラーログを確認し、足りないライブラリ名で検索してください。

追加の作業候補（要望に応じて実施します）
- Dockerfile を非 root 実行に変更（実装済みのサンプルを追加）
- pyinstaller を用いた multi-stage ビルド例を追加
- GitHub Actions など CI 用のワークフローを追加して、自動ビルド/テストを行う

必要なら、上記のうちどれを優先して追加するか教えてください。

