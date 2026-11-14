#!/usr/bin/env python3
"""
SOPITO++ (sopito++) - Compilador, Ensamblador, Desensamblador y Máquina Virtual

Lenguaje de programación basado en el sistema binario donde:
    '6' representa el bit 0
    '7' representa el bit 1

Sopito++ puede compilar código fuente (.spp o .sasm) directamente a C++ moderno.
"""

import sys
import os
import argparse
import subprocess
from typing import List, Tuple, Dict, Any, Optional

# --- Definición del Conjunto de Instrucciones (ISA) ---
# Cada instrucción tiene un opcode fijo de 5 dígitos en Sopito++ (5 bits: 00000 a 11111)

OPCODE_TABLE = {
    0:  {"mnemonic": "HALT",       "sopito": "66666", "args": 0, "desc": "Termina la ejecución"},
    1:  {"mnemonic": "PUSH",       "sopito": "66667", "args": 1, "desc": "Empuja un entero a la pila"},
    2:  {"mnemonic": "POP",        "sopito": "66676", "args": 0, "desc": "Descarta el tope de la pila"},
    3:  {"mnemonic": "DUP",        "sopito": "66677", "args": 0, "desc": "Duplica el valor en el tope"},
    4:  {"mnemonic": "SWAP",       "sopito": "66766", "args": 0, "desc": "Intercambia los dos elementos del tope"},
    5:  {"mnemonic": "OVER",       "sopito": "66767", "args": 0, "desc": "Copia el segundo elemento al tope"},
    6:  {"mnemonic": "ADD",        "sopito": "66776", "args": 0, "desc": "Suma los dos valores del tope (b + a)"},
    7:  {"mnemonic": "SUB",        "sopito": "66777", "args": 0, "desc": "Resta los dos valores del tope (b - a)"},
    8:  {"mnemonic": "MUL",        "sopito": "67666", "args": 0, "desc": "Multiplica los dos valores del tope (b * a)"},
    9:  {"mnemonic": "DIV",        "sopito": "67667", "args": 0, "desc": "División entera (b / a)"},
    10: {"mnemonic": "MOD",        "sopito": "67676", "args": 0, "desc": "Módulo / residuo (b % a)"},
    11: {"mnemonic": "NEG",        "sopito": "67677", "args": 0, "desc": "Invierte el signo del tope (-a)"},
    12: {"mnemonic": "EQ",         "sopito": "67766", "args": 0, "desc": "Compara igualdad: 1 si b == a, sino 0"},
    13: {"mnemonic": "LT",         "sopito": "67767", "args": 0, "desc": "Menor que: 1 si b < a, sino 0"},
    14: {"mnemonic": "GT",         "sopito": "67776", "args": 0, "desc": "Mayor que: 1 si b > a, sino 0"},
    15: {"mnemonic": "NOT",        "sopito": "67777", "args": 0, "desc": "Negación lógica: 1 si a == 0, sino 0"},
    16: {"mnemonic": "AND",        "sopito": "76666", "args": 0, "desc": "AND a nivel de bits"},
    17: {"mnemonic": "OR",         "sopito": "76667", "args": 0, "desc": "OR a nivel de bits"},
    18: {"mnemonic": "LABEL",      "sopito": "76676", "args": 1, "desc": "Define una etiqueta (ID numérico)"},
    19: {"mnemonic": "JMP",        "sopito": "76677", "args": 1, "desc": "Salto incondicional a una etiqueta"},
    20: {"mnemonic": "JZ",         "sopito": "76766", "args": 1, "desc": "Salto a etiqueta si el tope es cero (pop)"},
    21: {"mnemonic": "JNZ",        "sopito": "76767", "args": 1, "desc": "Salto si el tope no es cero (pop)"},
    22: {"mnemonic": "STORE",      "sopito": "76776", "args": 1, "desc": "Guarda tope en la celda de memoria ID"},
    23: {"mnemonic": "LOAD",       "sopito": "76777", "args": 1, "desc": "Carga celda de memoria ID al tope"},
    24: {"mnemonic": "PRINT_NUM",  "sopito": "77666", "args": 0, "desc": "Imprime el entero del tope"},
    25: {"mnemonic": "PRINT_CHAR", "sopito": "77667", "args": 0, "desc": "Imprime el entero del tope como carácter ASCII"},
    26: {"mnemonic": "PRINT_STR",  "sopito": "77676", "args": -1, "desc": "Imprime cadena fija de bytes 6/7"},
    27: {"mnemonic": "PRINT_NL",   "sopito": "77677", "args": 0, "desc": "Imprime un salto de línea (\\n)"},
    28: {"mnemonic": "READ_NUM",   "sopito": "77766", "args": 0, "desc": "Lee un entero de la entrada estándar"},
    29: {"mnemonic": "READ_CHAR",  "sopito": "77767", "args": 0, "desc": "Lee un carácter de la entrada estándar"},
    30: {"mnemonic": "CALL",       "sopito": "77776", "args": 1, "desc": "Llama a la subrutina en la etiqueta ID"},
    31: {"mnemonic": "RET",        "sopito": "77777", "args": 0, "desc": "Retorna de la subrutina actual"},
}

