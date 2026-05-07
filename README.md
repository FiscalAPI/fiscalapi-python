# FiscalAPI SDK para Python

[![PyPI version](https://badge.fury.io/py/fiscalapi.svg?cachebuster=1)](https://badge.fury.io/py/fiscalapi)
[![License: MPL-2.0](https://img.shields.io/badge/License-MPL_2.0-blue.svg)](https://github.com/FiscalAPI/fiscalapi-python/blob/main/LICENSE.txt)

**SDK oficial de https://fiscalapi.com para Python**, la API de facturación CFDI y otros servicios fiscales en México. Simplifica la integración con los servicios de facturación electrónica, eliminando las complejidades del SAT y facilitando la generación de facturas, notas de crédito, complementos de pago, nómina, carta porte, y más. ¡Facturar sin dolor ahora es posible!


## 📋 Facturación CFDI 4.0
- **Soporte completo para CFDI 4.0** con todas las especificaciones oficiales
- **Timbrado de facturas de ingreso** con validación automática
- **Timbrado de notas de crédito** (facturas de egreso)
- **Timbrado de complementos de pago** en MXN, USD y EUR
- **Timbrado de facturas de nómina** 
- **Timbrado de facturas de carta porte** 
- **Timbrado de facturas de comercio exterior** 
- **Consulta del estatus de facturas** en el SAT en tiempo real
- **Cancelación de facturas**
- **Generación de archivos PDF** de las facturas con formato profesional
- **Personalización de logos y colores** en los PDF generados
- **Envío de facturas por correo electrónico** automatizado
- **Descarga de archivos XML** con estructura completa
- **Almacenamiento y recuperación** de facturas por 5 años
- Dos [modos de operación](https://docs.fiscalapi.com/modes-of-operation): **Por valores** o **Por referencias**
- [Ejemplos en Python](https://github.com/FiscalAPI/fiscalapi-samples-python)
  
## 📥 Descarga Masiva
- **Acceso a catálogos de descarga masiva** del SAT
- **Descarga de CFDI y Metadatos** en lotes grandes
- **Descarga masiva XML** con filtros personalizados
- **Reglas de descarga automática por RFC** 
- **Solicitudes de descarga** via API y Dashboard.
- **Automatización de solicitudes de descarga**

## 👥 Gestión de Personas
- **Administración de personas** (emisores, receptores, clientes, usuarios, etc.)
- **Gestión de certificados CSD y FIEL** (subir archivos .cer y .key a FiscalAPI)
- **Configuración de datos fiscales** (RFC, domicilio fiscal, régimen fiscal)
- **Datos de empleado** (agrega/actualiza/elimina datos de empleado a una persona. CFDI Nómina)
- **Datos de empleador** (agrega/actualiza/elimina datos de empleador a una persona. CFDI Nómina)

## 🎖️ Gestión de Timbres 
- **Gestión de folios fiscales** Compra timbres a fiscalapi y transfiere/retira a las personas de tu organizacion segun tus reglas de negocio.


## 🛍️ Gestión de Productos/Servicios
- **Gestión de productos y servicios** con catálogo personalizable
- **Administración de impuestos aplicables** (IVA, ISR, IEPS)

## 📚 Consulta de Catálogos SAT
- **Consulta en catálogos oficiales del SAT** actualizados
- **Consulta en catálogos oficiales de Descarga masiva del SAT** actualizados
- **Búsqueda de información** en catálogos del SAT con filtros avanzados
- **Acceso y búsqueda** en catálogos completos

## 🎫 Gestión de Timbres
- **Listar transacciones de timbres** con paginación
- **Consultar transacciones** por ID
- **Transferir timbres** entre personas
- **Retirar timbres** de una persona

## 📖 Recursos Adicionales
- **Cientos de ejemplos de código** disponibles en múltiples lenguajes de programación
- Documentación completa con guías paso a paso
- Ejemplos prácticos para casos de uso comunes
- Soporte técnico especializado
- Actualizaciones regulares conforme a cambios del SAT

## 📦 Instalación

**pip**:
```bash
pip install fiscalapi
```

**poetry**:
```bash
poetry add fiscalapi
```

## ⚙️ Configuración

### Configuración Básica

1. **Crea un objeto de configuración** con [tus credenciales](https://docs.fiscalapi.com/credentials-info):
```python
from fiscalapi import FiscalApiSettings

settings = FiscalApiSettings(
    api_url="https://test.fiscalapi.com",  # https://live.fiscalapi.com (producción)
    api_key="<API_KEY>",
    tenant="<TENANT_KEY>"
)
```

2. **Crea la instancia del cliente**:
```python
from fiscalapi import FiscalApiClient

client = FiscalApiClient(settings=settings)
```

## 🔄 Modos de Operación

FiscalAPI admite dos [modos de operación](https://docs.fiscalapi.com/modes-of-operation):

- **Por Referencias**: Envía solo IDs de objetos previamente creados en el dashboard de FiscalAPI.  
  Ideal para integraciones ligeras.

- **Por Valores**: Envía todos los campos requeridos en cada petición, con mayor control sobre los datos.  
  No se requiere configuración previa en el dashboard.

## 📝 Ejemplos de Uso

### 1. Crear una Persona (Emisor o Receptor)

```python
from fiscalapi import Person

person = Person(
    legal_name="Empresa Python SA de CV",
    email="mail7@gmail.com",
    password="TestPassword1234!"
)

api_response = client.people.create(person)
```

### 2. Subir Certificados CSD

[Descarga certificados de prueba](https://docs.fiscalapi.com/tax-files-info)

```python
from fiscalapi import TaxFile

# Subir certificado (CER)
certificado_csd = TaxFile(
    person_id="3f3478b4-60fd-459e-8bfc-f8239fc96257",
    tin="FUNK671228PH6",
    base64_file="MIIFgDCCA2igAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0NDYwDQYJKo...",
    file_type=0,  # 0 para certificado, 1 para llave privada
    password="12345678a"    
)

# Subir llave privada (KEY)
clave_privada_csd = TaxFile(
    person_id="3f3478b4-60fd-459e-8bfc-f8239fc96257",
    tin="FUNK671228PH6",
    base64_file="MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAg...",
    file_type=1,
    password="12345678a"
)

api_response_cer = client.tax_files.create(certificado_csd)
api_response_key = client.tax_files.create(clave_privada_csd)
```

### 3. Crear un Producto o Servicio

```python
from fiscalapi import Product

product = Product(
    description="Producto python sin impuestos",
    unit_price=Decimal("100.00")
)

api_response = client.products.create(product)
```

### 4. Actualizar Impuestos de un Producto

```python
from fiscalapi import Product, ProductTax

product = Product(
    id="f4bf4df3-5a91-4a30-b137-52cb517d13c4",
    description="Producto python sin impuestos",
    unit_price=Decimal("100.00"),
    product_taxes=[
        ProductTax(
            rate=Decimal("0.160000"),
            taxId="002",
            taxFlagId="T",
            taxTypeId="Tasa"
        ),
        ProductTax(
            rate=Decimal("0.106667"),
            taxId="002",
            taxFlagId="R",
            taxTypeId="Tasa"
        ),
        ProductTax(
            rate=Decimal("0.100000"),
            taxId="001",
            taxFlagId="R",
            taxTypeId="Tasa"
        )
    ]
)

api_response = client.products.update(product)
```

### 5. Crear una Factura de Ingreso (Por Referencias)

```python
from datetime import datetime
from decimal import Decimal
from fiscalapi import Invoice, InvoiceIssuer, InvoiceItem, InvoiceRecipient

invoice = Invoice(
    version_code="4.0",
    series="F",
    date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    payment_form_code="01",
    payment_conditions="Contado",
    currency_code="MXN",
    type_code="I",
    expedition_zip_code="42501",
    payment_method_code="PUE",
    exchange_rate=1,
    export_code="01",
    issuer=InvoiceIssuer(
        id="3f3478b4-60fd-459e-8bfc-f8239fc96257"
    ),
    recipient=InvoiceRecipient(
        id="96b46762-d246-4a67-a562-510a25dbafa9"
    ),
    items=[
        InvoiceItem(
            id="114a4be5-fb65-40b2-a762-ff0c55c6ebfa",
            quantity=Decimal("1.5"),
            discount=Decimal("255.85")
        )
    ]
)

api_response = client.invoices.create(invoice)
```

### 6. Crear la Misma Factura de Ingreso (Por Valores)

```python
from fiscalapi import Invoice, InvoiceIssuer, InvoiceItem, InvoiceRecipient, ItemTax, TaxCredential

invoice = Invoice(
    version_code="4.0",
    series="F",
    date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    payment_form_code="01",
    currency_code="MXN",
    type_code="I",
    expedition_zip_code="42501",
    payment_method_code="PUE",
    exchange_rate=1,
    export_code="01",
    issuer=InvoiceIssuer(
        tin="FUNK671228PH6",
        legal_name="KARLA FUENTE NOLASCO",
        tax_regime_code="621",
        tax_credentials=[
            TaxCredential(
                base64_file="MIIFgDCCA2igAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0NDYwDQYJKo...",
                file_type=0,
                password="12345678a"
            ),
            TaxCredential(
                base64_file="MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAg...",
                file_type=1,
                password="12345678a"
            )
        ]
    ),
    recipient=InvoiceRecipient(
        tin="EKU9003173C9",
        legal_name="ESCUELA KEMPER URGATE",
        zip_code="42501",
        tax_regime_code="601",
        cfdi_use_code="G01",
        email="mail@domain.com"
    ),
    items=[
        InvoiceItem(
            item_code="84111506",
            quantity=Decimal("9.5"),
            unit_of_measurement_code="E48",
            description="Invoicing software as a service",
            unit_price=Decimal("3587.75"),
            tax_object_code="02",
            item_sku="7506022301697",
            discount=Decimal("255.85"),
            item_taxes=[
                ItemTax(
                    tax_code="002",
                    tax_type_code="Tasa",
                    tax_rate=Decimal("0.160000"),
                    tax_flag_code="T"
                )
            ]
        )
    ]
)

api_response = client.invoices.create(invoice)
```

### 7. Búsqueda en Catálogos del SAT

```python
# Visite https://docs.fiscalapi.com/catalogs
# Buscar registros que contengan 'Tarjeta' en el catalogo oficial Formas de pago 'SatPaymentForms' (página 1, tamaño página 10)
api_response = client.catalogs.search_catalog("SatPaymentForms", "Tarjeta", 1, 10)

if api_response.succeeded:
    for item in api_response.data.items:
        print(f"Unidad: {item.description}")
else:
    print(api_response.message)
```

## 📋 Operaciones Principales

- **Facturas (CFDI)**
  Crear facturas de ingreso, notas de crédito, complementos de pago, cancelaciones, generación de PDF/XML.
- **Personas (Clientes/Emisores)**
  Alta y administración de personas, gestión de certificados (CSD).
- **Productos y Servicios**
  Administración de catálogos de productos, búsqueda en catálogos SAT.
- **Timbres**
  Listar transacciones, transferir y retirar timbres entre personas.

## 📂 Más Ejemplos

- [Gestión de Timbres](examples/ejemplos-timbres.py)
- [Complementos de Pago](examples/ejemplos-facturas-de-complemento-pago.py)
- [Facturas de Nómina](examples/ejemplos-facturas-de-nomina.py)
- [Impuestos Locales (Por Valores)](examples/ejemplos-factura-impuestos-locales-valores.py)
- [Impuestos Locales (Por Referencias)](examples/ejemplos-factura-impuestos-locales-referencias.py)

## 🤝 Contribuir

1. Haz un fork del repositorio.
2. Crea una rama para tu feature: `git checkout -b feature/AmazingFeature`
3. Realiza commits de tus cambios: `git commit -m 'Add some AmazingFeature'`
4. Sube tu rama: `git push origin feature/AmazingFeature`
5. Abre un Pull Request en GitHub.

## 🐛 Reportar Problemas

1. Asegúrate de usar la última versión del SDK.
2. Verifica si el problema ya fue reportado.
3. Proporciona un ejemplo mínimo reproducible.
4. Incluye los mensajes de error completos.

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia **MPL**. Consulta el archivo [LICENSE](LICENSE.txt) para más detalles.

## 🔗 Enlaces Útiles

- [Documentación Oficial](https://docs.fiscalapi.com)
- [Como obtener mis credenciales](https://docs.fiscalapi.com/credentials-info)
- [Portal de FiscalAPI](https://fiscalapi.com)
- [Soporte técnico](https://fiscalapi.com/contact-us)
- [Certificados de prueba](https://docs.fiscalapi.com/tax-files-info)
- [Postman Collection](https://documenter.getpostman.com/view/4346593/2sB2j4eqXr)
- [SDKs en otros lenguajes](https://docs.fiscalapi.com/sdks)
---

Desarrollado con ❤️ por [Fiscalapi](https://www.fiscalapi.com)
