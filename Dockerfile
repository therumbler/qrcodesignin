FROM python:3.13.2-alpine AS builder

WORKDIR /build

RUN apk add --no-cache curl

# install uv
RUN python3 -m pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync
COPY . .
ENV PATH=/app/.venv/bin:$PATH
ENTRYPOINT [ "./entrypoint.sh" ]

# FROM python:3.13.2-alpine AS runtime

# WORKDIR /app
# # RUN python3 -m pip install uv
# COPY --from=builder /build/.venv /app/.venv
# COPY . .
# ENV PATH=/app/.venv/bin:$PATH
# ENTRYPOINT [ "./entrypoint.sh" ]