MNEMONIC_TO_OPCODE = {v["mnemonic"]: k for k, v in OPCODE_TABLE.items()}
SOPITO_TO_OPCODE = {v["sopito"]: k for k, v in OPCODE_TABLE.items()}


# --- Funciones de Conversión Numérica y Binaria ---

def sopito_to_binary_str(s: str) -> str:
    """Convierte caracteres de Sopito++ ('6' y '7') a binario estándar ('0' y '1')."""
    return "".join("0" if c == "6" else "1" for c in s if c in ("6", "7"))


def binary_str_to_sopito(b: str) -> str:
    """Convierte una cadena binaria ('0' y '1') a Sopito++ ('6' y '7')."""
    return "".join("6" if c == "0" else "7" for c in b if c in ("0", "1"))


def sopito_to_int(s: str) -> int:
    """Convierte un número escrito en 6s y 7s a un entero decimal de 64 bits."""
    bin_str = sopito_to_binary_str(s)
    if not bin_str:
        return 0
    return int(bin_str, 2)


def int_to_sopito(n: int, min_bits: int = 1) -> str:
    """Convierte un entero positivo a formato Sopito++ (6s y 7s)."""
    if n < 0:
        raise ValueError("Los números directos en Sopito++ deben ser no negativos. Use NEG para negativos.")
    bin_str = bin(n)[2:]
    if len(bin_str) < min_bits:
        bin_str = bin_str.zfill(min_bits)
    return binary_str_to_sopito(bin_str)


def unescape_str(s: str) -> str:
    """Procesa secuencias de escape como \\n, \\t de forma segura sin alterar UTF-8."""
    res = []
    i = 0
    while i < len(s):
        if s[i] == '\\' and i + 1 < len(s):
            nxt = s[i+1]
            if nxt == 'n':
                res.append('\n')
                i += 2
                continue
            elif nxt == 't':
                res.append('\t')
                i += 2
                continue
            elif nxt == 'r':
                res.append('\r')
                i += 2
                continue
            elif nxt == '\\':
                res.append('\\')
                i += 2
                continue
            elif nxt == '"':
                res.append('"')
                i += 2
                continue
            elif nxt == "'":
                res.append("'")
                i += 2
                continue
        res.append(s[i])
        i += 1
    return "".join(res)


def text_to_sopito_bytes(text: str) -> List[str]:
    """Convierte texto UTF-8 a una lista de bytes de 8 caracteres en 6s y 7s."""
    res = []
    raw_bytes = text.encode("utf-8")
    for b in raw_bytes:
        b_str = bin(b)[2:].zfill(8)
        res.append(binary_str_to_sopito(b_str))
    return res


def sopito_bytes_to_text(bytes_list: List[str]) -> str:
    """Convierte una lista de bytes en 6s y 7s a texto UTF-8."""
    raw_bytes = bytearray()
    for b_sop in bytes_list:
        val = sopito_to_int(b_sop)
        raw_bytes.append(val & 0xFF)
    return raw_bytes.decode("utf-8", errors="replace")


# --- Estructura de Instrucción ---

class Instruction:
    def __init__(self, opcode: int, args: Optional[List[Any]] = None, line_num: int = 0, raw_str: str = ""):
        self.opcode = opcode
        self.args = args if args is not None else []
        self.line_num = line_num
        self.raw_str = raw_str

    @property
    def mnemonic(self) -> str:
        return OPCODE_TABLE[self.opcode]["mnemonic"]

    def __repr__(self):
        args_str = " " + " ".join(str(a) for a in self.args) if self.args else ""
        return f"<Inst {self.mnemonic}{args_str}>"


# --- Parser de Código Fuente Puro Sopito++ (.spp) ---

