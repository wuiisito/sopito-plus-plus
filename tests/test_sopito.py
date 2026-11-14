#!/usr/bin/env python3
"""
Suite de pruebas unitarias para Sopito++
"""

import unittest
import sys
import os

# Añadir directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sopitoc import (
    sopito_to_binary_str,
    binary_str_to_sopito,
    sopito_to_int,
    int_to_sopito,
    text_to_sopito_bytes,
    sopito_bytes_to_text,
    parse_spp,
    parse_sasm,
    assemble_to_spp,
    disassemble,
    compile_to_cpp,
    SopitoVM,
    OPCODE_TABLE,
    MNEMONIC_TO_OPCODE,
)


class TestSopitoConversions(unittest.TestCase):
    def test_bit_mapping(self):
        # 6 = 0, 7 = 1
        self.assertEqual(sopito_to_binary_str("6"), "0")
        self.assertEqual(sopito_to_binary_str("7"), "1")
        self.assertEqual(sopito_to_binary_str("7676"), "1010")
        self.assertEqual(binary_str_to_sopito("1010"), "7676")
        self.assertEqual(binary_str_to_sopito("00000"), "66666")
        self.assertEqual(binary_str_to_sopito("11111"), "77777")

    def test_numeric_conversions(self):
        # 0 en binario es 0 -> '6'
        self.assertEqual(sopito_to_int("6"), 0)
        self.assertEqual(sopito_to_int("7"), 1)
        self.assertEqual(sopito_to_int("76"), 2)
        self.assertEqual(sopito_to_int("77"), 3)
        self.assertEqual(sopito_to_int("766"), 4)
        self.assertEqual(sopito_to_int("767"), 5)
        self.assertEqual(sopito_to_int("776"), 6)
        self.assertEqual(sopito_to_int("777"), 7)
        self.assertEqual(sopito_to_int("767676"), 42)

        self.assertEqual(int_to_sopito(0), "6")
        self.assertEqual(int_to_sopito(1), "7")
        self.assertEqual(int_to_sopito(6), "776")
        self.assertEqual(int_to_sopito(7), "777")
        self.assertEqual(int_to_sopito(42), "767676")

    def test_text_bytes(self):
        msg = "Hola Sopito++"
        bytes_sop = text_to_sopito_bytes(msg)
        self.assertEqual(len(bytes_sop), len(msg.encode("utf-8")))
        recovered = sopito_bytes_to_text(bytes_sop)
        self.assertEqual(recovered, msg)


class TestSopitoVM(unittest.TestCase):
    def test_arithmetic(self):
        code = """
        PUSH 15
        PUSH 4
        ADD
        PUSH 3
        SUB
        PUSH 2
        MUL
        PUSH 4
        DIV
        HALT
        """
        insts = parse_sasm(code)
        vm = SopitoVM(insts)
        vm.run()
        # ((15 + 4 - 3) * 2) / 4 = (16 * 2) / 4 = 32 / 4 = 8
        self.assertEqual(vm.stack, [8])

    def test_stack_operations(self):
        code = """
        PUSH 10
        DUP
        PUSH 20
        SWAP
        OVER
        HALT
        """
        insts = parse_sasm(code)
        vm = SopitoVM(insts)
        vm.run()
        # PUSH 10 -> [10]
        # DUP     -> [10, 10]
        # PUSH 20 -> [10, 10, 20]
        # SWAP    -> [10, 20, 10]
        # OVER    -> [10, 20, 10, 20]
        self.assertEqual(vm.stack, [10, 20, 10, 20])

    def test_memory_store_load(self):
        code = """
        PUSH 42
        STORE 5
        PUSH 100
        STORE 6
        LOAD 5
        LOAD 6
        ADD
        HALT
        """
        insts = parse_sasm(code)
        vm = SopitoVM(insts)
        vm.run()
        self.assertEqual(vm.stack, [142])
        self.assertEqual(vm.memory[5], 42)
        self.assertEqual(vm.memory[6], 100)

    def test_comparison_logic(self):
        code = """
        PUSH 5
        PUSH 10
        LT
        PUSH 20
        PUSH 20
        EQ
        AND
        HALT
        """
        insts = parse_sasm(code)
        vm = SopitoVM(insts)
        vm.run()
        # 5 < 10 is 1
        # 20 == 20 is 1
        # 1 & 1 is 1
        self.assertEqual(vm.stack, [1])

    def test_pure_spp_execution(self):
        # 6 + 7 = 13 en puro Sopito++ (6s y 7s)
        # PUSH 6 -> 66667 776
        # PUSH 7 -> 66667 777
        # ADD    -> 66776
        # HALT   -> 66666
        raw_code = "66667 776 66667 777 66776 66666"
        insts = parse_spp(raw_code)
        self.assertEqual(len(insts), 4)
        vm = SopitoVM(insts)
        vm.run()
        self.assertEqual(vm.stack, [13])


class TestCppCodeGeneration(unittest.TestCase):
    def test_generate_cpp_structure(self):
        code = """
        PUSH 6
        PUSH 7
        ADD
        PRINT_NUM
        PRINT_NL
        HALT
        """
        insts = parse_sasm(code)
        cpp = compile_to_cpp(insts, "test_prog")
        self.assertIn("#include <iostream>", cpp)
        self.assertIn("std::vector<int64_t> stack;", cpp)
        self.assertIn("std::unordered_map<int64_t, int64_t> memory;", cpp)
        self.assertIn("stack.push_back(6LL);", cpp)
        self.assertIn("stack.push_back(7LL);", cpp)
        self.assertIn("std::cout << pop();", cpp)
        self.assertIn("return 0;", cpp)


if __name__ == "__main__":
    unittest.main()
