// ===========================================================================
// Generado automáticamente por el Compilador de Sopito++ (sopitoc)
// Fuente original: 02_suma.spp
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
    std::cout << "Calculando 6 + 7 en Sopito++...\n";
    // [77676] PRINT_STR (Línea 6)
    std::cout << "Resultado: ";
    // [66667] PUSH (Línea 7)
    stack.push_back(6LL);
    // [66667] PUSH (Línea 8)
    stack.push_back(7LL);
    // [66776] ADD (Línea 9)
    { int64_t a = pop(); if (!stack.empty()) stack.back() += a; }
    // [77666] PRINT_NUM (Línea 10)
    std::cout << pop();
    // [77677] PRINT_NL (Línea 11)
    std::cout << '\n';
    // [66666] HALT (Línea 12)
    return 0;

    return 0;
}