def parse_spp(source_code: str) -> List[Instruction]:
    """
    Parsea código Sopito++ puro (.spp) donde todo consiste en 6s y 7s,
    con soporte para comentarios (#, //, ;) y espacios en blanco.
    """
    tokens = []
    for line_idx, line in enumerate(source_code.splitlines(), start=1):
        # Eliminar comentarios
        cleaned_line = ""
        in_comment = False
        i = 0
        while i < len(line):
            if line[i] == '#' or line[i] == ';' or line[i:i+2] == '//':
                break
            cleaned_line += line[i]
            i += 1
        
        # Extraer tokens separados por espacios
        words = cleaned_line.split()
        for w in words:
            # Validar que sólo contenga 6 y 7
            if not all(c in ('6', '7') for c in w):
                raise SyntaxError(
                    f"[Línea {line_idx}] Token inválido '{w}'. En Sopito++ sólo se permiten los dígitos 6 (0) y 7 (1)."
                )
            tokens.append((w, line_idx))

    instructions = []
    token_idx = 0
    total_tokens = len(tokens)

    while token_idx < total_tokens:
        tok, line_num = tokens[token_idx]
        token_idx += 1

        if len(tok) != 5:
            raise SyntaxError(
                f"[Línea {line_num}] Opcode inválido '{tok}'. Cada opcode debe tener exactamente 5 dígitos de 6s y 7s."
            )

        if tok not in SOPITO_TO_OPCODE:
            raise SyntaxError(f"[Línea {line_num}] Opcode desconocido '{tok}'.")

        opcode = SOPITO_TO_OPCODE[tok]
        op_info = OPCODE_TABLE[opcode]
        args_needed = op_info["args"]

        if args_needed == 0:
            instructions.append(Instruction(opcode, [], line_num, tok))
        elif args_needed == 1:
            if token_idx >= total_tokens:
                raise SyntaxError(f"[Línea {line_num}] La instrucción {op_info['mnemonic']} requiere 1 argumento.")
            arg_tok, arg_line = tokens[token_idx]
            token_idx += 1
            num_val = sopito_to_int(arg_tok)
            instructions.append(Instruction(opcode, [num_val], line_num, f"{tok} {arg_tok}"))
        elif args_needed == -1:
            # Caso especial: PRINT_STR (<longitud> <byte1> <byte2> ...)
            if token_idx >= total_tokens:
                raise SyntaxError(f"[Línea {line_num}] PRINT_STR requiere longitud de cadena.")
            len_tok, _ = tokens[token_idx]
            token_idx += 1
            length = sopito_to_int(len_tok)

            bytes_sop = []
            for _ in range(length):
                if token_idx >= total_tokens:
                    raise SyntaxError(f"[Línea {line_num}] PRINT_STR esperaba {length} bytes, pero terminó el archivo.")
                b_tok, _ = tokens[token_idx]
                token_idx += 1
                bytes_sop.append(b_tok)
            
            str_val = sopito_bytes_to_text(bytes_sop)
            instructions.append(Instruction(opcode, [str_val], line_num, f"{tok} ... ({length} chars)"))

    return instructions


# --- Parser y Ensamblador de Mnemónicos (.sasm) ---

def parse_sasm(source_code: str) -> List[Instruction]:
    """
    Parsea código en ensamblador legible de Sopito++ (.sasm).

    Ejemplos de sintaxis::

        PUSH 42
        PUSH_STR "Hola Mundo"
        ADD
        PRINT_NUM
    """
    instructions = []
    for line_idx, line in enumerate(source_code.splitlines(), start=1):
        line = line.strip()
        if not line or line.startswith(('#', '//', ';')):
            continue

        # Eliminar comentarios al final de la línea
        clean_line = ""
        in_quotes = False
        i = 0
        while i < len(line):
            ch = line[i]
            if ch == '"':
                in_quotes = not in_quotes
            elif not in_quotes and (ch == '#' or ch == ';' or line[i:i+2] == '//'):
                break
            clean_line += ch
            i += 1
        clean_line = clean_line.strip()
        if not clean_line:
            continue

        # Extraer mnemónico y argumentos
        parts = clean_line.split(maxsplit=1)
        mnemonic = parts[0].upper()
        arg_str = parts[1].strip() if len(parts) > 1 else ""

        if mnemonic == "PUSH_STR":
            # Macro para imprimir o empujar cadena
            if not (arg_str.startswith('"') and arg_str.endswith('"')):
                raise SyntaxError(f"[Línea {line_idx}] PUSH_STR requiere una cadena entre comillas.")
            content = unescape_str(arg_str[1:-1])
            instructions.append(Instruction(MNEMONIC_TO_OPCODE["PRINT_STR"], [content], line_idx, clean_line))
            continue

        if mnemonic not in MNEMONIC_TO_OPCODE:
            raise SyntaxError(f"[Línea {line_idx}] Mnemónico desconocido '{mnemonic}'.")

        opcode = MNEMONIC_TO_OPCODE[mnemonic]
        op_info = OPCODE_TABLE[opcode]
        args_needed = op_info["args"]

        if args_needed == 0:
            instructions.append(Instruction(opcode, [], line_idx, clean_line))
        elif args_needed == 1:
            if not arg_str:
                raise SyntaxError(f"[Línea {line_idx}] '{mnemonic}' requiere un argumento entero.")
            try:
                # Permite entero decimal directo o en formato 6/7 con prefijo 0s / sopito
                if arg_str.startswith("0s") or arg_str.startswith("0S"):
                    val = sopito_to_int(arg_str[2:])
                elif all(c in ('6', '7') for c in arg_str) and not arg_str.isdigit():
                    val = sopito_to_int(arg_str)
                else:
                    val = int(arg_str, 0)
            except ValueError:
                raise SyntaxError(f"[Línea {line_idx}] Argumento inválido '{arg_str}'. Se esperaba un número.")
            instructions.append(Instruction(opcode, [val], line_idx, clean_line))
        elif args_needed == -1: # PRINT_STR directo
            content = unescape_str(arg_str.strip('"'))
            instructions.append(Instruction(opcode, [content], line_idx, clean_line))

    return instructions


