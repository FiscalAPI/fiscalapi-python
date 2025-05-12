# setup.py
import os
from setuptools import setup, find_packages

VERSION = "4.0.150"
# Descripción breve basada en el .csproj
DESCRIPTION = "Genera facturas CFDI válidas ante el SAT consumiendo el API de https://www.fiscalapi.com"

# Carga un README.md (si existe) como descripción larga
current_dir = os.path.abspath(os.path.dirname(__file__))
long_description_file = os.path.join(current_dir, "README.md")
if os.path.exists(long_description_file):
    with open(long_description_file, encoding="utf-8") as f:
        LONG_DESCRIPTION = f.read()
else:
    LONG_DESCRIPTION = DESCRIPTION  # fallback si no se encuentra README.md

setup(
    name="fiscalapi",  # Normalmente en minúsculas en PyPI
    version=VERSION,
    author="Fiscalapi",
    author_email="contacto@fiscalapi.com",  # Ajusta con el correo que corresponda
    url="https://www.fiscalapi.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    
    # Licencia Pública de Mozilla (por ejemplo, MPL 2.0)
    license="MPL-2.0",
    
    packages=find_packages(
        exclude=["tests", "*.tests", "*.tests.*", "tests.*"]
    ),
    keywords=["factura", "cfdi", "facturacion", "mexico", "sat", "fiscalapi"],
    
    python_requires=">=3.7",  # Ajusta según la compatibilidad mínima de Python
    
    install_requires=[
        "pydantic>=2.0.0",
        "requests>=2.0.0",
        "urllib3>=1.0.0",
        "certifi>=2023.0.0",
        "email_validator>=2.2.0",
    ],
    
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python :: 3.7",
        "Topic :: Office/Business :: Financial",
    ],
)
