Cómo Contribuir a Sopito++
===========================

¡Nos encanta recibir contribuciones de la comunidad!

Directrices
-----------

1. **Haz un Fork** del repositorio en GitHub.
2. **Crea una rama** para tu funcionalidad o corrección:
   
   .. code-block:: bash

      git checkout -b feature/nueva-instruccion

3. **Escribe pruebas unitarias** en ``tests/test_sopito.py`` para asegurar que todo funcione sin regresiones.
4. **Ejecuta la suite de pruebas**:

   .. code-block:: bash

      python tests/test_sopito.py

5. **Construye la documentación**:

   .. code-block:: bash

      python -m sphinx -b html docs docs/_build/html

6. **Envía un Pull Request** detallando tus cambios.