# --- Ensamblador: AST -> Código Puro Sopito++ (.spp) ---

def assemble_to_spp(instructions: List[Instruction], annotated: bool = True) -> str:
    """Convierte una lista de instrucciones a código fuente Sopito++ puro (6s y 7s)."""
    lines = []
    lines.append("# ===========================================")
    lines.append("# Programa generado en Sopito++ (6=0, 7=1)")
    lines.append("# ===========================================\n")

    for inst in instructions:
        op_info = OPCODE_TABLE[inst.opcode]
        sop_op = op_info["sopito"]
        mnemonic = op_info["mnemonic"]

        if op_info["args"] == 0:
            if annotated:
                lines.append(f"{sop_op:<10} # {mnemonic}")
            else:
                lines.append(sop_op)
        elif op_info["args"] == 1:
            val = inst.args[0]
            sop_val = int_to_sopito(val)
            if annotated:
                lines.append(f"{sop_op} {sop_val:<12} # {mnemonic} {val} (binario: {sopito_to_binary_str(sop_val)})")
            else:
                lines.append(f"{sop_op} {sop_val}")
        elif op_info["args"] == -1:
            # PRINT_STR
            text = inst.args[0]
            bytes_sop = text_to_sopito_bytes(text)
            len_sop = int_to_sopito(len(bytes_sop))
            bytes_str = " ".join(bytes_sop)
            if annotated:
                escaped = repr(text)
                lines.append(f"{sop_op} {len_sop} {bytes_str} # PRINT_STR {escaped}")
            else:
                lines.append(f"{sop_op} {len_sop} {bytes_str}")

    return "\n".join(lines)


# --- Desensamblador: Código Puro (.spp) -> Ensamblador (.sasm) ---

def disassemble(instructions: List[Instruction]) -> str:
    """Desensambla instrucciones a código ensamblador legible con explicaciones."""
    lines = []
    lines.append("# --- Desensamblado de Sopito++ ---")
    for inst in instructions:
        op_info = OPCODE_TABLE[inst.opcode]
        mnem = op_info["mnemonic"]
        desc = op_info["desc"]
        if op_info["args"] == 0:
            lines.append(f"{mnem:<14} # [{op_info['sopito']}] {desc}")
        elif op_info["args"] == 1:
            val = inst.args[0]
            sop_val = int_to_sopito(val)
            lines.append(f"{mnem} {val:<8} # [{op_info['sopito']} {sop_val}] {desc}")
        elif op_info["args"] == -1:
            text = repr(inst.args[0])
            lines.append(f"{mnem} {text:<12} # [{op_info['sopito']} ...] {desc}")
    return "\n".join(lines)


# --- Generador de Código C++ Moderno ---

