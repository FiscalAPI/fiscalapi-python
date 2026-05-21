"""
Ejemplo: firma de carta manifiesto vía POST /api/v4/manifests usando el SDK de FiscalAPI.

El endpoint recibe el certificado (.cer) y la llave privada (.key) de la FIEL (e.firma)
del contribuyente en base64, además de la contraseña de la llave. Devuelve el PDF de la
carta manifiesto firmada (también en base64).

Importante: usar FIEL, NO CSD. El payload es idéntico al de tax-files, pero el endpoint
requiere los archivos de la e.firma del SAT (no los del CSD de timbrado).
"""
from fiscalapi import FiscalApiClient, FiscalApiSettings
from fiscalapi.models import SignManifestRequest


# Configuración de FiscalAPI
settings = FiscalApiSettings(
    api_url="https://test.fiscalapi.com",
    api_key="API_KEY",
    tenant="TENANT_ID"
)

# Credenciales FIEL de prueba (ESCUELA KEMPER URGATE)
escuela_kemper_urgate_base64_cer_fiel = "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";
escuela_kemper_urgate_base64_key_fiel = "MIIFDjBABgkqhkiG9w0BBQ0wMzAbBgkqhkiG9w0BBQwwDgQIAgEAAoIBAQACAggAMBQGCCqGSIb3DQMHBAgwggS9AgEAMASCBMh4EHl7aNSCaMDA1VlRoXCZ5UUmqErAbucRBAKNQXH8t0f2aSYkk74BKjNDtQ2u5LylXUf6MrOHJZV3J/U8IVU02MuKmvSb5kIvEKE3FZ/OSKoZC58sLQ/+m1joBEHn2QgMld3NsSRA6rv5Jv7Gyl8URb3XT6W7qr/nznufyuxyBSTj68+HgdJt/EeGp3Ud1Sk/1mY8PEt7tT86UjH+20/07ZVIhik6fQDFxELrm4jCJkTrQenqEykHVy/w5mJgrqwfS4SsGaNY9J5TUJNauyw193y/6C48SxwpTjA2GYtpxIUl9GNtXbUHUvsbVTZ06gnnCXUx3IOj+wFI9qUvPYl2DVSfV3iVAYsTXG/R5gOIw4k6s235gZEfJpoQZ4eq1LiYbKXqTjR9ntCEit0RyWirwt/2UcrRNgnXFU58xYUzY45noSR6QD8u05ZGsGT1Q3xesanSxCmsjrfh26a5EoH3voFhpI99/M2CyhwIm63ab2CKz8DMrhCPWxUgKDn2xZgW79zBgQ6qN0t9iqJ69guwG4rkWNqs/5vyYdK5PbJSt9KmeHZNYl1/wBMP4PDomA0iHiRQ2Jpc7tdedQXPid3DSIrk9XqMwB6SBThGOSzJ4Tkb78ybsHTjx3apF4ZHH6U66WzRbjggt2H0XmCbKLvNbAPqfA+vZzpIZK0LrsUGvG/wtoqFedZ/AV3wBvQTIRkwHImvFqoDd7fMCg8MLV3yJJGNcgcsI1RSV0EAJ5YafNHR9IPNl6pI7X6RDT7jobeyelyE5xepJklnNCIGLkYTGmXgXG0cYxtWYqvT7jQuEeseFSlxScxbvWI1vTzRpuis2YiZYteX4f+kGnMq6eOw+qtqXwB2bsw48ZGC9Ar34znqX/iOogQD+I2zWfllEdhQWdBF11m5YmwfnfQyoOOhx5s2bdqWv+XN6BMtRxfG7UOvB0p9ki1FdGOBD9BsSaF0etF8HPmy9zHPugCRQH50eVbqNnxPAnyaucPR/8ZEJXVuQ99KkhZRwr5brR9WP6ooDnws+yMe3q95hVVXWd4zDWPuh2JcT4ZzVzm9iwB7EZDYYCq/UXTg07Bb8hL0pw7UJFDelNMr4HOsarJZyUZferGQ62Ki7d/9xGOF4aL/lmni5okXU+fUKWkT7UhJCcxr3zeCnbe5FTNZgjIbieAMPtJiS30ow1EtxUsQF32f14lDdsi8twTT0GsILvZwNvGk/KZRlQU2iLm4hr44w6gmyg1J7m5ivL/MwbQ/DIf4djcOqckWBqtLCAp/HwSYjIXxrlPF1pICnzbfxTc6gLyTOsvoCngSnP2feOMTMMpFXVC1h0mfObxOhcbwxCC18AnNqfxh5rCvNxKYi0yqa5g9UFBOOKyxrhvP/eMdnPpd1DtvzP79zMQCQ+NlXt/XtmDRNUpPc7nPwhdPbRJTsetDqZK9NQf6cZ4/2cDIMd1/QomTmzKU9cjNXZgMcDSY7UYrN+n8CrETwu9dgNDuYjynh4XYlm0x9/Rx5r+77d1nzE6rkBH17/lH3fb8p4MWDlr6HIIgXxYCmeAhiws8tthJoD/nk1n6fvrxTFrEmEE1XG7JrNrDP1dLnjH+paHXy0thdQ8lpBMM4Wtqk0KVPn2SyaY3dslkdHg=";
password = "12345678a"


# ============================================================================
# 1. FIRMA DE CARTA MANIFIESTO (ESCUELA KEMPER URGATE)
# ============================================================================
def firma_carta_manifiesto(client: FiscalApiClient) -> None:
    request = SignManifestRequest(
        base64_cer=escuela_kemper_urgate_base64_cer_fiel,
        base64_key=escuela_kemper_urgate_base64_key_fiel,
        password=password,
    )
    response = client.manifests.sign(request)
    print("Response:", response)


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================
def main() -> None:
    client = FiscalApiClient(settings=settings)
    try:
        
        firma_carta_manifiesto(client)
        pass
    except Exception as error:
        print("Error:", error)


if __name__ == "__main__":
    main()
