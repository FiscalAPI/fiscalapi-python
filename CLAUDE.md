# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FiscalAPI Python SDK - Official SDK for integrating with FiscalAPI, Mexico's electronic invoicing (CFDI 4.0) and fiscal services platform. Simplifies integration with SAT (Mexico's tax authority) for invoice creation, tax certificate management, payroll invoices (CFDI de Nomina), and bulk downloads.

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

# Clean build artifacts
rm -rf dist build fiscalapi.egg-info
```

**Version management:** Version is defined in `setup.py` (line 5: `VERSION = "X.Y.Z"`). CI/CD is manually triggered via `workflow_dispatch`.

## Architecture

### Service-Oriented Design with Facade Pattern

```
FiscalApiClient (Facade)
    │
    ├── FiscalApiSettings (Configuration)
    │
    └── Services (all inherit from BaseService)
        ├── invoice_service.py        → Invoice CRUD, PDF, XML, cancellation, SAT status
        ├── people_service.py         → Person/entity management
        │   ├── employee_service.py   → Employee data (sub-service for payroll)
        │   └── employer_service.py   → Employer data (sub-service for payroll)
        ├── product_service.py        → Product/service catalog
        ├── tax_file_service.py       → CSD/FIEL certificate uploads
        ├── api_key_service.py        → API key management
        ├── catalog_service.py        → SAT catalog searches
        ├── stamp_service.py          → Stamp (timbres) transactions
        └── download_*_service.py     → Bulk download management
```

**Entry Point Pattern:**
```python
from fiscalapi import FiscalApiClient, FiscalApiSettings

settings = FiscalApiSettings(api_url="...", api_key="...", tenant="...")
client = FiscalApiClient(settings=settings)

# Access services through client
client.invoices.create(invoice)
client.people.get_list(page_num, page_size)
client.stamps.get_list(page_num, page_size)
```

### Models (Pydantic v2)

Located in `fiscalapi/models/`:
- **common_models.py** - Base DTOs: `ApiResponse[T]`, `PagedList[T]`, `ValidationFailure`, `FiscalApiSettings`
- **fiscalapi_models.py** - Domain models: `Invoice`, `Person`, `Product`, `TaxFile`, payroll complements, stamp transactions

**Key Pattern - Field Aliasing:** Models use Pydantic `Field(alias="...")` for API JSON field mapping. When serializing, use `by_alias=True` and `exclude_none=True`.

### Public API Exports

All types are exported from the main package (`fiscalapi/__init__.py`):
```python
from fiscalapi import Invoice, Person, Product, FiscalApiClient, ApiResponse
```

Also available via submodules:
```python
from fiscalapi.models import Invoice, Person
from fiscalapi.services import InvoiceService, StampService
```

### Two Operation Modes

1. **By References** - Use pre-created object IDs (faster, less data transfer)
2. **By Values** - Send all field data directly (self-contained, no prior setup)

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

- `fiscalapi/__init__.py` - Central exports for all 85 public types (models + services)
- `fiscalapi/services/base_service.py` - HTTP client, serialization, response handling
- `fiscalapi/services/fiscalapi_client.py` - Main client facade
- `setup.py` - Package metadata, version, and dependencies

## Example Files

All example files are located in the `examples/` directory:

- `examples/examples.py` - General usage examples (all invoice types)
- `examples/ejemplos-facturas-de-nomina.py` - Payroll invoice examples (13 types)
- `examples/ejemplos-facturas-de-complemento-pago.py` - Payment complement examples
- `examples/ejemplos-timbres.py` - Stamp service examples
- `examples/ejemplos-factura-impuestos-locales-valores.py` - Local taxes examples (by values)
- `examples/ejemplos-factura-impuestos-locales-referencias.py` - Local taxes examples (by references)

## Reference Documentation

- `payroll-requirements.md` - Detailed payroll implementation spec with all models, services, and SAT codes

## Dependencies

- Python >= 3.9 (CI/CD uses Python 3.9.13)
- pydantic >= 2.0.0 (validation & serialization)
- requests >= 2.0.0 (HTTP client)
- email_validator >= 2.2.0

## Development Setup

```bash
# Create virtual environment with Python 3.9+
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

### Adding New Services

1. Create service class inheriting from `BaseService` in `fiscalapi/services/`
2. Export from `fiscalapi/services/__init__.py`
3. Export from `fiscalapi/__init__.py`
4. Add property to `FiscalApiClient` class

## External Resources

- API Documentation: https://docs.fiscalapi.com
- Test Certificates: https://docs.fiscalapi.com/recursos/descargas
- Postman Collection: https://documenter.getpostman.com/view/4346593/2sB2j4eqXr