def compile_to_cpp(instructions: List[Instruction], source_name: str = "sopito_program") -> str:
    """
    Traduce las instrucciones de Sopito++ a código fuente C++ estándar,
    altamente optimizado, legible y con manejo seguro de pila y memoria.
    """
    cpp_lines = [
        "// ===========================================================================",
        f"// Generado automáticamente por el Compilador de Sopito++ (sopitoc)",
        f"// Fuente original: {source_name}",
        "// Dialecto: Sopito++ (6 = bit 0, 7 = bit 1)",
        "// ===========================================================================",
        "#include <iostream>",
        "#include <vector>",
        "#include <unordered_map>",
        "#include <cstdint>",
        "#include <string>",
        "",
        "// Estructura de Ejecución de Sopito++",
        "int main() {",
        "    // Pila de datos principal (enteros de 64 bits)",
        "    std::vector<int64_t> stack;",
        "    stack.reserve(1024);",
        "",
        "    // Memoria direccionable (celdas de variables globales)",
        "    std::unordered_map<int64_t, int64_t> memory;",
        "",
        "    // Pila de llamadas para subrutinas (CALL / RET)",
        "    std::vector<int> call_stack;",
        "    call_stack.reserve(64);",
        "",
        "    // Funciones auxiliares inline para seguridad de pila",
        "    auto pop = [&]() -> int64_t {",
        "        if (stack.empty()) return 0;",
        "        int64_t val = stack.back();",
        "        stack.pop_back();",
        "        return val;",
        "    };",
        "",
        "    auto top = [&]() -> int64_t {",
        "        return stack.empty() ? 0 : stack.back();",
        "    };",
        "",
        "    // --- Instrucciones Traducidas ---",
    ]

    # Pre-identificar llamadas para los puntos de retorno
    call_return_counter = 0
    call_return_points = []
    for inst in instructions:
        if inst.opcode == MNEMONIC_TO_OPCODE["CALL"]:
            call_return_counter += 1
            call_return_points.append(call_return_counter)

    has_ret = any(inst.opcode == MNEMONIC_TO_OPCODE["RET"] for inst in instructions)
    current_call_idx = 0

    for idx, inst in enumerate(instructions):
        mnem = inst.mnemonic
        op_info = OPCODE_TABLE[inst.opcode]
        sop_repr = op_info["sopito"]

        cpp_lines.append(f"    // [{sop_repr}] {mnem} (Línea {inst.line_num})")

        if mnem == "HALT":
            cpp_lines.append("    return 0;")
        elif mnem == "PUSH":
            val = inst.args[0]
            cpp_lines.append(f"    stack.push_back({val}LL);")
        elif mnem == "POP":
            cpp_lines.append("    pop();")
        elif mnem == "DUP":
            cpp_lines.append("    stack.push_back(top());")
        elif mnem == "SWAP":
            cpp_lines.append("    if (stack.size() >= 2) std::swap(stack[stack.size()-1], stack[stack.size()-2]);")
        elif mnem == "OVER":
            cpp_lines.append("    if (stack.size() >= 2) stack.push_back(stack[stack.size()-2]);")
        elif mnem == "ADD":
            cpp_lines.append("    { int64_t a = pop(); if (!stack.empty()) stack.back() += a; }")
        elif mnem == "SUB":
            cpp_lines.append("    { int64_t a = pop(); if (!stack.empty()) stack.back() -= a; }")
        elif mnem == "MUL":
            cpp_lines.append("    { int64_t a = pop(); if (!stack.empty()) stack.back() *= a; }")
        elif mnem == "DIV":
            cpp_lines.append("    { int64_t a = pop(); if (!stack.empty()) stack.back() = (a != 0 ? stack.back() / a : 0); }")
        elif mnem == "MOD":
            cpp_lines.append("    { int64_t a = pop(); if (!stack.empty()) stack.back() = (a != 0 ? stack.back() % a : 0); }")
        elif mnem == "NEG":
            cpp_lines.append("    if (!stack.empty()) stack.back() = -stack.back();")
        elif mnem == "EQ":
            cpp_lines.append("    { int64_t a = pop(); if (!stack.empty()) stack.back() = (stack.back() == a ? 1 : 0); }")
        elif mnem == "LT":
            cpp_lines.append("    { int64_t a = pop(); if (!stack.empty()) stack.back() = (stack.back() < a ? 1 : 0); }")
        elif mnem == "GT":
            cpp_lines.append("    { int64_t a = pop(); if (!stack.empty()) stack.back() = (stack.back() > a ? 1 : 0); }")
        elif mnem == "NOT":
            cpp_lines.append("    if (!stack.empty()) stack.back() = (stack.back() == 0 ? 1 : 0);")
        elif mnem == "AND":
            cpp_lines.append("    { int64_t a = pop(); if (!stack.empty()) stack.back() = (stack.back() & a); }")
        elif mnem == "OR":
            cpp_lines.append("    { int64_t a = pop(); if (!stack.empty()) stack.back() = (stack.back() | a); }")
        elif mnem == "LABEL":
            label_id = inst.args[0]
            cpp_lines.append(f"sopito_label_{label_id}:")
        elif mnem == "JMP":
            label_id = inst.args[0]
            cpp_lines.append(f"    goto sopito_label_{label_id};")
        elif mnem == "JZ":
            label_id = inst.args[0]
            cpp_lines.append(f"    if (pop() == 0) goto sopito_label_{label_id};")
        elif mnem == "JNZ":
            label_id = inst.args[0]
            cpp_lines.append(f"    if (pop() != 0) goto sopito_label_{label_id};")
        elif mnem == "STORE":
            var_id = inst.args[0]
            cpp_lines.append(f"    memory[{var_id}LL] = pop();")
        elif mnem == "LOAD":
            var_id = inst.args[0]
            cpp_lines.append(f"    stack.push_back(memory[{var_id}LL]);")
        elif mnem == "PRINT_NUM":
            cpp_lines.append("    std::cout << pop();")
        elif mnem == "PRINT_CHAR":
            cpp_lines.append("    std::cout << static_cast<char>(pop());")
        elif mnem == "PRINT_STR":
            text_escaped = ""
            for c in inst.args[0]:
                if c == '\\': text_escaped += "\\\\"
                elif c == '"': text_escaped += "\\\""
                elif c == '\n': text_escaped += "\\n"
                elif c == '\t': text_escaped += "\\t"
                elif c == '\r': text_escaped += "\\r"
                else: text_escaped += c
            cpp_lines.append(f'    std::cout << "{text_escaped}";')
        elif mnem == "PRINT_NL":
            cpp_lines.append("    std::cout << '\\n';")
        elif mnem == "READ_NUM":
            cpp_lines.append("    { int64_t val = 0; if (std::cin >> val) stack.push_back(val); else stack.push_back(0); }")
        elif mnem == "READ_CHAR":
            cpp_lines.append("    { char c = 0; if (std::cin.get(c)) stack.push_back(static_cast<uint8_t>(c)); else stack.push_back(-1); }")
        elif mnem == "CALL":
            target_label = inst.args[0]
            current_call_idx += 1
            cpp_lines.append(f"    call_stack.push_back({current_call_idx});")
            cpp_lines.append(f"    goto sopito_label_{target_label};")
            cpp_lines.append(f"sopito_ret_point_{current_call_idx}:")
        elif mnem == "RET":
            cpp_lines.append("    if (!call_stack.empty()) {")
            cpp_lines.append("        int ret_id = call_stack.back();")
            cpp_lines.append("        call_stack.pop_back();")
            cpp_lines.append("        switch (ret_id) {")
            for pt in call_return_points:
                cpp_lines.append(f"            case {pt}: goto sopito_ret_point_{pt};")
            cpp_lines.append("            default: break;")
            cpp_lines.append("        }")
            cpp_lines.append("    }")

    cpp_lines.append("")
    cpp_lines.append("    return 0;")
    cpp_lines.append("}")
    cpp_lines.append("")
    return "\n".join(cpp_lines)


