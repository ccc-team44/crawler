#!/usr/bin/env bash
docker build --tag crawler:1.0 . &&    crawler:1.0docker run --network host -it -e DATABASE_USER=admin -e DATABASE_PASSWORD=1111 -e DATABASE_PORT=5984 -e DATABASE_HOST=172.26.130.31 -e NODE_INDEX=0