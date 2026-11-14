Instalación y Primeros Pasos
=============================

Requisitos Previos
------------------

Para utilizar Sopito++, únicamente requieres:
- **Python 3.8 o superior** (probado en Python 3.10, 3.12 y 3.14).
- *(Opcional)* Un compilador de C++ como **g++**, **clang++** o **MSVC (cl)** si deseas generar binarios ejecutables nativos (``.exe`` o ELF).

Clonar el Repositorio
---------------------

Puedes clonar el repositorio oficial desde GitHub:

.. code-block:: bash

   git clone https://github.com/tu-usuario/sopito.git
   cd sopito

Estructura de Archivos
----------------------

.. code-block:: text

   sopito++/
   ├── sopitoc.py           # Compilador principal, VM, ensamblador y CLI
   ├── sopito.bat           # Acceso directo para Windows
   ├── SPECIFICATION.md     # Especificación formal
   ├── README.md            # Guía rápida
   ├── LICENSE              # Licencia MIT
   ├── .readthedocs.yaml    # Configuración de Read the Docs
   ├── docs/                # Documentación en Sphinx
   ├── examples/            # Programas de ejemplo (.spp y .sasm)
   └── tests/               # Pruebas unitarias

Uso de la Línea de Comandos (CLI)
---------------------------------

El script principal es ``sopitoc.py`` (o ``sopito.bat`` en Windows). Puedes consultar la ayuda completa con:

.. code-block:: bash

   python sopitoc.py --help

Comandos principales:

* **compile**: Compila un archivo a código C++:

  .. code-block:: bash

     python sopitoc.py compile examples/01_hola_mundo.spp -o hola.cpp

* **run**: Ejecuta el programa en la máquina virtual:

  .. code-block:: bash

     python sopitoc.py run examples/01_hola_mundo.spp

* **assemble**: Convierte mnemónicos legibles (``.sasm``) a código binario puro de 6s y 7s (``.spp``):

  .. code-block:: bash

     python sopitoc.py assemble examples/02_suma.sasm -o suma.spp

* **disasm**: Desensambla un archivo binario a texto legible:

  .. code-block:: bash

     python sopitoc.py disasm examples/02_suma.spp

* **repl**: Inicia la sesión interactiva:

  .. code-block:: bash

     python sopitoc.py repl

* **encode / decode**: Herramientas auxiliares de conversión:

  .. code-block:: bash

     python sopitoc.py encode 42 --num
     python sopitoc.py decode 767676 --num
