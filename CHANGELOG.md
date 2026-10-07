# Changelog

Cambios del SDK y notas de comportamiento del API de FiscalAPI que afectan a quien usa el SDK.

## [Sin publicar]

### Cambios incompatibles (BREAKING)

- Se elimina `Person.capital_regime` (estaba deprecado): el API no tiene régimen de capital, ignoraba el valor y nunca lo devolvía. Quite `capital_regime=...` de los `Person(...)` que construya y toda lectura de `person.capital_regime` (ahora lanza `AttributeError`); envíe la razón social sin régimen de capital en `legal_name`. Pasarlo al constructor no lanza error, pero se descarta sin enviarse.
- `TaxCredential` deja de heredar de `BaseDto`: solo tiene `base64_file`, `file_type` y `password` (opcional en el .cer). Quite `id=...`, `created_at=...` y `updated_at=...` de los `TaxCredential(...)` que construya (se descartan sin enviarse) y toda lectura de esos atributos (ahora lanza `AttributeError`). Un código que trate un `TaxCredential` como `BaseDto` (por ejemplo `isinstance(cred, BaseDto)`) ya no lo reconoce.

### Modelo `Person`

- Nuevos campos opcionales:
  - `phone_number` (`phoneNumber`): lo aceptan la creación y la actualización de personas.
  - `balances`: saldos por tipo de crédito (`CreditBalance`: `credit_type` y `available`, solo lectura). Solo aparecen los tipos que la persona ha tenido; un tipo ausente tiene saldo 0, y un tipo que el SDK no conoce conserva su número.
  - `is_owner` (`isOwner`): `True` si la persona es el owner de su tenant (solo lectura).
  - `country`: país de residencia fiscal expandido (solo lectura).
- `password`: requerida al crear; al actualizar, `None` o vacía conserva la contraseña actual. El API nunca la devuelve.
- `user_type_id`: `"C"` (cliente, el valor por omisión al crear) o `"U"` (usuario). `"T"` (tenant) solo llega en respuestas: el API lo rechaza al crear y al actualizar solo lo acepta si la persona ya es `"T"`.

### `TaxCredential`

- `password` deja de ser obligatorio en el modelo: el API solo lo exige en la llave privada (.key, `file_type=1`); en el certificado (.cer) no lo usa.

### Notas del API (sin cambio de forma en el SDK)

- `Person.tax_password` es la contraseña de la llave privada (.key) que la persona guarda en su perfil; el API no la usa para sellar (al timbrar usa la contraseña de los certificados registrados o la de `tax_credentials`). Solo la reciben con valor la propia persona y el owner del tenant; los demás reciben `None`. Al actualizar, `None` la conserva (el SDK no envía los `None`) y `""` la borra.
- `ValidationFailure.attempted_value`: en un 400 de validación, el valor de un secreto (contraseñas, códigos, tokens, archivos y contraseñas de CSD/FIEL) llega enmascarado como `"[masked: n]"` (`n` es su longitud), o `"[masked]"` si la falla es de un objeto o una lista que lo contiene.
- El API ya no devuelve `twoFactorEnabled` en las personas (este SDK nunca lo modeló).
- `TaxFile.tin` es opcional en `tax_files.create()`: si se omite (`None` o vacío), el API usa el RFC de la persona. Si se envía, debe ser el RFC de la persona (sin distinguir mayúsculas); si no, el API responde 400 con la falla en `Tin` (después de comprobar que puede gestionar los certificados de la persona; si no, 403). El API no guarda el valor enviado: el `tin` del archivo siempre es el RFC de la persona.
