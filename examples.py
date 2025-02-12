from datetime import datetime
from decimal import Decimal
from fiscalapi.models.common_models import FiscalApiSettings
from fiscalapi.models.fiscalapi_models import Invoice, InvoiceIssuer, InvoiceItem, InvoiceRecipient, ItemTax, Product, ProductTax, Person, RelatedInvoice, TaxCredential, TaxFile
from fiscalapi.services.fiscalapi_client import FiscalApiClient

def main ():
    
    print("Hello World!")
    
    settings = FiscalApiSettings(
            api_url="https://test.fiscalapi.com",
            api_key="<API_KEY>",
            tenant="<TENANT_KEY>",
    )
    
    client = FiscalApiClient(settings=settings)
        
    # listar productos
    #api_response = client.products.get_list(1, 10)
    
    
    # obtener producto por id
    # api_response = client.products.get_by_id("27808326-1824-4f3c-87fb-03ace1066f16")
    
    # crear producto
    # product: Product = Product(
    #     description="Producto python sin impuestos",
    #     unit_price=Decimal("100.00")
    # )
    
    # api_response = client.products.create(product)

    
    
    # actualizar producto
    # product: Product = Product(
    #     id="f4bf4df3-5a91-4a30-b137-52cb517d13c4",
    #     description="Producto python sin impuestos",
    #     unit_price=Decimal("100.00"),
    #     product_taxes=[
    #         ProductTax(
    #             rate=Decimal("0.160000"),
    #             taxId="002",
    #             taxFlagId="T",
    #             taxTypeId="Tasa"
    #         ),
    #         ProductTax(
    #             rate=Decimal("0.106667"),
    #             taxId="002",
    #             taxFlagId="R",
    #             taxTypeId="Tasa"
    #         ),
    #         ProductTax(
    #             rate=Decimal("0.100000"),
    #             taxId="001",
    #             taxFlagId="R",
    #             taxTypeId="Tasa"
    #         )
            
    #     ]
    # )
    
    # api_response = client.products.update(product)
    
    
    
    # Eliminar producto
    # api_response = client.products.delete("c86c400a-71df-4dbc-ab2b-2f4b0f32c5ac")
    
    
    
    # Listar personas
    # api_response = client.people.get_list(1, 10)
    
    # Obtener persona por id
    # api_response = client.people.get_by_id("3f3478b4-60fd-459e-8bfc-f8239fc96257")
    
    

    # Crear persona
    # person: Person = Person(
    #     legal_name="Empresa Python SA de CV",
    #     email="mail7@gmail.com",
    #     password="TestPassword1234!",
    # )

    # api_response = client.people.create(person)
    
    

    # Actualizar persona
    # person: Person = Person(
    #     id="637245ad-86b5-43ab-ac20-eb94f04aa9e8", # Id de la persona
    #     legal_name="ESCUELA KEMPER URGATE", # Razon social
    #     tin="EKU9003173C9", # RFC
    #     capital_regime="SA de CV",# Regimen de capital
    #     sat_tax_regime_id="601", # General de Ley Personas Morales
    #     sat_cfdi_use_id="G03", # Gastos en general
    #     zip_code="42501", # Codigo postal de la constancia de situacion fiscal
    #     tax_password="12345678a", # Contraseña de los sellos (certificados SAT)
    #     #email="newmail@gmail.com", # Correo electronico
    #     #password="NewPassword1234!", # Contraseña para acceder al dashboard
    # )
    
    # api_response = client.people.update(person)
    
    
    # Eliminar persona
    # api_response = client.people.delete("e8faddaa-f0d3-4c68-b046-dfe32f6c3ef9")
    



    # Listar certificados    
    # api_response = client.tax_files.get_list(1, 10)
    
    
    
    # Obtener certificado por id
    # api_response = client.tax_files.get_by_id("90f2c101-87cf-4ab6-97af-92f45e62e09d")
    
    
    # Crear certificado (subir certificado a KARLA FUENTE NOLASCO)
    # tax_file: TaxFile = TaxFile(
    #     person_id="3f3478b4-60fd-459e-8bfc-f8239fc96257",
    #     tin="FUNK671228PH6",
    #     base64_file="MIIFgDCCA2igAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0NDYwDQYJKoZIhvcNAQELBQAwggErMQ8wDQYDVQQDDAZBQyBVQVQxLjAsBgNVBAoMJVNFUlZJQ0lPIERFIEFETUlOSVNUUkFDSU9OIFRSSUJVVEFSSUExGjAYBgNVBAsMEVNBVC1JRVMgQXV0aG9yaXR5MSgwJgYJKoZIhvcNAQkBFhlvc2Nhci5tYXJ0aW5lekBzYXQuZ29iLm14MR0wGwYDVQQJDBQzcmEgY2VycmFkYSBkZSBjYWxpejEOMAwGA1UEEQwFMDYzNzAxCzAJBgNVBAYTAk1YMRkwFwYDVQQIDBBDSVVEQUQgREUgTUVYSUNPMREwDwYDVQQHDAhDT1lPQUNBTjERMA8GA1UELRMIMi41LjQuNDUxJTAjBgkqhkiG9w0BCQITFnJlc3BvbnNhYmxlOiBBQ0RNQS1TQVQwHhcNMjMwNTE4MTQzNTM3WhcNMjcwNTE4MTQzNTM3WjCBpzEdMBsGA1UEAxMUS0FSTEEgRlVFTlRFIE5PTEFTQ08xHTAbBgNVBCkTFEtBUkxBIEZVRU5URSBOT0xBU0NPMR0wGwYDVQQKExRLQVJMQSBGVUVOVEUgTk9MQVNDTzEWMBQGA1UELRMNRlVOSzY3MTIyOFBINjEbMBkGA1UEBRMSRlVOSzY3MTIyOE1DTE5MUjA1MRMwEQYDVQQLEwpTdWN1cnNhbCAxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhNXbTSqGX6+/3Urpemyy5vVG2IdP2v7v001+c4BoMxEDFDQ32cOFdDiRxy0Fq9aR+Ojrofq8VeftvN586iyA1A6a0QnA68i7JnQKI4uJy+u0qiixuHu6u3b3BhSpoaVHcUtqFWLLlzr0yBxfVLOqVna/1/tHbQJg9hx57mp97P0JmXO1WeIqi+Zqob/mVZh2lsPGdJ8iqgjYFaFn9QVOQ1Pq74o1PTqwfzqgJSfV0zOOlESDPWggaDAYE4VNyTBisOUjlNd0x7ppcTxSi3yenrJHqkq/pqJsRLKf6VJ/s9p6bsd2bj07hSDpjlDC2lB25eEfkEkeMkXoE7ErXQ5QCwIDAQABox0wGzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQsFAAOCAgEAHwYpgbClHULXYhK4GNTgonvXh81oqfXwCSWAyDPiTYFDWVfWM9C4ApxMLyc0XvJte75Rla+bPC08oYN3OlhbbvP3twBL/w9SsfxvkbpFn2ZfGSTXZhyiq4vjmQHW1pnFvGelwgU4v3eeRE/MjoCnE7M/Q5thpuog6WGf7CbKERnWZn8QsUaJsZSEkg6Bv2jm69ye57ab5rrOUaeMlstTfdlaHAEkUgLX/NXq7RbGwv82hkHY5b2vYcXeh34tUMBL6os3OdRlooN9ZQGkVIISvxVZpSHkYC20DFNh1Bb0ovjfujlTcka81GnbUhFGZtRuoVQ1RVpMO8xtx3YKBLp4do3hPmnRCV5hCm43OIjYx9Ov2dqICV3AaNXSLV1dW39Bak/RBiIDGHzOIW2+VMPjvvypBjmPv/tmbqNHWPSAWOxTyMx6E1gFCZvi+5F+BgkdC3Lm7U0BU0NfvsXajZd8sXnIllvEMrikCLoI/yurvexNDcF1RW/FhMsoua0eerwczcNm66pGjHm05p9DR6lFeJZrtqeqZuojdxBWy4vH6ghyJaupergoX+nmdG3JYeRttCFF/ITI68TeCES5V3Y0C3psYAg1XxcGRLGd4chPo/4xwiLkijWtgt0/to5ljGBwfK7r62PHZfL1Dp+i7V3w7hmOlhbXzP+zhMZn1GCk7KY=",
    #     file_type=0, # 0 para certificado, 1 para llave privada
    #     password="12345678a"    
    # )
    # api_response = client.tax_files.create(tax_file)
    # print(api_response)
     
    # Crear certificado (subir llave privada a KARLA FUENTE NOLASCO)
    # tax_file: TaxFile = TaxFile(
    #     person_id="3f3478b4-60fd-459e-8bfc-f8239fc96257",
    #     tin="FUNK671228PH6",
    #     base64_file="MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAgEAAoIBAQACAggAMBQGCCqGSIb3DQMHBAgwggS9AgEAMASCBMh4EHl7aNSCaMDA1VlRoXCZ5UUmqErAbucRBAKNQXH8t8gVCl/ItHMI2hMJ76QOECOqEi1Y89cDpegDvh/INXyMsXbzi87tfFzgq1O+9ID6aPWGg+bNGADXyXxDVdy7Nq/SCdoXvo66MTYwq8jyJeUHDHEGMVBcmZpD44VJCvLBxDcvByuevP4Wo2NKqJCwK+ecAdZc/8Rvd947SjbMHuS8BppfQWARVUqA5BLOkTAHNv6tEk/hncC7O2YOGSShart8fM8dokgGSyewHVFe08POuQ+WDHeVpvApH/SP29rwktSoiHRoL6dK+F2YeEB5SuFW9LQgYCutjapmUP/9TC3Byro9Li6UrvQHxNmgMFGQJSYjFdqlGjLibfuguLp7pueutbROoZaSxU8HqlfYxLkpJUxUwNI1ja/1t3wcivtWknVXBd13R06iVfU1HGe8Kb4u5il4a4yP4p7VT4RE3b1SBLJeG+BxHiE8gFaaKcX/Cl6JV14RPTvk/6VnAtEQ66qHJex21KKuiJo2JoOmDXVHmvGQlWXNjYgoPx28Xd5WsofL+n7HDR2Ku8XgwJw6IXBJGuoday9qWN9v/k7DGlNGB6Sm4gdVUmycMP6EGhB1vFTiDfOGQO42ywmcpKoMETPVQ5InYKE0xAOckgcminDgxWjtUHjBDPEKifEjYudPwKmR6Cf4ZdGvUWwY/zq9pPAC9bu423KeBCnSL8AQ4r5SVsW6XG0njamwfNjpegwh/YG7sS7sDtZ8gi7r6tZYjsOqZlCYU0j7QTBpuQn81Yof2nQRCFxhRJCeydmIA8+z0nXrcElk7NDPk4kYQS0VitJ2qeQYNENzGBglROkCl2y6GlxAG80IBtReCUp/xOSdlwDR0eim+SNkdStvmQM5IcWBuDKwGZc1A4v/UoLl7niV9fpl4X6bUX8lZzY4gidJOafoJ30VoY/lYGkrkEuz3GpbbT5v8fF3iXVRlEqhlpe8JSGu7Rd2cPcJSkQ1Cuj/QRhHPhFMF2KhTEf95c9ZBKI8H7SvBi7eLXfSW2Y0ve6vXBZKyjK9whgCU9iVOsJjqRXpAccaWOKi420CjmS0+uwj/Xr2wLZhPEjBA/G6Od30+eG9mICmbp/5wAGhK/ZxCT17ZETyFmOMo49jl9pxdKocJNuzMrLpSz7/g5Jwp8+y8Ck5YP7AX0R/dVA0t37DO7nAbQT5XVSYpMVh/yvpYJ9WR+tb8Yg1h2lERLR2fbuhQRcwmisZR2W3Sr2b7hX9MCMkMQw8y2fDJrzLrqKqkHcjvnI/TdzZW2MzeQDoBBb3fmgvjYg07l4kThS73wGX992w2Y+a1A2iirSmrYEm9dSh16JmXa8boGQAONQzQkHh7vpw0IBs9cnvqO1QLB1GtbBztUBXonA4TxMKLYZkVrrd2RhrYWMsDp7MpC4M0p/DA3E/qscYwq1OpwriewNdx6XXqMZbdUNqMP2viBY2VSGmNdHtVfbN/rnaeJetFGX7XgTVYD7wDq8TW9yseCK944jcT+y/o0YiT9j3OLQ2Ts0LDTQskpJSxRmXEQGy3NBDOYFTvRkcGJEQJItuol8NivJN1H9LoLIUAlAHBZxfHpUYx66YnP4PdTdMIWH+nxyekKPFfAT7olQ=",
    #     file_type=1, # 0 para certificado, 1 para llave privada
    #     password="12345678a"
    # )
        
    
    # api_response = client.tax_files.create(tax_file)
    # print(api_response)
    
    
    # Eliminar certificado
    # api_response = client.tax_files.delete("6f65fb80-6c20-4cc6-ba1d-e109d4a3df70")
    
    
    # Obtener certificados por defecto de una persona
    # api_response = client.tax_files.get_default_values("3f3478b4-60fd-459e-8bfc-f8239fc96257")
    
    # print(api_response)
    
    
    # Obtener certificados por defecto de una persona (ids)
    
    #api_response = client.tax_files.get_default_references("3f3478b4-60fd-459e-8bfc-f8239fc96257")
    
    #print(api_response)
    
    
    
    # obtener lista de catalogos SAT disponibles en fiscalapi
    # api_response = client.catalogs.get_list()
    
    
    # obtener registro de un catalogo por nombre y id
    # obtiene el uso de cfdi con id G03 (Gastos en general) del catalogo de usos de cfdi (SatCfdiUses)
    #api_response = client.catalogs.get_record_by_id("SatCfdiUses", "G03")
    
    
    # buscar en un catalogo por nombre y texto de busqueda
    # obtiene los registros del catalogo de formas de pago (SatPaymentForms) que contengan la palabra "tarjeta"
    #api_response = client.catalogs.search_catalog("SatPaymentForms", "tarjeta")
    
    
    
    
    # Listar facturas
    #api_response = client.invoices.get_list(1, 2)
    
    
    
    # Obtener factura por id
    
    #api_response = client.invoices.get_by_id("05341ec6-538d-4d92-938e-acc9b33da47e",True)
    
    
    
    # Crear factura de ingreso por valores (cURL). 
    
    # curl --location 'https://localhost:7173/api/v4/invoices/income' \
    # --header 'X-TENANT-KEY: e839651d-1765-4cd0-ba7f-547a4c20580f' \
    # --header 'X-TIME-ZONE: America/Mexico_City' \
    # --header 'Content-Type: application/json' \
    # --header 'X-API-KEY: sk_development_e0e47dfa_5146_40c2_b3a3_3055909a6b88' \
    # --data-raw '{
    #   "versionCode": "4.0",
    #   "series": "F",
    #   "date": "2025-02-11T16:16:43",
    #   "paymentFormCode": "01",
    #   "currencyCode": "MXN",
    #   "typeCode": "I",
    #   "expeditionZipCode": "42501",
    #   "paymentMethodCode": "PUE",
    #   "exchangeRate": 1,
    #   "exportCode": "01",
    #   "issuer": {
    #     "tin": "FUNK671228PH6",
    #     "legalName": "KARLA FUENTE NOLASCO",
    #     "taxRegimeCode": "621",
    #     "taxCredentials": [
    #       {
    #         "base64File": "MIIFgDCCA2igAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0NDYwDQYJKoZIhvcNAQELBQAwggErMQ8wDQYDVQQDDAZBQyBVQVQxLjAsBgNVBAoMJVNFUlZJQ0lPIERFIEFETUlOSVNUUkFDSU9OIFRSSUJVVEFSSUExGjAYBgNVBAsMEVNBVC1JRVMgQXV0aG9yaXR5MSgwJgYJKoZIhvcNAQkBFhlvc2Nhci5tYXJ0aW5lekBzYXQuZ29iLm14MR0wGwYDVQQJDBQzcmEgY2VycmFkYSBkZSBjYWxpejEOMAwGA1UEEQwFMDYzNzAxCzAJBgNVBAYTAk1YMRkwFwYDVQQIDBBDSVVEQUQgREUgTUVYSUNPMREwDwYDVQQHDAhDT1lPQUNBTjERMA8GA1UELRMIMi41LjQuNDUxJTAjBgkqhkiG9w0BCQITFnJlc3BvbnNhYmxlOiBBQ0RNQS1TQVQwHhcNMjMwNTE4MTQzNTM3WhcNMjcwNTE4MTQzNTM3WjCBpzEdMBsGA1UEAxMUS0FSTEEgRlVFTlRFIE5PTEFTQ08xHTAbBgNVBCkTFEtBUkxBIEZVRU5URSBOT0xBU0NPMR0wGwYDVQQKExRLQVJMQSBGVUVOVEUgTk9MQVNDTzEWMBQGA1UELRMNRlVOSzY3MTIyOFBINjEbMBkGA1UEBRMSRlVOSzY3MTIyOE1DTE5MUjA1MRMwEQYDVQQLEwpTdWN1cnNhbCAxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhNXbTSqGX6+/3Urpemyy5vVG2IdP2v7v001+c4BoMxEDFDQ32cOFdDiRxy0Fq9aR+Ojrofq8VeftvN586iyA1A6a0QnA68i7JnQKI4uJy+u0qiixuHu6u3b3BhSpoaVHcUtqFWLLlzr0yBxfVLOqVna/1/tHbQJg9hx57mp97P0JmXO1WeIqi+Zqob/mVZh2lsPGdJ8iqgjYFaFn9QVOQ1Pq74o1PTqwfzqgJSfV0zOOlESDPWggaDAYE4VNyTBisOUjlNd0x7ppcTxSi3yenrJHqkq/pqJsRLKf6VJ/s9p6bsd2bj07hSDpjlDC2lB25eEfkEkeMkXoE7ErXQ5QCwIDAQABox0wGzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQsFAAOCAgEAHwYpgbClHULXYhK4GNTgonvXh81oqfXwCSWAyDPiTYFDWVfWM9C4ApxMLyc0XvJte75Rla+bPC08oYN3OlhbbvP3twBL/w9SsfxvkbpFn2ZfGSTXZhyiq4vjmQHW1pnFvGelwgU4v3eeRE/MjoCnE7M/Q5thpuog6WGf7CbKERnWZn8QsUaJsZSEkg6Bv2jm69ye57ab5rrOUaeMlstTfdlaHAEkUgLX/NXq7RbGwv82hkHY5b2vYcXeh34tUMBL6os3OdRlooN9ZQGkVIISvxVZpSHkYC20DFNh1Bb0ovjfujlTcka81GnbUhFGZtRuoVQ1RVpMO8xtx3YKBLp4do3hPmnRCV5hCm43OIjYx9Ov2dqICV3AaNXSLV1dW39Bak/RBiIDGHzOIW2+VMPjvvypBjmPv/tmbqNHWPSAWOxTyMx6E1gFCZvi+5F+BgkdC3Lm7U0BU0NfvsXajZd8sXnIllvEMrikCLoI/yurvexNDcF1RW/FhMsoua0eerwczcNm66pGjHm05p9DR6lFeJZrtqeqZuojdxBWy4vH6ghyJaupergoX+nmdG3JYeRttCFF/ITI68TeCES5V3Y0C3psYAg1XxcGRLGd4chPo/4xwiLkijWtgt0/to5ljGBwfK7r62PHZfL1Dp+i7V3w7hmOlhbXzP+zhMZn1GCk7KY=",
    #         "fileType": 0,
    #         "password": "12345678a"
    #       },
    #       {
    #         "base64File": "MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAgEAAoIBAQACAggAMBQGCCqGSIb3DQMHBAgwggS9AgEAMASCBMh4EHl7aNSCaMDA1VlRoXCZ5UUmqErAbucRBAKNQXH8t8gVCl/ItHMI2hMJ76QOECOqEi1Y89cDpegDvh/INXyMsXbzi87tfFzgq1O+9ID6aPWGg+bNGADXyXxDVdy7Nq/SCdoXvo66MTYwq8jyJeUHDHEGMVBcmZpD44VJCvLBxDcvByuevP4Wo2NKqJCwK+ecAdZc/8Rvd947SjbMHuS8BppfQWARVUqA5BLOkTAHNv6tEk/hncC7O2YOGSShart8fM8dokgGSyewHVFe08POuQ+WDHeVpvApH/SP29rwktSoiHRoL6dK+F2YeEB5SuFW9LQgYCutjapmUP/9TC3Byro9Li6UrvQHxNmgMFGQJSYjFdqlGjLibfuguLp7pueutbROoZaSxU8HqlfYxLkpJUxUwNI1ja/1t3wcivtWknVXBd13R06iVfU1HGe8Kb4u5il4a4yP4p7VT4RE3b1SBLJeG+BxHiE8gFaaKcX/Cl6JV14RPTvk/6VnAtEQ66qHJex21KKuiJo2JoOmDXVHmvGQlWXNjYgoPx28Xd5WsofL+n7HDR2Ku8XgwJw6IXBJGuoday9qWN9v/k7DGlNGB6Sm4gdVUmycMP6EGhB1vFTiDfOGQO42ywmcpKoMETPVQ5InYKE0xAOckgcminDgxWjtUHjBDPEKifEjYudPwKmR6Cf4ZdGvUWwY/zq9pPAC9bu423KeBCnSL8AQ4r5SVsW6XG0njamwfNjpegwh/YG7sS7sDtZ8gi7r6tZYjsOqZlCYU0j7QTBpuQn81Yof2nQRCFxhRJCeydmIA8+z0nXrcElk7NDPk4kYQS0VitJ2qeQYNENzGBglROkCl2y6GlxAG80IBtReCUp/xOSdlwDR0eim+SNkdStvmQM5IcWBuDKwGZc1A4v/UoLl7niV9fpl4X6bUX8lZzY4gidJOafoJ30VoY/lYGkrkEuz3GpbbT5v8fF3iXVRlEqhlpe8JSGu7Rd2cPcJSkQ1Cuj/QRhHPhFMF2KhTEf95c9ZBKI8H7SvBi7eLXfSW2Y0ve6vXBZKyjK9whgCU9iVOsJjqRXpAccaWOKi420CjmS0+uwj/Xr2wLZhPEjBA/G6Od30+eG9mICmbp/5wAGhK/ZxCT17ZETyFmOMo49jl9pxdKocJNuzMrLpSz7/g5Jwp8+y8Ck5YP7AX0R/dVA0t37DO7nAbQT5XVSYpMVh/yvpYJ9WR+tb8Yg1h2lERLR2fbuhQRcwmisZR2W3Sr2b7hX9MCMkMQw8y2fDJrzLrqKqkHcjvnI/TdzZW2MzeQDoBBb3fmgvjYg07l4kThS73wGX992w2Y+a1A2iirSmrYEm9dSh16JmXa8boGQAONQzQkHh7vpw0IBs9cnvqO1QLB1GtbBztUBXonA4TxMKLYZkVrrd2RhrYWMsDp7MpC4M0p/DA3E/qscYwq1OpwriewNdx6XXqMZbdUNqMP2viBY2VSGmNdHtVfbN/rnaeJetFGX7XgTVYD7wDq8TW9yseCK944jcT+y/o0YiT9j3OLQ2Ts0LDTQskpJSxRmXEQGy3NBDOYFTvRkcGJEQJItuol8NivJN1H9LoLIUAlAHBZxfHpUYx66YnP4PdTdMIWH+nxyekKPFfAT7olQ=",
    #         "fileType": 1,
    #         "password": "12345678a"
    #       }
    #     ]
    #   },
    #   "recipient": {
    #     "tin": "EKU9003173C9",
    #     "legalName": "ESCUELA KEMPER URGATE",
    #     "zipCode": "42501",
    #     "taxRegimeCode": "601",
    #     "cfdiUseCode": "G01",
    #     "email": "someone@somewhere.com"
    #   },
    #   "items": [
    #     {
    #       "itemCode": "01010101",
    #       "quantity": 9.5,
    #       "unitOfMeasurementCode": "E48",
    #       "unitOfMeasurement": "Unidad de servicio",
    #       "description": "Invoicing software as a service",
    #       "unitPrice": 3587.75,
    #       "taxObjectCode": "02",
    #       "itemSku": "7506022301697",
    #       "discount": 255.85,
    #       "itemTaxes": [
    #         {
    #           "taxCode": "002",
    #           "taxTypeCode": "Tasa",
    #           "taxRate": 0.160000,
    #           "TaxFlagCode": "T"
    #         }
    #       ]
    #     }
    #   ]
    # }'
    
    
   # Crear factura de ingreso por valores (Sdk). 
    # invoice = Invoice(
    #     version_code="4.0",
    #     series="F",
    #     date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), #YYYY-MM-DDThh:mm:ss
    #     payment_form_code="01",
    #     currency_code="MXN",
    #     type_code="I",
    #     expedition_zip_code="42501",
    #     payment_method_code="PUE",
    #     exchange_rate=1,
    #     export_code="01",
    #     issuer=InvoiceIssuer(
    #         tin="FUNK671228PH6",
    #         legal_name="KARLA FUENTE NOLASCO",
    #         tax_regime_code="621",
    #         tax_credentials= [
    #             TaxCredential(
    #                 base64_file="MIIFgDCCA2igAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0NDYwDQYJKoZIhvcNAQELBQAwggErMQ8wDQYDVQQDDAZBQyBVQVQxLjAsBgNVBAoMJVNFUlZJQ0lPIERFIEFETUlOSVNUUkFDSU9OIFRSSUJVVEFSSUExGjAYBgNVBAsMEVNBVC1JRVMgQXV0aG9yaXR5MSgwJgYJKoZIhvcNAQkBFhlvc2Nhci5tYXJ0aW5lekBzYXQuZ29iLm14MR0wGwYDVQQJDBQzcmEgY2VycmFkYSBkZSBjYWxpejEOMAwGA1UEEQwFMDYzNzAxCzAJBgNVBAYTAk1YMRkwFwYDVQQIDBBDSVVEQUQgREUgTUVYSUNPMREwDwYDVQQHDAhDT1lPQUNBTjERMA8GA1UELRMIMi41LjQuNDUxJTAjBgkqhkiG9w0BCQITFnJlc3BvbnNhYmxlOiBBQ0RNQS1TQVQwHhcNMjMwNTE4MTQzNTM3WhcNMjcwNTE4MTQzNTM3WjCBpzEdMBsGA1UEAxMUS0FSTEEgRlVFTlRFIE5PTEFTQ08xHTAbBgNVBCkTFEtBUkxBIEZVRU5URSBOT0xBU0NPMR0wGwYDVQQKExRLQVJMQSBGVUVOVEUgTk9MQVNDTzEWMBQGA1UELRMNRlVOSzY3MTIyOFBINjEbMBkGA1UEBRMSRlVOSzY3MTIyOE1DTE5MUjA1MRMwEQYDVQQLEwpTdWN1cnNhbCAxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhNXbTSqGX6+/3Urpemyy5vVG2IdP2v7v001+c4BoMxEDFDQ32cOFdDiRxy0Fq9aR+Ojrofq8VeftvN586iyA1A6a0QnA68i7JnQKI4uJy+u0qiixuHu6u3b3BhSpoaVHcUtqFWLLlzr0yBxfVLOqVna/1/tHbQJg9hx57mp97P0JmXO1WeIqi+Zqob/mVZh2lsPGdJ8iqgjYFaFn9QVOQ1Pq74o1PTqwfzqgJSfV0zOOlESDPWggaDAYE4VNyTBisOUjlNd0x7ppcTxSi3yenrJHqkq/pqJsRLKf6VJ/s9p6bsd2bj07hSDpjlDC2lB25eEfkEkeMkXoE7ErXQ5QCwIDAQABox0wGzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQsFAAOCAgEAHwYpgbClHULXYhK4GNTgonvXh81oqfXwCSWAyDPiTYFDWVfWM9C4ApxMLyc0XvJte75Rla+bPC08oYN3OlhbbvP3twBL/w9SsfxvkbpFn2ZfGSTXZhyiq4vjmQHW1pnFvGelwgU4v3eeRE/MjoCnE7M/Q5thpuog6WGf7CbKERnWZn8QsUaJsZSEkg6Bv2jm69ye57ab5rrOUaeMlstTfdlaHAEkUgLX/NXq7RbGwv82hkHY5b2vYcXeh34tUMBL6os3OdRlooN9ZQGkVIISvxVZpSHkYC20DFNh1Bb0ovjfujlTcka81GnbUhFGZtRuoVQ1RVpMO8xtx3YKBLp4do3hPmnRCV5hCm43OIjYx9Ov2dqICV3AaNXSLV1dW39Bak/RBiIDGHzOIW2+VMPjvvypBjmPv/tmbqNHWPSAWOxTyMx6E1gFCZvi+5F+BgkdC3Lm7U0BU0NfvsXajZd8sXnIllvEMrikCLoI/yurvexNDcF1RW/FhMsoua0eerwczcNm66pGjHm05p9DR6lFeJZrtqeqZuojdxBWy4vH6ghyJaupergoX+nmdG3JYeRttCFF/ITI68TeCES5V3Y0C3psYAg1XxcGRLGd4chPo/4xwiLkijWtgt0/to5ljGBwfK7r62PHZfL1Dp+i7V3w7hmOlhbXzP+zhMZn1GCk7KY=",
    #                 file_type=0,  # 0 para certificado, 1 para llave privada
    #                 password="12345678a"
    #             ),
    #             TaxCredential(
    #                 base64_file="MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAgEAAoIBAQACAggAMBQGCCqGSIb3DQMHBAgwggS9AgEAMASCBMh4EHl7aNSCaMDA1VlRoXCZ5UUmqErAbucRBAKNQXH8t8gVCl/ItHMI2hMJ76QOECOqEi1Y89cDpegDvh/INXyMsXbzi87tfFzgq1O+9ID6aPWGg+bNGADXyXxDVdy7Nq/SCdoXvo66MTYwq8jyJeUHDHEGMVBcmZpD44VJCvLBxDcvByuevP4Wo2NKqJCwK+ecAdZc/8Rvd947SjbMHuS8BppfQWARVUqA5BLOkTAHNv6tEk/hncC7O2YOGSShart8fM8dokgGSyewHVFe08POuQ+WDHeVpvApH/SP29rwktSoiHRoL6dK+F2YeEB5SuFW9LQgYCutjapmUP/9TC3Byro9Li6UrvQHxNmgMFGQJSYjFdqlGjLibfuguLp7pueutbROoZaSxU8HqlfYxLkpJUxUwNI1ja/1t3wcivtWknVXBd13R06iVfU1HGe8Kb4u5il4a4yP4p7VT4RE3b1SBLJeG+BxHiE8gFaaKcX/Cl6JV14RPTvk/6VnAtEQ66qHJex21KKuiJo2JoOmDXVHmvGQlWXNjYgoPx28Xd5WsofL+n7HDR2Ku8XgwJw6IXBJGuoday9qWN9v/k7DGlNGB6Sm4gdVUmycMP6EGhB1vFTiDfOGQO42ywmcpKoMETPVQ5InYKE0xAOckgcminDgxWjtUHjBDPEKifEjYudPwKmR6Cf4ZdGvUWwY/zq9pPAC9bu423KeBCnSL8AQ4r5SVsW6XG0njamwfNjpegwh/YG7sS7sDtZ8gi7r6tZYjsOqZlCYU0j7QTBpuQn81Yof2nQRCFxhRJCeydmIA8+z0nXrcElk7NDPk4kYQS0VitJ2qeQYNENzGBglROkCl2y6GlxAG80IBtReCUp/xOSdlwDR0eim+SNkdStvmQM5IcWBuDKwGZc1A4v/UoLl7niV9fpl4X6bUX8lZzY4gidJOafoJ30VoY/lYGkrkEuz3GpbbT5v8fF3iXVRlEqhlpe8JSGu7Rd2cPcJSkQ1Cuj/QRhHPhFMF2KhTEf95c9ZBKI8H7SvBi7eLXfSW2Y0ve6vXBZKyjK9whgCU9iVOsJjqRXpAccaWOKi420CjmS0+uwj/Xr2wLZhPEjBA/G6Od30+eG9mICmbp/5wAGhK/ZxCT17ZETyFmOMo49jl9pxdKocJNuzMrLpSz7/g5Jwp8+y8Ck5YP7AX0R/dVA0t37DO7nAbQT5XVSYpMVh/yvpYJ9WR+tb8Yg1h2lERLR2fbuhQRcwmisZR2W3Sr2b7hX9MCMkMQw8y2fDJrzLrqKqkHcjvnI/TdzZW2MzeQDoBBb3fmgvjYg07l4kThS73wGX992w2Y+a1A2iirSmrYEm9dSh16JmXa8boGQAONQzQkHh7vpw0IBs9cnvqO1QLB1GtbBztUBXonA4TxMKLYZkVrrd2RhrYWMsDp7MpC4M0p/DA3E/qscYwq1OpwriewNdx6XXqMZbdUNqMP2viBY2VSGmNdHtVfbN/rnaeJetFGX7XgTVYD7wDq8TW9yseCK944jcT+y/o0YiT9j3OLQ2Ts0LDTQskpJSxRmXEQGy3NBDOYFTvRkcGJEQJItuol8NivJN1H9LoLIUAlAHBZxfHpUYx66YnP4PdTdMIWH+nxyekKPFfAT7olQ=", 
    #                 file_type=1, # 0 para certificado, 1 para llave privada
    #                 password="12345678a"
    #             )
    #         ]
    #     ),
    #     recipient=InvoiceRecipient(
    #         tin="EKU9003173C9",
    #         legal_name="ESCUELA KEMPER URGATE",
    #         zip_code="42501",
    #         tax_regime_code="601",
    #         cfdi_use_code="G01",
    #         email="mail@domain.com"
    #     ),
    #     items=[
    #         InvoiceItem(
    #             item_code="01010101",
    #             quantity=Decimal(9.5),
    #             unit_of_measurement_code="E48",
    #             unit_of_measurement="Unidad de servicio",
    #             description="Invoicing software as a service",
    #             unit_price=Decimal("3587.75"),
    #             tax_object_code="02",
    #             item_sku="7506022301697",
    #             discount=Decimal("255.85"),
    #             item_taxes=[
    #                 ItemTax(
    #                     tax_code="002",
    #                     tax_type_code="Tasa",
    #                     tax_rate=Decimal("0.160000"),
    #                     tax_flag_code="T" #(T)raslado o (R)etencion
    #                 )
    #             ]
    #         )
    #     ]
    # )
        
    # api_response = client.invoices.create(invoice)
    # print(api_response)
    
    
    
    
    
    
    # Crear factura de ingreso por referencias (cURL). 
     
    # curl --location 'https://localhost:7173/api/v4/invoices/income' \
    # --header 'X-TENANT-KEY: e839651d-1765-4cd0-ba7f-547a4c20580f' \
    # --header 'X-TIME-ZONE: America/Mexico_City' \
    # --header 'Content-Type: application/json' \
    # --header 'X-API-KEY: sk_development_e0e47dfa_5146_40c2_b3a3_3055909a6b88' \
    # --data '{
    # "versionCode": "4.0",
    # "series": "F",
    # "date": "2025-02-11T16:29:58",
    # "paymentFormCode": "01",
    # "currencyCode": "MXN",
    # "typeCode": "I",
    # "expeditionZipCode": "42501",
    # "paymentMethodCode": "PUE",
    # "exchangeRate": 1,
    # "exportCode": "01",
    # "issuer": {
    #     "id": "3f3478b4-60fd-459e-8bfc-f8239fc96257"
    # },
    # "recipient": {
    #     "id": "96b46762-d246-4a67-a562-510a25dbafa9"
    # },
    # "items": [
    #     {
    #     "id": "114a4be5-fb65-40b2-a762-ff0c55c6ebfa",
    #     "quantity": 2,
    #     "discount": 255.85
    #     }
    # ]
    # }'

    
    # Crear factura de ingreso por referencias (Sdk).
    # invoice = Invoice(
    #     version_code="4.0",
    #     series="F",
    #     date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), #YYYY-MM-DDThh:mm:ss
    #     payment_form_code="01",
    #     payment_conditions="Contado",
    #     currency_code="MXN",
    #     type_code="I",
    #     expedition_zip_code="42501",
    #     payment_method_code="PUE",
    #     exchange_rate=1,
    #     export_code="01",
    #     issuer=InvoiceIssuer(
    #         id="3f3478b4-60fd-459e-8bfc-f8239fc96257"
    #     ),
    #     recipient=InvoiceRecipient(
    #         id="96b46762-d246-4a67-a562-510a25dbafa9"
    #     ),
    #     items=[
    #         InvoiceItem(
    #             id="114a4be5-fb65-40b2-a762-ff0c55c6ebfa",
    #             quantity=Decimal("1.5"),
    #             discount=Decimal("255.85")
    #         )
    #     ]
    # )
    
    # api_response = client.invoices.create(invoice)
    # print(api_response)
    
          
    
    
  
    
    # Crear nota de credito (factura de egreso) por valores (cURL).
    
    #  curl --location 'https://localhost:7173/api/v4/invoices/credit-note' \
    # --header 'X-TENANT-KEY: e839651d-1765-4cd0-ba7f-547a4c20580f' \
    # --header 'X-TIME-ZONE: America/Mexico_City' \
    # --header 'Content-Type: application/json' \
    # --header 'X-API-KEY: sk_development_e0e47dfa_5146_40c2_b3a3_3055909a6b88' \
    # --data-raw '{
    # "versionCode": "4.0",
    # "series": "CN",
    # "date": "2025-02-10T20:12:33",
    # "paymentFormCode": "03",
    # "paymentConditions": "Contado",
    # "currencyCode": "MXN",
    # "typeCode": "E",
    # "expeditionZipCode": "01160",
    # "paymentMethodCode": "PUE",
    # "exchangeRate": 1,
    # "exportCode": "01",
    # "issuer": {
    #     "tin": "FUNK671228PH6",
    #     "legalName": "KARLA FUENTE NOLASCO",
    #     "taxRegimeCode": "621",
    #     "taxCredentials": [
    #     {
    #         "base64File": "MIIFgDCCA2igAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0NDYwDQYJKoZIhvcNAQELBQAwggErMQ8wDQYDVQQDDAZBQyBVQVQxLjAsBgNVBAoMJVNFUlZJQ0lPIERFIEFETUlOSVNUUkFDSU9OIFRSSUJVVEFSSUExGjAYBgNVBAsMEVNBVC1JRVMgQXV0aG9yaXR5MSgwJgYJKoZIhvcNAQkBFhlvc2Nhci5tYXJ0aW5lekBzYXQuZ29iLm14MR0wGwYDVQQJDBQzcmEgY2VycmFkYSBkZSBjYWxpejEOMAwGA1UEEQwFMDYzNzAxCzAJBgNVBAYTAk1YMRkwFwYDVQQIDBBDSVVEQUQgREUgTUVYSUNPMREwDwYDVQQHDAhDT1lPQUNBTjERMA8GA1UELRMIMi41LjQuNDUxJTAjBgkqhkiG9w0BCQITFnJlc3BvbnNhYmxlOiBBQ0RNQS1TQVQwHhcNMjMwNTE4MTQzNTM3WhcNMjcwNTE4MTQzNTM3WjCBpzEdMBsGA1UEAxMUS0FSTEEgRlVFTlRFIE5PTEFTQ08xHTAbBgNVBCkTFEtBUkxBIEZVRU5URSBOT0xBU0NPMR0wGwYDVQQKExRLQVJMQSBGVUVOVEUgTk9MQVNDTzEWMBQGA1UELRMNRlVOSzY3MTIyOFBINjEbMBkGA1UEBRMSRlVOSzY3MTIyOE1DTE5MUjA1MRMwEQYDVQQLEwpTdWN1cnNhbCAxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhNXbTSqGX6+/3Urpemyy5vVG2IdP2v7v001+c4BoMxEDFDQ32cOFdDiRxy0Fq9aR+Ojrofq8VeftvN586iyA1A6a0QnA68i7JnQKI4uJy+u0qiixuHu6u3b3BhSpoaVHcUtqFWLLlzr0yBxfVLOqVna/1/tHbQJg9hx57mp97P0JmXO1WeIqi+Zqob/mVZh2lsPGdJ8iqgjYFaFn9QVOQ1Pq74o1PTqwfzqgJSfV0zOOlESDPWggaDAYE4VNyTBisOUjlNd0x7ppcTxSi3yenrJHqkq/pqJsRLKf6VJ/s9p6bsd2bj07hSDpjlDC2lB25eEfkEkeMkXoE7ErXQ5QCwIDAQABox0wGzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQsFAAOCAgEAHwYpgbClHULXYhK4GNTgonvXh81oqfXwCSWAyDPiTYFDWVfWM9C4ApxMLyc0XvJte75Rla+bPC08oYN3OlhbbvP3twBL/w9SsfxvkbpFn2ZfGSTXZhyiq4vjmQHW1pnFvGelwgU4v3eeRE/MjoCnE7M/Q5thpuog6WGf7CbKERnWZn8QsUaJsZSEkg6Bv2jm69ye57ab5rrOUaeMlstTfdlaHAEkUgLX/NXq7RbGwv82hkHY5b2vYcXeh34tUMBL6os3OdRlooN9ZQGkVIISvxVZpSHkYC20DFNh1Bb0ovjfujlTcka81GnbUhFGZtRuoVQ1RVpMO8xtx3YKBLp4do3hPmnRCV5hCm43OIjYx9Ov2dqICV3AaNXSLV1dW39Bak/RBiIDGHzOIW2+VMPjvvypBjmPv/tmbqNHWPSAWOxTyMx6E1gFCZvi+5F+BgkdC3Lm7U0BU0NfvsXajZd8sXnIllvEMrikCLoI/yurvexNDcF1RW/FhMsoua0eerwczcNm66pGjHm05p9DR6lFeJZrtqeqZuojdxBWy4vH6ghyJaupergoX+nmdG3JYeRttCFF/ITI68TeCES5V3Y0C3psYAg1XxcGRLGd4chPo/4xwiLkijWtgt0/to5ljGBwfK7r62PHZfL1Dp+i7V3w7hmOlhbXzP+zhMZn1GCk7KY=",
    #         "fileType": 0,
    #         "password": "12345678a"
    #     },
    #     {
    #         "base64File": "MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAgEAAoIBAQACAggAMBQGCCqGSIb3DQMHBAgwggS9AgEAMASCBMh4EHl7aNSCaMDA1VlRoXCZ5UUmqErAbucRBAKNQXH8t8gVCl/ItHMI2hMJ76QOECOqEi1Y89cDpegDvh/INXyMsXbzi87tfFzgq1O+9ID6aPWGg+bNGADXyXxDVdy7Nq/SCdoXvo66MTYwq8jyJeUHDHEGMVBcmZpD44VJCvLBxDcvByuevP4Wo2NKqJCwK+ecAdZc/8Rvd947SjbMHuS8BppfQWARVUqA5BLOkTAHNv6tEk/hncC7O2YOGSShart8fM8dokgGSyewHVFe08POuQ+WDHeVpvApH/SP29rwktSoiHRoL6dK+F2YeEB5SuFW9LQgYCutjapmUP/9TC3Byro9Li6UrvQHxNmgMFGQJSYjFdqlGjLibfuguLp7pueutbROoZaSxU8HqlfYxLkpJUxUwNI1ja/1t3wcivtWknVXBd13R06iVfU1HGe8Kb4u5il4a4yP4p7VT4RE3b1SBLJeG+BxHiE8gFaaKcX/Cl6JV14RPTvk/6VnAtEQ66qHJex21KKuiJo2JoOmDXVHmvGQlWXNjYgoPx28Xd5WsofL+n7HDR2Ku8XgwJw6IXBJGuoday9qWN9v/k7DGlNGB6Sm4gdVUmycMP6EGhB1vFTiDfOGQO42ywmcpKoMETPVQ5InYKE0xAOckgcminDgxWjtUHjBDPEKifEjYudPwKmR6Cf4ZdGvUWwY/zq9pPAC9bu423KeBCnSL8AQ4r5SVsW6XG0njamwfNjpegwh/YG7sS7sDtZ8gi7r6tZYjsOqZlCYU0j7QTBpuQn81Yof2nQRCFxhRJCeydmIA8+z0nXrcElk7NDPk4kYQS0VitJ2qeQYNENzGBglROkCl2y6GlxAG80IBtReCUp/xOSdlwDR0eim+SNkdStvmQM5IcWBuDKwGZc1A4v/UoLl7niV9fpl4X6bUX8lZzY4gidJOafoJ30VoY/lYGkrkEuz3GpbbT5v8fF3iXVRlEqhlpe8JSGu7Rd2cPcJSkQ1Cuj/QRhHPhFMF2KhTEf95c9ZBKI8H7SvBi7eLXfSW2Y0ve6vXBZKyjK9whgCU9iVOsJjqRXpAccaWOKi420CjmS0+uwj/Xr2wLZhPEjBA/G6Od30+eG9mICmbp/5wAGhK/ZxCT17ZETyFmOMo49jl9pxdKocJNuzMrLpSz7/g5Jwp8+y8Ck5YP7AX0R/dVA0t37DO7nAbQT5XVSYpMVh/yvpYJ9WR+tb8Yg1h2lERLR2fbuhQRcwmisZR2W3Sr2b7hX9MCMkMQw8y2fDJrzLrqKqkHcjvnI/TdzZW2MzeQDoBBb3fmgvjYg07l4kThS73wGX992w2Y+a1A2iirSmrYEm9dSh16JmXa8boGQAONQzQkHh7vpw0IBs9cnvqO1QLB1GtbBztUBXonA4TxMKLYZkVrrd2RhrYWMsDp7MpC4M0p/DA3E/qscYwq1OpwriewNdx6XXqMZbdUNqMP2viBY2VSGmNdHtVfbN/rnaeJetFGX7XgTVYD7wDq8TW9yseCK944jcT+y/o0YiT9j3OLQ2Ts0LDTQskpJSxRmXEQGy3NBDOYFTvRkcGJEQJItuol8NivJN1H9LoLIUAlAHBZxfHpUYx66YnP4PdTdMIWH+nxyekKPFfAT7olQ=",
    #         "fileType": 1,
    #         "password": "12345678a"
    #     }
    #     ]
    # },
    # "recipient": {
    #     "tin": "EKU9003173C9",
    #     "legalName": "ESCUELA KEMPER URGATE",
    #     "zipCode": "42501",
    #     "taxRegimeCode": "601",
    #     "cfdiUseCode": "G01",
    #     "email": "someone@somewhere.com"
    # },
    # "relatedInvoices": [
    #     {
    #     "uuid": "5FB2822E-396D-4725-8521-CDC4BDD20CCF",
    #     "relationshipTypeCode": "01"
    #     }
    # ],
    # "items": [
    #     {
    #     "itemCode": "01010101",
    #     "quantity": 0.5,
    #     "unitOfMeasurementCode": "E48",
    #     "description": "Invoicing software as a service",
    #     "unitPrice": 3587.75,
    #     "taxObjectCode": "02",
    #     "itemSku": "7506022301697",
    #     "itemTaxes": [
    #         {
    #         "taxCode": "002",
    #         "taxTypeCode": "Tasa",
    #         "taxRate": 0.160000,
    #         "TaxFlagCode": "T"
    #         }
    #     ]
    #     }
    # ]
    # }'
    
    # Crear nota de credito (factura de egreso) por valores (Sdk).
    # credit_note = Invoice(
    #     version_code="4.0",
    #     series="CN",
    #     date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), #YYYY-MM-DDThh:mm:ss
    #     payment_form_code="03",
    #     currency_code="MXN",
    #     type_code="E",
    #     expedition_zip_code="01160",
    #     payment_method_code="PUE",
    #     exchange_rate=1,
    #     export_code="01",
    #      issuer=InvoiceIssuer(
    #         tin="FUNK671228PH6",
    #         legal_name="KARLA FUENTE NOLASCO",
    #         tax_regime_code="621",
    #         tax_credentials= [
    #             TaxCredential(
    #                 base64_file="MIIFgDCCA2igAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0NDYwDQYJKoZIhvcNAQELBQAwggErMQ8wDQYDVQQDDAZBQyBVQVQxLjAsBgNVBAoMJVNFUlZJQ0lPIERFIEFETUlOSVNUUkFDSU9OIFRSSUJVVEFSSUExGjAYBgNVBAsMEVNBVC1JRVMgQXV0aG9yaXR5MSgwJgYJKoZIhvcNAQkBFhlvc2Nhci5tYXJ0aW5lekBzYXQuZ29iLm14MR0wGwYDVQQJDBQzcmEgY2VycmFkYSBkZSBjYWxpejEOMAwGA1UEEQwFMDYzNzAxCzAJBgNVBAYTAk1YMRkwFwYDVQQIDBBDSVVEQUQgREUgTUVYSUNPMREwDwYDVQQHDAhDT1lPQUNBTjERMA8GA1UELRMIMi41LjQuNDUxJTAjBgkqhkiG9w0BCQITFnJlc3BvbnNhYmxlOiBBQ0RNQS1TQVQwHhcNMjMwNTE4MTQzNTM3WhcNMjcwNTE4MTQzNTM3WjCBpzEdMBsGA1UEAxMUS0FSTEEgRlVFTlRFIE5PTEFTQ08xHTAbBgNVBCkTFEtBUkxBIEZVRU5URSBOT0xBU0NPMR0wGwYDVQQKExRLQVJMQSBGVUVOVEUgTk9MQVNDTzEWMBQGA1UELRMNRlVOSzY3MTIyOFBINjEbMBkGA1UEBRMSRlVOSzY3MTIyOE1DTE5MUjA1MRMwEQYDVQQLEwpTdWN1cnNhbCAxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhNXbTSqGX6+/3Urpemyy5vVG2IdP2v7v001+c4BoMxEDFDQ32cOFdDiRxy0Fq9aR+Ojrofq8VeftvN586iyA1A6a0QnA68i7JnQKI4uJy+u0qiixuHu6u3b3BhSpoaVHcUtqFWLLlzr0yBxfVLOqVna/1/tHbQJg9hx57mp97P0JmXO1WeIqi+Zqob/mVZh2lsPGdJ8iqgjYFaFn9QVOQ1Pq74o1PTqwfzqgJSfV0zOOlESDPWggaDAYE4VNyTBisOUjlNd0x7ppcTxSi3yenrJHqkq/pqJsRLKf6VJ/s9p6bsd2bj07hSDpjlDC2lB25eEfkEkeMkXoE7ErXQ5QCwIDAQABox0wGzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQsFAAOCAgEAHwYpgbClHULXYhK4GNTgonvXh81oqfXwCSWAyDPiTYFDWVfWM9C4ApxMLyc0XvJte75Rla+bPC08oYN3OlhbbvP3twBL/w9SsfxvkbpFn2ZfGSTXZhyiq4vjmQHW1pnFvGelwgU4v3eeRE/MjoCnE7M/Q5thpuog6WGf7CbKERnWZn8QsUaJsZSEkg6Bv2jm69ye57ab5rrOUaeMlstTfdlaHAEkUgLX/NXq7RbGwv82hkHY5b2vYcXeh34tUMBL6os3OdRlooN9ZQGkVIISvxVZpSHkYC20DFNh1Bb0ovjfujlTcka81GnbUhFGZtRuoVQ1RVpMO8xtx3YKBLp4do3hPmnRCV5hCm43OIjYx9Ov2dqICV3AaNXSLV1dW39Bak/RBiIDGHzOIW2+VMPjvvypBjmPv/tmbqNHWPSAWOxTyMx6E1gFCZvi+5F+BgkdC3Lm7U0BU0NfvsXajZd8sXnIllvEMrikCLoI/yurvexNDcF1RW/FhMsoua0eerwczcNm66pGjHm05p9DR6lFeJZrtqeqZuojdxBWy4vH6ghyJaupergoX+nmdG3JYeRttCFF/ITI68TeCES5V3Y0C3psYAg1XxcGRLGd4chPo/4xwiLkijWtgt0/to5ljGBwfK7r62PHZfL1Dp+i7V3w7hmOlhbXzP+zhMZn1GCk7KY=",
    #                 file_type=0,  # 0 para certificado, 1 para llave privada
    #                 password="12345678a"
    #             ),
    #             TaxCredential(
    #                 base64_file="MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAgEAAoIBAQACAggAMBQGCCqGSIb3DQMHBAgwggS9AgEAMASCBMh4EHl7aNSCaMDA1VlRoXCZ5UUmqErAbucRBAKNQXH8t8gVCl/ItHMI2hMJ76QOECOqEi1Y89cDpegDvh/INXyMsXbzi87tfFzgq1O+9ID6aPWGg+bNGADXyXxDVdy7Nq/SCdoXvo66MTYwq8jyJeUHDHEGMVBcmZpD44VJCvLBxDcvByuevP4Wo2NKqJCwK+ecAdZc/8Rvd947SjbMHuS8BppfQWARVUqA5BLOkTAHNv6tEk/hncC7O2YOGSShart8fM8dokgGSyewHVFe08POuQ+WDHeVpvApH/SP29rwktSoiHRoL6dK+F2YeEB5SuFW9LQgYCutjapmUP/9TC3Byro9Li6UrvQHxNmgMFGQJSYjFdqlGjLibfuguLp7pueutbROoZaSxU8HqlfYxLkpJUxUwNI1ja/1t3wcivtWknVXBd13R06iVfU1HGe8Kb4u5il4a4yP4p7VT4RE3b1SBLJeG+BxHiE8gFaaKcX/Cl6JV14RPTvk/6VnAtEQ66qHJex21KKuiJo2JoOmDXVHmvGQlWXNjYgoPx28Xd5WsofL+n7HDR2Ku8XgwJw6IXBJGuoday9qWN9v/k7DGlNGB6Sm4gdVUmycMP6EGhB1vFTiDfOGQO42ywmcpKoMETPVQ5InYKE0xAOckgcminDgxWjtUHjBDPEKifEjYudPwKmR6Cf4ZdGvUWwY/zq9pPAC9bu423KeBCnSL8AQ4r5SVsW6XG0njamwfNjpegwh/YG7sS7sDtZ8gi7r6tZYjsOqZlCYU0j7QTBpuQn81Yof2nQRCFxhRJCeydmIA8+z0nXrcElk7NDPk4kYQS0VitJ2qeQYNENzGBglROkCl2y6GlxAG80IBtReCUp/xOSdlwDR0eim+SNkdStvmQM5IcWBuDKwGZc1A4v/UoLl7niV9fpl4X6bUX8lZzY4gidJOafoJ30VoY/lYGkrkEuz3GpbbT5v8fF3iXVRlEqhlpe8JSGu7Rd2cPcJSkQ1Cuj/QRhHPhFMF2KhTEf95c9ZBKI8H7SvBi7eLXfSW2Y0ve6vXBZKyjK9whgCU9iVOsJjqRXpAccaWOKi420CjmS0+uwj/Xr2wLZhPEjBA/G6Od30+eG9mICmbp/5wAGhK/ZxCT17ZETyFmOMo49jl9pxdKocJNuzMrLpSz7/g5Jwp8+y8Ck5YP7AX0R/dVA0t37DO7nAbQT5XVSYpMVh/yvpYJ9WR+tb8Yg1h2lERLR2fbuhQRcwmisZR2W3Sr2b7hX9MCMkMQw8y2fDJrzLrqKqkHcjvnI/TdzZW2MzeQDoBBb3fmgvjYg07l4kThS73wGX992w2Y+a1A2iirSmrYEm9dSh16JmXa8boGQAONQzQkHh7vpw0IBs9cnvqO1QLB1GtbBztUBXonA4TxMKLYZkVrrd2RhrYWMsDp7MpC4M0p/DA3E/qscYwq1OpwriewNdx6XXqMZbdUNqMP2viBY2VSGmNdHtVfbN/rnaeJetFGX7XgTVYD7wDq8TW9yseCK944jcT+y/o0YiT9j3OLQ2Ts0LDTQskpJSxRmXEQGy3NBDOYFTvRkcGJEQJItuol8NivJN1H9LoLIUAlAHBZxfHpUYx66YnP4PdTdMIWH+nxyekKPFfAT7olQ=", 
    #                 file_type=1, # 0 para certificado, 1 para llave privada
    #                 password="12345678a"
    #             )
    #         ]
    #     ),
    #     recipient=InvoiceRecipient(
    #         tin="EKU9003173C9",
    #         legal_name="ESCUELA KEMPER URGATE",
    #         zip_code="42501",
    #         tax_regime_code="601",
    #         cfdi_use_code="G01",
    #         email="mail@domain.com"
    #     ),
    #     related_invoices=[
    #         RelatedInvoice(
    #             uuid="5FB2822E-396D-4725-8521-CDC4BDD20CCF", # UUID de la factura relacionada
    #             relationship_type_code="01" # 01 para nota de credito
    #         )
    #     ],
    #     items=[
    #         InvoiceItem(
    #             item_code="01010101",
    #             quantity=Decimal("0.5"),
    #             unit_of_measurement_code="E48",
    #             description="Invoicing software as a service",
    #             unit_price=Decimal("3587.75"),
    #             tax_object_code="02",
    #             item_sku="7506022301697",
    #             item_taxes=[
    #                 ItemTax(
    #                     tax_code="002",
    #                     tax_type_code="Tasa",
    #                     tax_rate=Decimal("0.160000"),
    #                     tax_flag_code="T" #(T)raslado o (R)etencion
    #                 )
    #             ]
    #         )
    #     ]
    # )
    
    # api_response = client.invoices.create(credit_note)
    # print(api_response)
        

   # Crear nota de credito (factura de egreso) por referencias (cURL).
    #   curl --location 'https://localhost:7173/api/v4/invoices/credit-note' \
    # --header 'X-TENANT-KEY: e839651d-1765-4cd0-ba7f-547a4c20580f' \
    # --header 'X-TIME-ZONE: America/Mexico_City' \
    # --header 'Content-Type: application/json' \
    # --header 'X-API-KEY: sk_development_e0e47dfa_5146_40c2_b3a3_3055909a6b88' \
    # --data '{
    #   "versionCode": "4.0",
    #   "series": "CN",
    #   "date": "2025-02-11T16:44:11",
    #   "paymentFormCode": "03",
    #   "currencyCode": "MXN",
    #   "typeCode": "E",
    #   "expeditionZipCode": "01160",
    #   "paymentMethodCode": "PUE",
    #   "exchangeRate": 1,
    #   "exportCode": "01",
    #   "issuer": {
    #     "id": "3f3478b4-60fd-459e-8bfc-f8239fc96257"
    #   },
    #   "recipient": {
    #     "id": "96b46762-d246-4a67-a562-510a25dbafa9"
    #   },
    #   "relatedInvoices": [
    #     {
    #       "uuid": "5FB2822E-396D-4725-8521-CDC4BDD20CCF",
    #       "relationshipTypeCode": "01"
    #     }
    #   ],
    #   "items": [
    #     {
    #       "id": "114a4be5-fb65-40b2-a762-ff0c55c6ebfa",
    #        "quantity": 0.5
    #     }
    #   ]
    # }'
   
    # Crear nota de credito (factura de egreso) por referencias (Sdk).
    
    # credit_note = Invoice(
    #     version_code="4.0",
    #     series="CN",
    #     date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), #YYYY-MM-DDThh:mm:ss
    #     payment_form_code="03",
    #     payment_conditions="Contado",
    #     currency_code="MXN",
    #     type_code="E",
    #     expedition_zip_code="01160",
    #     payment_method_code="PUE",
    #     exchange_rate=1,
    #     export_code="01",
    #     issuer=InvoiceIssuer(
    #         id="3f3478b4-60fd-459e-8bfc-f8239fc96257"
    #     ),
    #     recipient=InvoiceRecipient(
    #         id="96b46762-d246-4a67-a562-510a25dbafa9"
    #     ),
    #     related_invoices=[
    #         RelatedInvoice(
    #             uuid="5FB2822E-396D-4725-8521-CDC4BDD20CCF",
    #             relationship_type_code="01"
    #         )
    #     ],
    #     items=[
    #         InvoiceItem(
    #             id="114a4be5-fb65-40b2-a762-ff0c55c6ebfa",
    #             quantity=Decimal("0.5")
    #         )
    #     ]
    # )
    
    # api_response = client.invoices.create(credit_note)
    # print(api_response)
    
    
    # Crear complemento pago (factura de pago) por valores (cURL).
    
    #   curl --location 'https://localhost:7173/api/v4/invoices/payment' \
    # --header 'X-TENANT-KEY: e839651d-1765-4cd0-ba7f-547a4c20580f' \
    # --header 'X-TIME-ZONE: America/Mexico_City' \
    # --header 'Content-Type: application/json' \
    # --header 'X-API-KEY: sk_development_e0e47dfa_5146_40c2_b3a3_3055909a6b88' \
    # --data-raw '{
    # "versionCode": "4.0",
    # "series": "CP",
    # "date": "2025-02-11T16:16:29",
    # "currencyCode": "XXX",
    # "typeCode": "P",
    # "expeditionZipCode": "01160",
    # "exchangeRate": 1,
    # "exportCode": "01",
    # "issuer": {
    #     "tin": "FUNK671228PH6",
    #     "legalName": "KARLA FUENTE NOLASCO",
    #     "taxRegimeCode": "621",
    #     "taxCredentials": [
    #     {
    #         "base64File": "MIIFgDCCA2igAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0NDYwDQYJKoZIhvcNAQELBQAwggErMQ8wDQYDVQQDDAZBQyBVQVQxLjAsBgNVBAoMJVNFUlZJQ0lPIERFIEFETUlOSVNUUkFDSU9OIFRSSUJVVEFSSUExGjAYBgNVBAsMEVNBVC1JRVMgQXV0aG9yaXR5MSgwJgYJKoZIhvcNAQkBFhlvc2Nhci5tYXJ0aW5lekBzYXQuZ29iLm14MR0wGwYDVQQJDBQzcmEgY2VycmFkYSBkZSBjYWxpejEOMAwGA1UEEQwFMDYzNzAxCzAJBgNVBAYTAk1YMRkwFwYDVQQIDBBDSVVEQUQgREUgTUVYSUNPMREwDwYDVQQHDAhDT1lPQUNBTjERMA8GA1UELRMIMi41LjQuNDUxJTAjBgkqhkiG9w0BCQITFnJlc3BvbnNhYmxlOiBBQ0RNQS1TQVQwHhcNMjMwNTE4MTQzNTM3WhcNMjcwNTE4MTQzNTM3WjCBpzEdMBsGA1UEAxMUS0FSTEEgRlVFTlRFIE5PTEFTQ08xHTAbBgNVBCkTFEtBUkxBIEZVRU5URSBOT0xBU0NPMR0wGwYDVQQKExRLQVJMQSBGVUVOVEUgTk9MQVNDTzEWMBQGA1UELRMNRlVOSzY3MTIyOFBINjEbMBkGA1UEBRMSRlVOSzY3MTIyOE1DTE5MUjA1MRMwEQYDVQQLEwpTdWN1cnNhbCAxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhNXbTSqGX6+/3Urpemyy5vVG2IdP2v7v001+c4BoMxEDFDQ32cOFdDiRxy0Fq9aR+Ojrofq8VeftvN586iyA1A6a0QnA68i7JnQKI4uJy+u0qiixuHu6u3b3BhSpoaVHcUtqFWLLlzr0yBxfVLOqVna/1/tHbQJg9hx57mp97P0JmXO1WeIqi+Zqob/mVZh2lsPGdJ8iqgjYFaFn9QVOQ1Pq74o1PTqwfzqgJSfV0zOOlESDPWggaDAYE4VNyTBisOUjlNd0x7ppcTxSi3yenrJHqkq/pqJsRLKf6VJ/s9p6bsd2bj07hSDpjlDC2lB25eEfkEkeMkXoE7ErXQ5QCwIDAQABox0wGzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQsFAAOCAgEAHwYpgbClHULXYhK4GNTgonvXh81oqfXwCSWAyDPiTYFDWVfWM9C4ApxMLyc0XvJte75Rla+bPC08oYN3OlhbbvP3twBL/w9SsfxvkbpFn2ZfGSTXZhyiq4vjmQHW1pnFvGelwgU4v3eeRE/MjoCnE7M/Q5thpuog6WGf7CbKERnWZn8QsUaJsZSEkg6Bv2jm69ye57ab5rrOUaeMlstTfdlaHAEkUgLX/NXq7RbGwv82hkHY5b2vYcXeh34tUMBL6os3OdRlooN9ZQGkVIISvxVZpSHkYC20DFNh1Bb0ovjfujlTcka81GnbUhFGZtRuoVQ1RVpMO8xtx3YKBLp4do3hPmnRCV5hCm43OIjYx9Ov2dqICV3AaNXSLV1dW39Bak/RBiIDGHzOIW2+VMPjvvypBjmPv/tmbqNHWPSAWOxTyMx6E1gFCZvi+5F+BgkdC3Lm7U0BU0NfvsXajZd8sXnIllvEMrikCLoI/yurvexNDcF1RW/FhMsoua0eerwczcNm66pGjHm05p9DR6lFeJZrtqeqZuojdxBWy4vH6ghyJaupergoX+nmdG3JYeRttCFF/ITI68TeCES5V3Y0C3psYAg1XxcGRLGd4chPo/4xwiLkijWtgt0/to5ljGBwfK7r62PHZfL1Dp+i7V3w7hmOlhbXzP+zhMZn1GCk7KY=",
    #         "fileType": 0,
    #         "password": "12345678a"
    #     },
    #     {
    #         "base64File": "MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAgEAAoIBAQACAggAMBQGCCqGSIb3DQMHBAgwggS9AgEAMASCBMh4EHl7aNSCaMDA1VlRoXCZ5UUmqErAbucRBAKNQXH8t8gVCl/ItHMI2hMJ76QOECOqEi1Y89cDpegDvh/INXyMsXbzi87tfFzgq1O+9ID6aPWGg+bNGADXyXxDVdy7Nq/SCdoXvo66MTYwq8jyJeUHDHEGMVBcmZpD44VJCvLBxDcvByuevP4Wo2NKqJCwK+ecAdZc/8Rvd947SjbMHuS8BppfQWARVUqA5BLOkTAHNv6tEk/hncC7O2YOGSShart8fM8dokgGSyewHVFe08POuQ+WDHeVpvApH/SP29rwktSoiHRoL6dK+F2YeEB5SuFW9LQgYCutjapmUP/9TC3Byro9Li6UrvQHxNmgMFGQJSYjFdqlGjLibfuguLp7pueutbROoZaSxU8HqlfYxLkpJUxUwNI1ja/1t3wcivtWknVXBd13R06iVfU1HGe8Kb4u5il4a4yP4p7VT4RE3b1SBLJeG+BxHiE8gFaaKcX/Cl6JV14RPTvk/6VnAtEQ66qHJex21KKuiJo2JoOmDXVHmvGQlWXNjYgoPx28Xd5WsofL+n7HDR2Ku8XgwJw6IXBJGuoday9qWN9v/k7DGlNGB6Sm4gdVUmycMP6EGhB1vFTiDfOGQO42ywmcpKoMETPVQ5InYKE0xAOckgcminDgxWjtUHjBDPEKifEjYudPwKmR6Cf4ZdGvUWwY/zq9pPAC9bu423KeBCnSL8AQ4r5SVsW6XG0njamwfNjpegwh/YG7sS7sDtZ8gi7r6tZYjsOqZlCYU0j7QTBpuQn81Yof2nQRCFxhRJCeydmIA8+z0nXrcElk7NDPk4kYQS0VitJ2qeQYNENzGBglROkCl2y6GlxAG80IBtReCUp/xOSdlwDR0eim+SNkdStvmQM5IcWBuDKwGZc1A4v/UoLl7niV9fpl4X6bUX8lZzY4gidJOafoJ30VoY/lYGkrkEuz3GpbbT5v8fF3iXVRlEqhlpe8JSGu7Rd2cPcJSkQ1Cuj/QRhHPhFMF2KhTEf95c9ZBKI8H7SvBi7eLXfSW2Y0ve6vXBZKyjK9whgCU9iVOsJjqRXpAccaWOKi420CjmS0+uwj/Xr2wLZhPEjBA/G6Od30+eG9mICmbp/5wAGhK/ZxCT17ZETyFmOMo49jl9pxdKocJNuzMrLpSz7/g5Jwp8+y8Ck5YP7AX0R/dVA0t37DO7nAbQT5XVSYpMVh/yvpYJ9WR+tb8Yg1h2lERLR2fbuhQRcwmisZR2W3Sr2b7hX9MCMkMQw8y2fDJrzLrqKqkHcjvnI/TdzZW2MzeQDoBBb3fmgvjYg07l4kThS73wGX992w2Y+a1A2iirSmrYEm9dSh16JmXa8boGQAONQzQkHh7vpw0IBs9cnvqO1QLB1GtbBztUBXonA4TxMKLYZkVrrd2RhrYWMsDp7MpC4M0p/DA3E/qscYwq1OpwriewNdx6XXqMZbdUNqMP2viBY2VSGmNdHtVfbN/rnaeJetFGX7XgTVYD7wDq8TW9yseCK944jcT+y/o0YiT9j3OLQ2Ts0LDTQskpJSxRmXEQGy3NBDOYFTvRkcGJEQJItuol8NivJN1H9LoLIUAlAHBZxfHpUYx66YnP4PdTdMIWH+nxyekKPFfAT7olQ=",
    #         "fileType": 1,
    #         "password": "12345678a"
    #     }
    #     ]
    # },
    # "recipient": {
    #     "tin": "EKU9003173C9",
    #     "legalName": "ESCUELA KEMPER URGATE",
    #     "zipCode": "42501",
    #     "taxRegimeCode": "601",
    #     "cfdiUseCode": "CP01",
    #     "email": "someone@somewhere.com"
    # },
    # "items": [
    #     {
    #     "itemCode": "84111506",
    #     "quantity": 1,
    #     "unitOfMeasurementCode": "ACT",
    #     "description": "Pago",
    #     "unitPrice": 0,
    #     "taxObjectCode": "01"
    #     }
    # ],
    # "payments": [
    #     {
    #     "paymentDate": "2024-06-03T14:44:56",
    #     "paymentFormCode": "28",
    #     "currencyCode": "MXN",
    #     "exchangeRate": 1,
    #     "amount": 28599.99,
    #     "sourceBankTin": "BSM970519DU8",
    #     "sourceBankAccount": "1234567891012131",
    #     "targetBankTin": "BBA830831LJ2",
    #     "targetBankAccount": "1234567890",
    #     "paidInvoices": [
    #         {
    #         "uuid": "5C7B0622-01B4-4EB8-96D0-E0DEBD89FF0F",
    #         "series": "F",
    #         "number": "1501",
    #         "currencyCode": "MXN",
    #         "partialityNumber": 1,
    #         "subTotal": 10000,
    #         "previousBalance": 9533.33,
    #         "paymentAmount": 9533.33,
    #         "remainingBalance": 0,
    #         "taxObjectCode": "02",
    #         "paidInvoiceTaxes": [
    #             {
    #             "taxCode": "002",
    #             "taxTypeCode": "Tasa",
    #             "taxRate": 0.160000,
    #             "taxFlagCode": "T"
    #             }
    #         ]
    #         }
    #     ]
    #     }
    # ]
    # }'
    
    
    # Crear complemento pago (factura de pago) por valores (Sdk).
    
    # payment_invoice = Invoice(
    #     version_code="4.0",
    #     series="CP",
    #     date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), #YYYY-MM-DDThh:mm:ss
    #     currency_code="XXX",
    #     type_code="P",
    #     expedition_zip_code="01160",
    #     exchange_rate=1,
    #     export_code="01",
    #     issuer=InvoiceIssuer(
    #         tin="FUNK671228PH6",
    #         legal_name="KARLA FUENTE NOLASCO",
    #         tax_regime_code="621",
    #         tax_credentials= [
    #             TaxCredential(
    #                 base64_file="MIIFgDCCA2igAwIBAgIUMzAwMDEwMDAwMDA1MDAwMDM0NDYwDQYJKoZIhvcNAQELBQAwggErMQ8wDQYDVQQDDAZBQyBVQVQxLjAsBgNVBAoMJVNFUlZJQ0lPIERFIEFETUlOSVNUUkFDSU9OIFRSSUJVVEFSSUExGjAYBgNVBAsMEVNBVC1JRVMgQXV0aG9yaXR5MSgwJgYJKoZIhvcNAQkBFhlvc2Nhci5tYXJ0aW5lekBzYXQuZ29iLm14MR0wGwYDVQQJDBQzcmEgY2VycmFkYSBkZSBjYWxpejEOMAwGA1UEEQwFMDYzNzAxCzAJBgNVBAYTAk1YMRkwFwYDVQQIDBBDSVVEQUQgREUgTUVYSUNPMREwDwYDVQQHDAhDT1lPQUNBTjERMA8GA1UELRMIMi41LjQuNDUxJTAjBgkqhkiG9w0BCQITFnJlc3BvbnNhYmxlOiBBQ0RNQS1TQVQwHhcNMjMwNTE4MTQzNTM3WhcNMjcwNTE4MTQzNTM3WjCBpzEdMBsGA1UEAxMUS0FSTEEgRlVFTlRFIE5PTEFTQ08xHTAbBgNVBCkTFEtBUkxBIEZVRU5URSBOT0xBU0NPMR0wGwYDVQQKExRLQVJMQSBGVUVOVEUgTk9MQVNDTzEWMBQGA1UELRMNRlVOSzY3MTIyOFBINjEbMBkGA1UEBRMSRlVOSzY3MTIyOE1DTE5MUjA1MRMwEQYDVQQLEwpTdWN1cnNhbCAxMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAhNXbTSqGX6+/3Urpemyy5vVG2IdP2v7v001+c4BoMxEDFDQ32cOFdDiRxy0Fq9aR+Ojrofq8VeftvN586iyA1A6a0QnA68i7JnQKI4uJy+u0qiixuHu6u3b3BhSpoaVHcUtqFWLLlzr0yBxfVLOqVna/1/tHbQJg9hx57mp97P0JmXO1WeIqi+Zqob/mVZh2lsPGdJ8iqgjYFaFn9QVOQ1Pq74o1PTqwfzqgJSfV0zOOlESDPWggaDAYE4VNyTBisOUjlNd0x7ppcTxSi3yenrJHqkq/pqJsRLKf6VJ/s9p6bsd2bj07hSDpjlDC2lB25eEfkEkeMkXoE7ErXQ5QCwIDAQABox0wGzAMBgNVHRMBAf8EAjAAMAsGA1UdDwQEAwIGwDANBgkqhkiG9w0BAQsFAAOCAgEAHwYpgbClHULXYhK4GNTgonvXh81oqfXwCSWAyDPiTYFDWVfWM9C4ApxMLyc0XvJte75Rla+bPC08oYN3OlhbbvP3twBL/w9SsfxvkbpFn2ZfGSTXZhyiq4vjmQHW1pnFvGelwgU4v3eeRE/MjoCnE7M/Q5thpuog6WGf7CbKERnWZn8QsUaJsZSEkg6Bv2jm69ye57ab5rrOUaeMlstTfdlaHAEkUgLX/NXq7RbGwv82hkHY5b2vYcXeh34tUMBL6os3OdRlooN9ZQGkVIISvxVZpSHkYC20DFNh1Bb0ovjfujlTcka81GnbUhFGZtRuoVQ1RVpMO8xtx3YKBLp4do3hPmnRCV5hCm43OIjYx9Ov2dqICV3AaNXSLV1dW39Bak/RBiIDGHzOIW2+VMPjvvypBjmPv/tmbqNHWPSAWOxTyMx6E1gFCZvi+5F+BgkdC3Lm7U0BU0NfvsXajZd8sXnIllvEMrikCLoI/yurvexNDcF1RW/FhMsoua0eerwczcNm66pGjHm05p9DR6lFeJZrtqeqZuojdxBWy4vH6ghyJaupergoX+nmdG3JYeRttCFF/ITI68TeCES5V3Y0C3psYAg1XxcGRLGd4chPo/4xwiLkijWtgt0/to5ljGBwfK7r62PHZfL1Dp+i7V3w7hmOlhbXzP+zhMZn1GCk7KY=",
    #                 file_type=0,  # 0 para certificado, 1 para llave privada
    #                 password="12345678a"
    #             ),
    #             TaxCredential(
    #                 base64_file="MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAgEAAoIBAQACAggAMBQGCCqGSIb3DQMHBAgwggS9AgEAMASCBMh4EHl7aNSCaMDA1VlRoXCZ5UUmqErAbucRBAKNQXH8t8gVCl/ItHMI2hMJ76QOECOqEi1Y89cDpegDvh/INXyMsXbzi87tfFzgq1O+9ID6aPWGg+bNGADXyXxDVdy7Nq/SCdoXvo66MTYwq8jyJeUHDHEGMVBcmZpD44VJCvLBxDcvByuevP4Wo2NKqJCwK+ecAdZc/8Rvd947SjbMHuS8BppfQWARVUqA5BLOkTAHNv6tEk/hncC7O2YOGSShart8fM8dokgGSyewHVFe08POuQ+WDHeVpvApH/SP29rwktSoiHRoL6dK+F2YeEB5SuFW9LQgYCutjapmUP/9TC3Byro9Li6UrvQHxNmgMFGQJSYjFdqlGjLibfuguLp7pueutbROoZaSxU8HqlfYxLkpJUxUwNI1ja/1t3wcivtWknVXBd13R06iVfU1HGe8Kb4u5il4a4yP4p7VT4RE3b1SBLJeG+BxHiE8gFaaKcX/Cl6JV14RPTvk/6VnAtEQ66qHJex21KKuiJo2JoOmDXVHmvGQlWXNjYgoPx28Xd5WsofL+n7HDR2Ku8XgwJw6IXBJGuoday9qWN9v/k7DGlNGB6Sm4gdVUmycMP6EGhB1vFTiDfOGQO42ywmcpKoMETPVQ5InYKE0xAOckgcminDgxWjtUHjBDPEKifEjYudPwKmR6Cf4ZdGvUWwY/zq9pPAC9bu423KeBCnSL8AQ4r5SVsW6XG0njamwfNjpegwh/YG7sS7sDtZ8gi7r6tZYjsOqZlCYU0j7QTBpuQn81Yof2nQRCFxhRJCeydmIA8+z0nXrcElk7NDPk4kYQS0VitJ2qeQYNENzGBglROkCl2y6GlxAG80IBtReCUp/xOSdlwDR0eim+SNkdStvmQM5IcWBuDKwGZc1A4v/UoLl7niV9fpl4X6bUX8lZzY4gidJOafoJ30VoY/lYGkrkEuz3GpbbT5v8fF3iXVRlEqhlpe8JSGu7Rd2cPcJSkQ1Cuj/QRhHPhFMF2KhTEf95c9ZBKI8H7SvBi7eLXfSW2Y0ve6vXBZKyjK9whgCU9iVOsJjqRXpAccaWOKi420CjmS0+uwj/Xr2wLZhPEjBA/G6Od30+eG9mICmbp/5wAGhK/ZxCT17ZETyFmOMo49jl9pxdKocJNuzMrLpSz7/g5Jwp8+y8Ck5YP7AX0R/dVA0t37DO7nAbQT5XVSYpMVh/yvpYJ9WR+tb8Yg1h2lERLR2fbuhQRcwmisZR2W3Sr2b7hX9MCMkMQw8y2fDJrzLrqKqkHcjvnI/TdzZW2MzeQDoBBb3fmgvjYg07l4kThS73wGX992w2Y+a1A2iirSmrYEm9dSh16JmXa8boGQAONQzQkHh7vpw0IBs9cnvqO1QLB1GtbBztUBXonA4TxMKLYZkVrrd2RhrYWMsDp7MpC4M0p/DA3E/qscYwq1OpwriewNdx6XXqMZbdUNqMP2viBY2VSGmNdHtVfbN/rnaeJetFGX7XgTVYD7wDq8TW9yseCK944jcT+y/o0YiT9j3OLQ2Ts0LDTQskpJSxRmXEQGy3NBDOYFTvRkcGJEQJItuol8NivJN1H9LoLIUAlAHBZxfHpUYx66YnP4PdTdMIWH+nxyekKPFfAT7olQ=", 
    #                 file_type=1, # 0 para certificado, 1 para llave privada
    #                 password="12345678a"
    #             )
    #         ]
    #     ),
    #     recipient=InvoiceRecipient(
    #         tin="EKU9003173C9",
    #         legal_name="ESCUELA KEMPER URGATE",
    #         zip_code="42501",
    #         tax_regime_code="601",
    #         cfdi_use_code="CP01",
    #         email="mail@domain.com",
    #     ),
    #     items=[
    #         InvoiceItem(
    #             item_code="84111506",
    #             quantity=1,
    #             unit_of_measurement_code="ACT",
    #             description="Pago",
    #             unit_price=0,
    #             tax_object_code="01"
    #         )
    #     ],
    #     # pagos recibidos
    #     payments=[
    #         InvoicePayment(
    #             payment_date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    #             payment_form_code="28",
    #             currency_code="MXN",
    #             exchange_rate=1,
    #             amount=Decimal("11600.00"),
    #             source_bank_tin="BSM970519DU8",
    #             source_bank_account="1234567891012131",
    #             target_bank_tin="BBA830831LJ2",
    #             target_bank_account="1234567890",
    #             paid_invoices=[ # facturas pagadas con el pago recibido
    #                 PaidInvoice(
    #                     uuid="5C7B0622-01B4-4EB8-96D0-E0DEBD89FF0F",
    #                     series="F",
    #                     number="123",
    #                     currency_code="MXN",
    #                     partiality_number=1,
    #                     sub_total=Decimal("10000.00"),
    #                     previous_balance=Decimal("11600.00"),
    #                     payment_amount=Decimal("11600.00"),
    #                     remaining_balance=0,
    #                     tax_object_code="02",
    #                     paid_invoice_taxes=[
    #                         PaidInvoiceTax(
    #                             tax_code="002",
    #                             tax_type_code="Tasa",
    #                             tax_rate=Decimal("0.160000"),
    #                             tax_flag_code="T"
    #                         )
    #                     ]
    #                 )
    #             ]
    #         )
    #     ]
        
    # )
    
    # api_response = client.invoices.create(payment_invoice)
    
    # print(api_response)
    
    
    # Crear complemento pago (factura de pago) por referencias (cURL).
    
    #   curl --location 'https://localhost:7173/api/v4/invoices/payment' \
    # --header 'X-TENANT-KEY: e839651d-1765-4cd0-ba7f-547a4c20580f' \
    # --header 'X-TIME-ZONE: America/Mexico_City' \
    # --header 'Content-Type: application/json' \
    # --header 'X-API-KEY: sk_development_e0e47dfa_5146_40c2_b3a3_3055909a6b88' \
    # --data '{
    #   "versionCode": "4.0",
    #   "series": "CP",
    #   "date": "2025-02-11T16:16:29",
    #   "currencyCode": "XXX",
    #   "typeCode": "P",
    #   "expeditionZipCode": "01160",
    #   "exchangeRate": 1,
    #   "exportCode": "01",
    #  "issuer": {
    #     "id": "3f3478b4-60fd-459e-8bfc-f8239fc96257"
    #   },
    #   "recipient": {
    #     "id": "96b46762-d246-4a67-a562-510a25dbafa9"
    #   },
    #   "payments": [
    #     {
    #       "paymentDate": "2024-06-03T14:44:56",
    #       "paymentFormCode": "28",
    #       "currencyCode": "MXN",
    #       "exchangeRate": 1,
    #       "amount": 11600.00,
    #       "sourceBankTin": "BSM970519DU8",
    #       "sourceBankAccount": "1234567891012131",
    #       "targetBankTin": "BBA830831LJ2",
    #       "targetBankAccount": "1234567890",
    #       "paidInvoices": [
    #         {
    #           "uuid": "5C7B0622-01B4-4EB8-96D0-E0DEBD89FF0F",
    #           "series": "F",
    #           "number": "1501",
    #           "currencyCode": "MXN",
    #           "partialityNumber": 1,
    #           "subTotal": 10000,
    #           "previousBalance": 11600.00,
    #           "paymentAmount": 11600.00,
    #           "remainingBalance": 0,
    #           "taxObjectCode": "02",
    #           "paidInvoiceTaxes": [
    #             {
    #               "taxCode": "002",
    #               "taxTypeCode": "Tasa",
    #               "taxRate": 0.160000,
    #               "taxFlagCode": "T"
    #             }
    #           ]
    #         }
    #       ]
    #     }
    #   ]
    # }'
    
    
    # Crear complemento pago (factura de pago) por referencias (Sdk).
    
    # payment_invoice = Invoice(
    #     version_code="4.0",
    #     series="CP",
    #     date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), #YYYY-MM-DDThh:mm:ss
    #     currency_code="XXX",
    #     type_code="P",
    #     expedition_zip_code="01160",
    #     exchange_rate=1,
    #     export_code="01",
    #     issuer=InvoiceIssuer(
    #         id="3f3478b4-60fd-459e-8bfc-f8239fc96257" # id del emisor
    #     ),
    #     recipient=InvoiceRecipient(
    #         id="96b46762-d246-4a67-a562-510a25dbafa9" # id del receptor
    #     ),
        
    #     # sin conceptos (items)
      
    #     # pagos recibidos
    #     payments=[
    #         InvoicePayment(
    #             payment_date=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    #             payment_form_code="28",
    #             currency_code="MXN",
    #             exchange_rate=1,
    #             amount=Decimal("11600.00"),
    #             source_bank_tin="BSM970519DU8",
    #             source_bank_account="1234567891012131",
    #             target_bank_tin="BBA830831LJ2",
    #             target_bank_account="1234567890",
    #             paid_invoices=[ # facturas pagadas con el pago recibido
    #                 PaidInvoice(
    #                     uuid="5C7B0622-01B4-4EB8-96D0-E0DEBD89FF0F",
    #                     series="F",
    #                     number="123",
    #                     currency_code="MXN",
    #                     partiality_number=1,
    #                     sub_total=Decimal("10000.00"),
    #                     previous_balance=Decimal("11600.00"),
    #                     payment_amount=Decimal("11600.00"),
    #                     remaining_balance=0,
    #                     tax_object_code="02",
    #                     paid_invoice_taxes=[
    #                         PaidInvoiceTax(
    #                             tax_code="002",
    #                             tax_type_code="Tasa",
    #                             tax_rate=Decimal("0.160000"),
    #                             tax_flag_code="T"
    #                         )
    #                     ]
    #                 )
    #             ]
    #         )
    #     ]
    # )
    
    # api_response = client.invoices.create(payment_invoice)
    
    # print(api_response)
    
if __name__ == "__main__":
    main()
    
    
if __name__ == "__main__":
    main()