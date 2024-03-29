# Dockerfile
# ベースとなるDockerイメージ指定
FROM python:3.12.2-bullseye

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係のリストをコピー
COPY ./requirements.txt /app/requirements.txt

# 依存関係をインストール
RUN pip install --no-cache-dir -r /app/requirements.txt

# ソースコードをコピー
COPY ./app /app

# ポート番号を指定
ENV PORT 8080

# FastAPIを起動
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]