# --- Máquina Virtual (Intérprete Directo de Sopito++) ---

class SopitoVM:
    """Máquina virtual integrada para ejecutar programas Sopito++ sin compilador externo."""

    def __init__(self, instructions: List[Instruction], trace: bool = False):
        self.instructions = instructions
        self.trace = trace
        self.stack: List[int] = []
        self.memory: Dict[int, int] = {}
        self.call_stack: List[int] = []
        self.labels: Dict[int, int] = {}
        self.ip = 0

        # Construir índice de etiquetas
        for idx, inst in enumerate(self.instructions):
            if inst.mnemonic == "LABEL":
                lbl_id = inst.args[0]
                self.labels[lbl_id] = idx

    def run(self):
        step = 0
        total = len(self.instructions)

        while self.ip < total:
            inst = self.instructions[self.ip]
            mnem = inst.mnemonic

            if self.trace:
                stack_preview = str(self.stack[-5:]) if len(self.stack) > 5 else str(self.stack)
                args_preview = f" {inst.args[0]}" if inst.args else ""
                print(f"[Paso {step:04d} | IP {self.ip:03d}] {mnem}{args_preview:<10} | Pila: {stack_preview}", file=sys.stderr)

            step += 1

            if mnem == "HALT":
                break
            elif mnem == "PUSH":
                self.stack.append(inst.args[0])
                self.ip += 1
            elif mnem == "POP":
                if self.stack:
                    self.stack.pop()
                self.ip += 1
            elif mnem == "DUP":
                if self.stack:
                    self.stack.append(self.stack[-1])
                self.ip += 1
            elif mnem == "SWAP":
                if len(self.stack) >= 2:
                    self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]
                self.ip += 1
            elif mnem == "OVER":
                if len(self.stack) >= 2:
                    self.stack.append(self.stack[-2])
                self.ip += 1
            elif mnem == "ADD":
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    self.stack[-1] += b
                self.ip += 1
            elif mnem == "SUB":
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    self.stack[-1] -= b
                self.ip += 1
            elif mnem == "MUL":
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    self.stack[-1] *= b
                self.ip += 1
            elif mnem == "DIV":
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    self.stack[-1] = self.stack[-1] // b if b != 0 else 0
                self.ip += 1
            elif mnem == "MOD":
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    self.stack[-1] = self.stack[-1] % b if b != 0 else 0
                self.ip += 1
            elif mnem == "NEG":
                if self.stack:
                    self.stack[-1] = -self.stack[-1]
                self.ip += 1
            elif mnem == "EQ":
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    self.stack[-1] = 1 if self.stack[-1] == b else 0
                self.ip += 1
            elif mnem == "LT":
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    self.stack[-1] = 1 if self.stack[-1] < b else 0
                self.ip += 1
            elif mnem == "GT":
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    self.stack[-1] = 1 if self.stack[-1] > b else 0
                self.ip += 1
            elif mnem == "NOT":
                if self.stack:
                    self.stack[-1] = 1 if self.stack[-1] == 0 else 0
                self.ip += 1
            elif mnem == "AND":
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    self.stack[-1] &= b
                self.ip += 1
            elif mnem == "OR":
                if len(self.stack) >= 2:
                    b = self.stack.pop()
                    self.stack[-1] |= b
                self.ip += 1
            elif mnem == "LABEL":
                self.ip += 1
            elif mnem == "JMP":
                lbl_id = inst.args[0]
                if lbl_id in self.labels:
                    self.ip = self.labels[lbl_id] + 1
                else:
                    raise RuntimeError(f"Etiqueta no encontrada: {lbl_id}")
            elif mnem == "JZ":
                lbl_id = inst.args[0]
                cond = self.stack.pop() if self.stack else 0
                if cond == 0:
                    if lbl_id in self.labels:
                        self.ip = self.labels[lbl_id] + 1
                    else:
                        raise RuntimeError(f"Etiqueta no encontrada: {lbl_id}")
                else:
                    self.ip += 1
            elif mnem == "JNZ":
                lbl_id = inst.args[0]
                cond = self.stack.pop() if self.stack else 0
                if cond != 0:
                    if lbl_id in self.labels:
                        self.ip = self.labels[lbl_id] + 1
                    else:
                        raise RuntimeError(f"Etiqueta no encontrada: {lbl_id}")
                else:
                    self.ip += 1
            elif mnem == "STORE":
                var_id = inst.args[0]
                val = self.stack.pop() if self.stack else 0
                self.memory[var_id] = val
                self.ip += 1
            elif mnem == "LOAD":
                var_id = inst.args[0]
                self.stack.append(self.memory.get(var_id, 0))
                self.ip += 1
            elif mnem == "PRINT_NUM":
                val = self.stack.pop() if self.stack else 0
                print(val, end="", flush=True)
                self.ip += 1
            elif mnem == "PRINT_CHAR":
                val = self.stack.pop() if self.stack else 0
                print(chr(val & 0xFF), end="", flush=True)
                self.ip += 1
            elif mnem == "PRINT_STR":
                print(inst.args[0], end="", flush=True)
                self.ip += 1
            elif mnem == "PRINT_NL":
                print("", flush=True)
                self.ip += 1
            elif mnem == "READ_NUM":
                try:
                    line = input()
                    val = int(line.strip())
                except (ValueError, EOFError):
                    val = 0
                self.stack.append(val)
                self.ip += 1
            elif mnem == "READ_CHAR":
                try:
                    ch = sys.stdin.read(1)
                    val = ord(ch) if ch else -1
                except EOFError:
                    val = -1
                self.stack.append(val)
                self.ip += 1
            elif mnem == "CALL":
                lbl_id = inst.args[0]
                if lbl_id in self.labels:
                    self.call_stack.append(self.ip + 1)
                    self.ip = self.labels[lbl_id] + 1
                else:
                    raise RuntimeError(f"Subrutina / etiqueta no encontrada: {lbl_id}")
            elif mnem == "RET":
                if self.call_stack:
                    self.ip = self.call_stack.pop()
                else:
                    break


