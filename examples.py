from fiscalapi.models.common_models import FiscalApiSettings
from fiscalapi.models.fiscalapi_models import Product, ProductTax, Person, TaxFile
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
    api_response = client.catalogs.search_catalog("SatPaymentForms", "tarjeta")
    
    print(api_response)
    
    
if __name__ == "__main__":
    main()