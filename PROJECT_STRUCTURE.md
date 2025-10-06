# QuantumTrade Project Structure

```
quantumtrade/
├── README.md
├── LICENSE
├── .gitignore
├── .env.example
├── docs/
│   ├── setup.md
│   ├── api.md
│   ├── architecture.md
│   ├── deployment.md
│   └── troubleshooting.md
├── scripts/
│   ├── start.sh         # One-command root start
│   ├── setup.sh         # One-command root setup
│   └── cleanup.sh       # Safe Docker cleanup
├── frontend/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── package.json
│   ├── vite.config.js
│   ├── public/
│   │   ├── index.html
│   │   └── assets/
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── features/
│       ├── components/
│       ├── hooks/
│       ├── context/
│       ├── services/
│       └── utils/
├── backend/
│   ├── Dockerfile
│   ├── Dockerfile.dev
│   ├── requirements.txt
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── core/
│   │   ├── services/
│   │   ├── agents/
│   │   │   └── plugins/
│   │   ├── api/
│   │   │   ├── server.py
│   │   │   ├── routes/
│   │   │   └── middleware/
│   │   ├── database/
│   │   │   └── migrations/
│   │   ├── config/
│   │   │   ├── environments/
│   │   │   └── feature_flags.yaml
│   │   └── utils/
│   ├── tests/
│   └── scripts/
│       ├── db_migrate.sh
├── docker/
│   ├── docker-compose.yml
│   └── .dockerignore
```