# --- Consola Interactiva (REPL) ---

def run_repl():
    """Ejecuta una sesión interactiva de Sopito++."""
    print("=" * 60)
    print("  Bienvenido al REPL Interactivo de Sopito++ (6=0, 7=1)")
    print("  Escribe comandos en 6/7 o mnemónicos (ej. 'PUSH 42', 'ADD').")
    print("  Escribe 'pila', 'opcodes', 'tabla' o 'salir' para ayuda/control.")
    print("=" * 60)

    vm = SopitoVM([])
    while True:
        try:
            line = input("sopito++> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n¡Hasta luego!")
            break

        if not line:
            continue
        if line.lower() in ("salir", "exit", "quit"):
            print("¡Hasta luego!")
            break
        elif line.lower() == "pila":
            print(f"Estado de la pila: {vm.stack}")
            continue
        elif line.lower() == "memoria":
            print(f"Memoria de variables: {vm.memory}")
            continue
        elif line.lower() in ("opcodes", "tabla"):
            print("\nTabla de Opcodes principales:")
            for k, v in OPCODE_TABLE.items():
                print(f"  {v['sopito']} ({k:02d}) -> {v['mnemonic']:<12} : {v['desc']}")
            print()
            continue

        try:
            # Detectar si es código en 6/7 o mnemónico
            first_word = line.split()[0]
            if all(c in ('6', '7') for c in first_word):
                insts = parse_spp(line)
            else:
                insts = parse_sasm(line)

            for inst in insts:
                vm.instructions = [inst]
                vm.ip = 0
                vm.run()

            print(f" [Pila: {vm.stack}]")
        except Exception as e:
            print(f"Error: {e}")


# --- CLI Principal ---

