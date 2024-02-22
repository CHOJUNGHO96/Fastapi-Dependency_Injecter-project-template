# Python 3.11 베이스 이미지 사용
FROM python:3.11-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Poetry 설치
RUN pip install poetry

# 프로젝트 의존성 파일 복사
COPY poetry.lock pyproject.toml /app/

# Poetry를 통해 의존성 설치. 개발 의존성은 제외
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# 프로젝트 파일 복사
COPY . /app

# Chrome을 설치하기 위한 dependencies 추가
RUN apt-get update && apt-get install -y wget gnupg2 apt-utils && apt-get install -y wget && apt-get install -y curl && apt-get install -y unzip

## Chrome 저장소와 ChromeDriver 추가 및 설치
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update -y \
    && apt-get install google-chrome-stable -y \
    && wget -N https://chromedriver.storage.googleapis.com/88.0.4324.96/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && apt-get install xvfb -y

# Uvicorn을 사용하여 FastAPI 애플리케이션 실행
CMD ["gunicorn", "app.main:app", "-k", "uvicorn.workers.UvicornWorker", "--workers", "4", "--bind", "0.0.0.0:5050"]
