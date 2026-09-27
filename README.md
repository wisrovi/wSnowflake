<p align="center">
  <a href="https://linkedin.com/in/wisrovi-rodriguez"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="https://wisrovi.dev"><img src="https://img.shields.io/badge/Author-wisrovi.dev-111827?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Portal" /></a>
  <a href="https://orcid.org/0009-0005-0710-1861"><img src="https://img.shields.io/badge/ORCID-0009--0005--0710--1861-A6CE39?style=for-the-badge&logo=orcid&logoColor=white" alt="ORCID" /></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License" /></a>
</p>

# wSnowflake

**Snowflake SQL ORM library for Python - type-safe database operations**

High-level Python ORM library providing a clean, type-safe interface for Snowflake database operations using Pydantic models for schema definition.

## Key Features

- **Pydantic Integration** - Define database schema using Pydantic models
- **Auto Table Creation** - Tables created/synchronized automatically with model changes
- **CRUD Operations** - Simple insert, get, update, delete methods
- **Type Safety** - Full type hints and Pydantic validation
- **Query Builder** - Safe query construction with SQL injection prevention
- **CLI Tool** - Command-line interface for common operations
- **Code Quality** - Pylint compatible, comprehensive type hints

## Technical Stack

- **Python**: 3.8+
- **Key Libraries**: snowflake-connector-python>=2.8.0
- **Testing**: pytest, pytest-cov, pytest-asyncio
- **Code Quality**: ruff, mypy

## Installation & Setup

```bash
pip install wsnowflake
```

Development installation:
```bash
pip install -e ".[dev]"
```

## Architecture & Workflow

```
wSnowflake/
├── src/wSnowflake/        # Main library package
│   ├── core/             # Core database operations
│   ├── builders/         # SQL query builder
│   ├── exceptions/      # Custom exceptions
│   ├── types/           # SQL type mapping
│   └── cli/             # CLI tool
├── examples/             # Usage examples (13+ folders)
├── test/                 # Test suite
│   ├── unit/           # Unit tests
│   └── integration/    # Integration tests
├── docs/                 # Sphinx documentation
├── stress_test/         # Performance testing
├── docker/              # Docker configurations
├── pyproject.toml       # Project config
└── README.md
```

**Workflow**: Define Pydantic model → Configure Snowflake connection → Initialize WSnowflake → Perform CRUD operations

## Configuration

**Environment Variables**:
- `SNOWFLAKE_USER` - Snowflake username
- `SNOWFLAKE_PASSWORD` - Snowflake password
- `SNOWFLAKE_ACCOUNT` - Snowflake account identifier
- `SNOWFLAKE_WAREHOUSE` - Warehouse name
- `SNOWFLAKE_DATABASE` - Database name
- `SNOWFLAKE_SCHEMA` - Schema name

**Configuration Files**:
- `pyproject.toml` - Project metadata and dependencies
- `setup.py` - Package configuration

## Usage

```python
from pydantic import BaseModel
from wSnowflake import WSnowflake, ConnectionManager

SF_CONFIG = {
    "user": "your_user",
    "password": "your_password",
    "account": "your_account",
    "warehouse": "your_warehouse",
    "database": "your_database",
    "schema": "your_schema",
}

class User(BaseModel):
    id: int
    name: str
    email: str

cm = ConnectionManager(**SF_CONFIG)
db = WSnowflake(cm)
db.insert(User(id=1, name="John", email="john@example.com"))
users = db.get_all()
```

---

## 👤 Autor & Afiliación Oficial

* **William Steve Rodriguez Villamizar (Wisrovi)**
* **Cargo:** Principal AI Engineer & Applied AI Solutions Architect | Scientific Researcher
* 📧 **Email:** [wisrovi.rodriguez@gmail.com](mailto:wisrovi.rodriguez@gmail.com) / [wisrovi@wisrovi.dev](mailto:wisrovi@wisrovi.dev)
* 🌐 **Portal Oficial:** [wisrovi.dev](https://wisrovi.dev)
* 💼 **LinkedIn:** [wisrovi-rodriguez](https://www.linkedin.com/in/wisrovi-rodriguez/)
* 🆔 **ORCID:** [0009-0005-0710-1861](https://orcid.org/0009-0005-0710-1861)
* 📦 **PyPI:** [pypi.org/user/wisrovi/](https://pypi.org/user/wisrovi/)
* 🐙 **GitHub:** [@wisrovi](https://github.com/wisrovi)


