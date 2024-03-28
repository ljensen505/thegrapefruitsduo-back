# Backend for thegrapefruitsduo.com

Use of poetry required.

To install dependencies:

```bash
poetry install
```

To seed the mysql database:

```bash
poetry run seed
```

To run the FastAPI app:

```bash
poetry run uvicorn app:app --reload --workers 2
```
