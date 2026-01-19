# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FiscalAPI Python SDK - Official SDK for integrating with FiscalAPI, Mexico's electronic invoicing (CFDI 4.0) and fiscal services platform. Simplifies integration with SAT (Mexico's tax authority) for invoice creation, tax certificate management, and bulk downloads.

## Build and Publish Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Build distribution packages
pip install setuptools wheel twine build
python -m build

# Verify packages before publishing
twine check dist/*

# Publish to PyPI (requires PYPI_API_TOKEN)
twine upload --username __token__ --password $PYPI_API_TOKEN dist/*
```

**Version management:** Version is defined in `setup.py`. CI/CD requires the version to match the git tag (vX.Y.Z format).

## Architecture

### Service-Oriented Design with Facade Pattern

```
FiscalApiClient (Facade)
    │
    ├── FiscalApiSettings (Configuration)
    │
    └── Services (all inherit from BaseService)
        ├── invoice_service.py    → Invoice CRUD, PDF, XML, cancellation, SAT status
        ├── people_service.py     → Person/entity management
        ├── product_service.py    → Product/service catalog
        ├── tax_file_servive.py   → CSD/FIEL certificate uploads
        ├── api_key_service.py    → API key management
        ├── catalog_service.py    → SAT catalog searches
        └── download_*_service.py → Bulk download management
```

**Entry Point Pattern:**
```python
from fiscalapi import FiscalApiClient, FiscalApiSettings

settings = FiscalApiSettings(api_url="...", api_key="...", tenant="...")
client = FiscalApiClient(settings=settings)

# Access services through client
client.invoices.create(invoice)
client.people.get_list(page_num, page_size)
```

### Models (Pydantic v2)

Located in `fiscalapi/models/`:
- **common_models.py** - Base DTOs: `ApiResponse[T]`, `PagedList[T]`, `ValidationFailure`, `FiscalApiSettings`
- **fiscalapi_models.py** - Domain models: `Invoice`, `Person`, `Product`, `TaxFile`, and related entities

**Key Pattern - Field Aliasing:** Models use Pydantic `Field(alias="...")` for API JSON field mapping. When serializing, use `by_alias=True` and `exclude_none=True`.

### Two Operation Modes

1. **By References** - Use pre-created object IDs (faster, less data transfer)
2. **By Values** - Send all field data directly (self-contained, no prior setup)

See `examples.py` and README.md for detailed examples of both modes.

### Request/Response Flow

1. Service method receives domain object
2. `BaseService.send_request()` serializes to JSON (excludes None, uses aliases)
3. URL constructed: `{base_url}/api/{version}/{endpoint}`
4. Headers added: `X-TENANT-KEY`, `X-API-KEY`, `X-TIME-ZONE`
5. Response deserialized to `ApiResponse[T]` with typed data

### SSL Handling

- Development (localhost/127.0.0.1): SSL verification disabled
- Production: Uses certifi certificate store

## Key Files

- `fiscalapi/__init__.py` - Central exports for all models and services
- `fiscalapi/services/base_service.py` - HTTP client, serialization, response handling
- `fiscalapi/services/fiscalapi_client.py` - Main client facade
- `examples.py` - 3600+ lines of usage examples (commented out)
- `setup.py` - Package metadata, version, and dependencies

## Dependencies

- Python >= 3.9 (CI/CD uses Python 3.9.13)
- pydantic >= 2.0.0 (validation & serialization)
- requests >= 2.0.0 (HTTP client)
- email_validator >= 2.2.0

## Development Setup

```bash
# Create virtual environment with Python 3.9.13
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Code Standards

### Pydantic v2 Compatibility

- Use `model_config = ConfigDict(...)` instead of `class Config:`
- Use `list[T]` and `dict[K,V]` (Python 3.9+ built-in generics) instead of `List[T]` and `Dict[K,V]`
- Use `default_factory=list` for mutable defaults, never `default=[]`
- All Field() calls should have explicit `default=...` for required fields

### Type Annotations

- All service methods must have return type annotations
- Use `Optional[T]` only for truly optional fields
- `ApiResponse[T]` supports any type T (not just BaseModel subclasses)

## External Resources

- API Documentation: https://docs.fiscalapi.com
- Test Certificates: https://docs.fiscalapi.com/recursos/descargas
- Postman Collection: Available in docs
