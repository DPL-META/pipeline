# tooling-interview

## PRODUCTS

#### requisitos:
- python 3.12
- poetry

#### instalando dependencias
```sh
poetry install
```

#### executando local
```sh
poetry run uvicorn app.main:app --host 0.0.0.0
```

#### executando tests
```sh
poetry run pytest
```

## USERS

#### requisitos:
- node 23.6.0

#### instalando dependencias
```sh
npm i
```

### executando as migrations com ORM
```bash
npm run migrate 
``` 

### executando o seed inicial
```bash
npm run seed
```

#### executando local
```sh
npm run dev
```

#### executando tests
```sh
npm run test
npm run test:e2e
```

### executando o build
```bash
npm run build
```

### executando o código do build da aplicação
```bash
npm start
```
