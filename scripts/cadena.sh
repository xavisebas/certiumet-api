#!/usr/bin/env bash
# Ejecuta la cadena CASE completa y guarda la salida de cada herramienta en docs/evidencias/.
# Uso (desde la raíz del repositorio, con el entorno virtual activo):  bash scripts/cadena.sh
set -u
EVID=docs/evidencias
mkdir -p "$EVID"
fecha() { date "+%Y-%m-%d %H:%M:%S"; }
paso() { echo; echo "=== $1 ($(fecha)) ==="; }

paso "1. Criterios del 07 = archivos .feature (T01, T02)"
{ python scripts/extraer_features.py --check && echo "Los 5 archivos .feature coinciden con el 07."; } 2>&1 | tee "$EVID/01-features.txt"

paso "2. Contrato OpenAPI con Spectral (T04)"
{ spectral --version; spectral lint api/openapi.yaml -F hint; echo "codigo de salida: $?"; } 2>&1 | tee "$EVID/02-spectral.txt"

paso "3. Documentación HTML desde el contrato (T05)"
{ openapi-generator-cli version; openapi-generator-cli generate -i api/openapi.yaml -g html2 -o docs/api > /dev/null 2>&1; echo "codigo de salida: $?"; ls -l docs/api/index.html; } 2>&1 | tee "$EVID/03-documentacion.txt"

paso "4. Stubs desde el contrato (T06)"
{ openapi-generator-cli generate -i api/openapi.yaml -g python-fastapi -o api/stubs/python-fastapi \
    --additional-properties=packageName=certiumet_stubs > /dev/null 2>&1; echo "codigo de salida: $?"
  echo "Archivos Python generados: $(find api/stubs/python-fastapi -name '*.py' | wc -l)"
  ls api/stubs/python-fastapi/src/certiumet_stubs/apis; } 2>&1 | tee "$EVID/04-stubs.txt"

paso "4b. Servidor simulado (mock) con Prism (T05)"
{
  prism --version
  prism mock api/openapi.yaml -p 4010 > /tmp/prism-certiumet.log 2>&1 &
  PRISM=$!
  sleep 8
  T="Authorization: Bearer token-de-prueba"; J="Content-Type: application/json"
  echo "POST /solicitudes (válido):";  curl -s -X POST localhost:4010/api/v1/solicitudes -H "$T" -H "$J" -d '{"tipoCertificado":"MATRICULA"}' -w "  [HTTP %{http_code}]\n"
  echo "POST /solicitudes (tipo no válido):"; curl -s -X POST localhost:4010/api/v1/solicitudes -H "$T" -H "$J" -d '{"tipoCertificado":"OTRO"}' -w "  [HTTP %{http_code}]\n"
  echo "GET /solicitudes/1 sin token:"; curl -s localhost:4010/api/v1/solicitudes/1 -w "  [HTTP %{http_code}]\n"
  echo "PATCH /resolucion (segunda aprobación, 409):"; curl -s -X PATCH localhost:4010/api/v1/solicitudes/1/resolucion -H "$T" -H "$J" -H "Prefer: code=409" -d '{"decision":"APROBAR"}' -w "  [HTTP %{http_code}]\n"
  echo "GET /verificaciones/{codigo} (público):"; curl -s localhost:4010/api/v1/verificaciones/7-3f9a1c2b7d4e8f60a1b2 -w "  [HTTP %{http_code}]\n"
  kill $PRISM
} 2>&1 | tee "$EVID/04b-prism-mock.txt"

paso "5. Linter del código (T08)"
{ ruff --version; ruff check .; echo "codigo de salida: $?"; } 2>&1 | tee "$EVID/05-ruff.txt"

paso "6. Reglas de dependencia entre módulos (T08, ADR-003)"
(cd src && lint-imports --config ../.importlinter) 2>&1 | tail -n 8 | tee "$EVID/06-import-linter.txt"

paso "7. Pruebas derivadas de los criterios (T07)"
{ echo "Base de datos: ${POSTGRES_DB:-SQLite (sin PostgreSQL)}"; python -m pytest -v -s -p no:cacheprovider; } 2>&1 | tee "$EVID/07-pruebas.txt"

paso "8. Matriz: Spectral y Redocly sobre el contrato con defectos sembrados"
{ spectral lint api/pruebas/openapi-con-defectos.yaml -F hint; echo "codigo de salida: $?"; } 2>&1 | tee "$EVID/08-matriz-spectral.txt"
{ redocly --version; redocly lint api/pruebas/openapi-con-defectos.yaml --format stylish; echo "codigo de salida: $?"; } 2>&1 | tee "$EVID/09-matriz-redocly.txt"

echo; echo "Listo. Las salidas quedaron en $EVID/"
