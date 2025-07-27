FROM python:3.13-alpine AS builder

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock* ./

RUN uv venv /venv && \
    . /venv/bin/activate && \
    uv pip install -r pyproject.toml

FROM python:3.13-alpine AS final

RUN apk add --no-cache bash git

COPY --from=builder /venv /venv

COPY . .

ENV PATH="/venv/bin:$PATH"

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]