def main():
    parser = argparse.ArgumentParser(
        description="Sopito++ (sopito++): Lenguaje binario donde 6 es 0 y 7 es 1. Compilador a C++."
    )
    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")

    # Comando: compile
    comp_parser = subparsers.add_parser("compile", help="Compilar archivo Sopito++ (.spp o .sasm) a C++")
    comp_parser.add_argument("input", help="Archivo de entrada (.spp o .sasm)")
    comp_parser.add_argument("-o", "--output", help="Archivo C++ de salida (.cpp)", default=None)
    comp_parser.add_argument("--build", action="store_true", help="Intentar compilar el C++ a ejecutable (.exe)")

    # Comando: run
    run_parser = subparsers.add_parser("run", help="Ejecutar directamente con la Máquina Virtual interna")
    run_parser.add_argument("input", help="Archivo a ejecutar (.spp o .sasm)")
    run_parser.add_argument("--trace", action="store_true", help="Mostrar traza paso a paso de la pila")

    # Comando: assemble
    asm_parser = subparsers.add_parser("assemble", help="Ensamblar archivo .sasm a código puro de 6s y 7s (.spp)")
    asm_parser.add_argument("input", help="Archivo de entrada (.sasm)")
    asm_parser.add_argument("-o", "--output", help="Archivo de salida (.spp)", default=None)
    asm_parser.add_argument("--no-comments", action="store_true", help="Generar sólo 6s y 7s sin comentarios")

    # Comando: disasm
    dis_parser = subparsers.add_parser("disasm", help="Desensamblar archivo .spp a mnemónicos legibles")
    dis_parser.add_argument("input", help="Archivo .spp a desensamblar")
    dis_parser.add_argument("-o", "--output", help="Archivo de salida opcional", default=None)

    # Comando: encode
    enc_parser = subparsers.add_parser("encode", help="Traducir texto o número normal a formato 6 y 7")
    enc_parser.add_argument("text", help="Texto o número a codificar")
    enc_parser.add_argument("--num", action="store_true", help="Interpretar entrada como número decimal")

    # Comando: decode
    dec_parser = subparsers.add_parser("decode", help="Traducir cadena de 6 y 7 a texto o número normal")
    dec_parser.add_argument("sopito_str", help="Cadena de 6s y 7s")
    dec_parser.add_argument("--num", action="store_true", help="Interpretar como número decimal")

    # Comando: repl
    subparsers.add_parser("repl", help="Iniciar consola interactiva")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    if args.command == "repl":
        run_repl()
        return

    if args.command == "encode":
        if args.num:
            n = int(args.text)
            sop = int_to_sopito(n)
            print(f"Decimal: {n}")
            print(f"Binario estándar: {bin(n)[2:]}")
            print(f"Sopito++ (6=0, 7=1): {sop}")
        else:
            bytes_sop = text_to_sopito_bytes(args.text)
            print(f"Texto: {repr(args.text)}")
            print(f"Sopito++ Bytes ({len(bytes_sop)}): {' '.join(bytes_sop)}")
        return

    if args.command == "decode":
        clean_sop = "".join(c for c in args.sopito_str if c in ('6', '7'))
        if args.num:
            n = sopito_to_int(clean_sop)
            print(f"Sopito++: {clean_sop}")
            print(f"Binario estándar: {sopito_to_binary_str(clean_sop)}")
            print(f"Decimal: {n}")
        else:
            # Dividir en bloques de 8 si es posible
            chunks = [clean_sop[i:i+8] for i in range(0, len(clean_sop), 8)]
            text = sopito_bytes_to_text(chunks)
            print(f"Sopito++: {clean_sop}")
            print(f"Texto ASCII: {text}")
        return

    # Comandos que leen un archivo de entrada
    if not os.path.isfile(args.input):
        print(f"Error: No se encontró el archivo '{args.input}'", file=sys.stderr)
        sys.exit(1)

    with open(args.input, "r", encoding="utf-8") as f:
        content = f.read()

    # Detectar formato según extensión o contenido
    is_sasm = args.input.endswith(".sasm")

    if args.command == "assemble":
        insts = parse_sasm(content)
        result_spp = assemble_to_spp(insts, annotated=not args.no_comments)
        out_file = args.output or os.path.splitext(args.input)[0] + ".spp"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(result_spp)
        print(f"[OK] Ensamblado exitoso: '{out_file}'")
        return

    if is_sasm:
        instructions = parse_sasm(content)
    else:
        instructions = parse_spp(content)

    if args.command == "disasm":
        dis_output = disassemble(instructions)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(dis_output)
            print(f"[OK] Desensamblado guardado en: '{args.output}'")
        else:
            print(dis_output)
        return

    if args.command == "run":
        vm = SopitoVM(instructions, trace=args.trace)
        vm.run()
        return

    if args.command == "compile":
        cpp_code = compile_to_cpp(instructions, source_name=os.path.basename(args.input))
        out_file = args.output or os.path.splitext(args.input)[0] + ".cpp"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(cpp_code)
        print(f"[OK] Código C++ generado exitosamente en: '{out_file}'")

        if args.build:
            exe_file = os.path.splitext(out_file)[0] + (".exe" if os.name == "nt" else "")
            # Probar compiladores C++ comunes
            compilers = ["g++", "clang++", "cl"]
            built = False
            for cc in compilers:
                try:
                    if cc in ("g++", "clang++"):
                        cmd = [cc, "-O2", out_file, "-o", exe_file]
                    else:
                        cmd = [cc, "/O2", out_file, f"/Fe:{exe_file}"]
                    res = subprocess.run(cmd, capture_output=True, text=True)
                    if res.returncode == 0:
                        print(f"[OK] Binario ejecutable compilado con {cc}: '{exe_file}'")
                        built = True
                        break
                except FileNotFoundError:
                    continue

            if not built:
                print(f"[INFO] No se encontró g++, clang++ ni cl en el PATH para generar el .exe.")
                print(f"       Puedes compilar '{out_file}' manualmente con cualquier compilador C++: g++ {out_file} -o {exe_file}")


if __name__ == "__main__":
    main()
