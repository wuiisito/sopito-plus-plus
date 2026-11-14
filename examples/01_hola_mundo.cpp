// ===========================================================================
// Generado automáticamente por el Compilador de Sopito++ (sopitoc)
// Fuente original: 01_hola_mundo.spp
// Dialecto: Sopito++ (6 = bit 0, 7 = bit 1)
// ===========================================================================
#include <iostream>
#include <vector>
#include <unordered_map>
#include <cstdint>
#include <string>

// Estructura de Ejecución de Sopito++
int main() {
    // Pila de datos principal (enteros de 64 bits)
    std::vector<int64_t> stack;
    stack.reserve(1024);

    // Memoria direccionable (celdas de variables globales)
    std::unordered_map<int64_t, int64_t> memory;

    // Pila de llamadas para subrutinas (CALL / RET)
    std::vector<int> call_stack;
    call_stack.reserve(64);

    // Funciones auxiliares inline para seguridad de pila
    auto pop = [&]() -> int64_t {
        if (stack.empty()) return 0;
        int64_t val = stack.back();
        stack.pop_back();
        return val;
    };

    auto top = [&]() -> int64_t {
        return stack.empty() ? 0 : stack.back();
    };

    // --- Instrucciones Traducidas ---
    // [77676] PRINT_STR (Línea 5)
    std::cout << "¡Hola desde Sopito++! (Donde 6 es 0 y 7 es 1)\n";
    // [66666] HALT (Línea 6)
    return 0;

    return 0;
}
