#!/bin/sh
exec uv run uvicorn --host 0.0.0.0 --port 5022 --factory 'webapp:make_app'
