# Guía para Contribuir a Sopito++ 🚀

¡Gracias por tu interés en colaborar con **Sopito++**!

## Cómo Empezar

1. Haz un **Fork** de este repositorio en GitHub.
2. Clona tu fork localmente:
   ```bash
   git clone https://github.com/tu-usuario/sopito.git
   cd sopito
   ```
3. Crea una rama para tu aporte:
   ```bash
   git checkout -b feature/mi-nueva-caracteristica
   ```

## Pruebas y Calidad de Código

Antes de enviar un Pull Request, asegúrate de que todos los tests pasen:

```bash
# Ejecutar suite de pruebas unitarias
python tests/test_sopito.py

# Verificar que la documentación compila sin errores ni warnings
python -m sphinx -W -b html docs docs/_build/html
```

## Estilo de Código

* Sigue **PEP 8** para el código Python en `sopitoc.py`.
* Mantén las instrucciones de Sopito++ estrictamente basadas en números de 5 bits usando `6` (para 0) y `7` (para 1).
* Comenta con claridad cualquier adición a la especificación en `SPECIFICATION.md` y `docs/especificacion.rst`.

## Enviar tu Pull Request

1. Realiza commits claros y descriptivos.
2. Sube la rama a tu fork:
   ```bash
   git push origin feature/mi-nueva-caracteristica
   ```
3. Abre un **Pull Request** en GitHub detallando tu propuesta.
