# -*- coding: utf-8 -*-
"""
Code Self-Modification Module - Модуль самомодификации кода
Техники для динамического изменения кода во время выполнения
"""

import os
import sys
import random
import string
import base64
import hashlib
import marshal
import types
import inspect
from typing import Callable, Any, Optional, List


class CodeMutator:
    """
    Класс для мутации и самомодификации кода.
    """

    def __init__(self):
        self.mutation_count = 0
        self.original_code = None

    def mutate_strings(self, code: str) -> str:
        """
        Мутирует строковые литералы в коде.

        Args:
            code: Исходный код

        Returns:
            Мутированный код
        """
        import re

        def replace_string(match):
            s = match.group(0)
            quote = s[0]
            content = s[1:-1]

            if len(content) < 3:
                return s

            # Кодируем в base64
            encoded = base64.b64encode(content.encode()).decode()
            return f'base64.b64decode("{encoded}").decode()'

        # Заменяем строки
        code = re.sub(r'"[^"]{3,}"', replace_string, code)
        code = re.sub(r"'[^']{3,}'", replace_string, code)

        self.mutation_count += 1
        return code

    def mutate_variable_names(self, code: str) -> str:
        """
        Мутирует имена переменных.

        Args:
            code: Исходный код

        Returns:
            Мутированный код
        """
        import re

        # Находим все имена переменных
        var_pattern = r'\b([a-z_][a-z0-9_]*)\b'
        variables = set(re.findall(var_pattern, code, re.IGNORECASE))

        # Исключаем ключевые слова Python
        keywords = {
            'def', 'class', 'if', 'else', 'elif', 'for', 'while', 'try',
            'except', 'finally', 'with', 'import', 'from', 'return', 'yield',
            'break', 'continue', 'pass', 'raise', 'assert', 'del', 'global',
            'nonlocal', 'lambda', 'and', 'or', 'not', 'in', 'is', 'True',
            'False', 'None', 'print', 'len', 'range', 'str', 'int', 'float'
        }

        variables = variables - keywords

        # Создаём маппинг
        mapping = {}
        for var in variables:
            if not var.startswith('_'):
                new_name = '_' + ''.join(random.choices(string.ascii_letters, k=10))
                mapping[var] = new_name

        # Заменяем
        for old, new in mapping.items():
            code = re.sub(r'\b' + old + r'\b', new, code)

        self.mutation_count += 1
        return code

    def add_junk_code(self, code: str, percentage: int = 20) -> str:
        """
        Добавляет мусорный код.

        Args:
            code: Исходный код
            percentage: Процент мусорного кода (0-100)

        Returns:
            Код с мусором
        """
        junk_snippets = [
            f"_{self._random_name()} = {random.randint(1000, 9999)}",
            f"_{self._random_name()} = '{self._random_name()}'",
            f"_{self._random_name()} = lambda x: x * {random.randint(2, 10)}",
            f"if {random.randint(1, 100)} > {random.randint(101, 200)}: pass",
        ]

        lines = code.split('\n')
        result = []

        # Вычисляем частоту добавления мусора
        frequency = max(1, int(100 / max(1, percentage)))

        for i, line in enumerate(lines):
            result.append(line)
            if i % frequency == 0 and line.strip() and not line.strip().startswith('#'):
                result.append(random.choice(junk_snippets))

        self.mutation_count += 1
        return '\n'.join(result)

    def apply_metamorphism(self, code: str) -> str:
        """
        Применяет метаморфизм - полную перестройку кода.

        Args:
            code: Исходный код

        Returns:
            Метаморфный код
        """
        # Применяем все техники
        code = self.mutate_strings(code)
        code = self.mutate_variable_names(code)
        code = self.add_junk_code(code, percentage=30)
        code = self.encrypt_code(code)

        self.mutation_count += 1
        return code

    def encrypt_code(self, code: str) -> str:
        """
        Шифрует код и создаёт лоадер.

        Args:
            code: Исходный код

        Returns:
            Зашифрованный код с лоадером
        """
        # Компилируем код
        compiled = compile(code, '<string>', 'exec')

        # Сериализуем
        marshaled = marshal.dumps(compiled)

        # Кодируем в base64
        encoded = base64.b64encode(marshaled).decode()

        # Создаём лоадер
        loader = f'''
import base64, marshal
exec(marshal.loads(base64.b64decode("{encoded}")))
'''

        self.mutation_count += 1
        return loader

    def polymorphic_transform(self, code: str) -> str:
        """
        Полиморфная трансформация кода.

        Args:
            code: Исходный код

        Returns:
            Трансформированный код
        """
        # Применяем несколько техник
        code = self.mutate_strings(code)
        code = self.mutate_variable_names(code)
        code = self.add_junk_code(code)

        return code

    def _random_name(self, length: int = 8) -> str:
        """Генерирует случайное имя."""
        return ''.join(random.choices(string.ascii_letters, k=length))


class RuntimeMutator:
    """
    Класс для мутации кода во время выполнения.
    """

    @staticmethod
    def modify_function(func: Callable, new_code: str) -> Callable:
        """
        Модифицирует функцию во время выполнения.

        Args:
            func: Исходная функция
            new_code: Новый код функции

        Returns:
            Модифицированная функция
        """
        # Компилируем новый код
        compiled = compile(new_code, '<string>', 'exec')

        # Создаём новую функцию
        namespace = {}
        exec(compiled, namespace)

        # Находим функцию в namespace
        for name, obj in namespace.items():
            if callable(obj) and not name.startswith('_'):
                return obj

        return func

    @staticmethod
    def inject_code_into_function(func: Callable, injection: str, position: str = 'start') -> Callable:
        """
        Внедряет код в функцию.

        Args:
            func: Целевая функция
            injection: Код для внедрения
            position: Позиция ('start' или 'end')

        Returns:
            Модифицированная функция
        """
        # Получаем исходный код
        source = inspect.getsource(func)

        # Находим тело функции
        lines = source.split('\n')
        func_def = lines[0]
        body = '\n'.join(lines[1:])

        # Внедряем код
        if position == 'start':
            new_body = f"{injection}\n{body}"
        else:
            new_body = f"{body}\n{injection}"

        new_source = f"{func_def}\n{new_body}"

        # Компилируем
        compiled = compile(new_source, '<string>', 'exec')
        namespace = {}
        exec(compiled, namespace)

        return namespace[func.__name__]

    @staticmethod
    def create_metamorphic_function(base_func: Callable) -> Callable:
        """
        Создаёт метаморфную функцию, которая изменяется при каждом вызове.

        Args:
            base_func: Базовая функция

        Returns:
            Метаморфная функция
        """
        mutation_counter = [0]

        def metamorphic_wrapper(*args, **kwargs):
            # Изменяем функцию при каждом вызове
            mutation_counter[0] += 1

            # Добавляем случайную задержку
            import time
            time.sleep(random.uniform(0.001, 0.01))

            # Выполняем оригинальную функцию
            result = base_func(*args, **kwargs)

            return result

        return metamorphic_wrapper


class CodeObfuscator:
    """
    Продвинутый обфускатор с самомодификацией.
    """

    @staticmethod
    def create_self_modifying_code(code: str) -> str:
        """
        Создаёт самомодифицирующийся код.

        Args:
            code: Исходный код

        Returns:
            Самомодифицирующийся код
        """
        # Кодируем исходный код
        encoded = base64.b64encode(code.encode()).decode()

        wrapper = f'''
import base64, random, string

# Декодируем и модифицируем код
def _decode_and_modify():
    code = base64.b64decode("{encoded}").decode()

    # Добавляем случайные комментарии
    lines = code.split('\\n')
    modified = []
    for line in lines:
        modified.append(line)
        if random.random() > 0.7:
            comment = '# ' + ''.join(random.choices(string.ascii_letters, k=20))
            modified.append(comment)

    return '\\n'.join(modified)

# Выполняем модифицированный код
exec(_decode_and_modify())
'''

        return wrapper

    @staticmethod
    def create_code_with_checksum(code: str) -> str:
        """
        Создаёт код с проверкой контрольной суммы.

        Args:
            code: Исходный код

        Returns:
            Код с проверкой
        """
        # Вычисляем контрольную сумму
        checksum = hashlib.sha256(code.encode()).hexdigest()

        wrapper = f'''
import hashlib

# Код с проверкой целостности
_code = """{code}"""

# Проверяем контрольную сумму
_expected = "{checksum}"
_actual = hashlib.sha256(_code.encode()).hexdigest()

if _actual != _expected:
    import sys
    sys.exit(0)

# Выполняем код
exec(_code)
'''

        return wrapper


class PolymorphicEngine:
    """
    Движок для полиморфной трансформации кода.
    """

    def __init__(self):
        self.mutator = CodeMutator()

    def apply_polymorphism(self, code: str) -> str:
        """
        Применяет полиморфную трансформацию к коду.

        Args:
            code: Исходный код

        Returns:
            Полиморфный код
        """
        # Применяем несколько техник мутации
        code = self.mutator.mutate_variable_names(code)
        code = self.mutator.add_junk_code(code)

        return code

    def generate_variants(self, code: str, count: int = 3) -> List[str]:
        """
        Генерирует несколько полиморфных вариантов.

        Args:
            code: Исходный код
            count: Количество вариантов

        Returns:
            Список вариантов
        """
        variants = []
        for _ in range(count):
            variant = self.apply_polymorphism(code)
            variants.append(variant)
        return variants


class AntiTampering:
    """
    Класс для защиты от модификации кода.
    """

    @staticmethod
    def add_integrity_check(code: str) -> str:
        """
        Добавляет проверку целостности.

        Args:
            code: Исходный код

        Returns:
            Код с проверкой целостности
        """
        checksum = hashlib.sha256(code.encode()).hexdigest()

        protected = f'''
import hashlib, sys

def _check_integrity():
    with open(__file__, 'r') as f:
        content = f.read()

    # Вычисляем контрольную сумму
    lines = content.split('\\n')
    code_lines = [l for l in lines if not l.strip().startswith('_check_integrity')]
    code = '\\n'.join(code_lines)

    checksum = hashlib.sha256(code.encode()).hexdigest()

    # Проверяем
    if checksum != "{checksum}":
        sys.exit(0)

_check_integrity()

{code}
'''

        return protected

    @staticmethod
    def add_debugger_detection(code: str) -> str:
        """
        Добавляет детект отладчика.

        Args:
            code: Исходный код

        Returns:
            Код с детектом отладчика
        """
        protected = f'''
import sys, ctypes

def _check_debugger():
    try:
        if ctypes.windll.kernel32.IsDebuggerPresent():
            sys.exit(0)
    except:
        pass

_check_debugger()

{code}
'''

        return protected


def generate_polymorphic_payload(base_code: str, iterations: int = 5) -> List[str]:
    """
    Генерирует несколько полиморфных вариантов кода.

    Args:
        base_code: Базовый код
        iterations: Количество вариантов

    Returns:
        Список вариантов кода
    """
    mutator = CodeMutator()
    variants = []

    for i in range(iterations):
        variant = mutator.polymorphic_transform(base_code)
        variants.append(variant)

    return variants


# Пример использования
if __name__ == "__main__":
    print("Code Self-Modification Module - Тестирование")
    print("=" * 60)

    # Пример кода
    sample_code = """
def hello_world():
    message = "Hello, World!"
    print(message)
    return message

hello_world()
"""

    print("\n[Исходный код]")
    print(sample_code)

    # Мутация строк
    print("\n[Мутация строк]")
    mutator = CodeMutator()
    mutated = mutator.mutate_strings(sample_code)
    print(mutated[:200] + "...")

    # Полиморфная трансформация
    print("\n[Полиморфная трансформация]")
    poly = mutator.polymorphic_transform(sample_code)
    print(poly[:300] + "...")

    # Шифрование кода
    print("\n[Шифрование кода]")
    encrypted = mutator.encrypt_code(sample_code)
    print(encrypted[:200] + "...")

    # Самомодифицирующийся код
    print("\n[Самомодифицирующийся код]")
    self_mod = CodeObfuscator.create_self_modifying_code(sample_code)
    print(self_mod[:300] + "...")

    # Генерация полиморфных вариантов
    print("\n[Генерация полиморфных вариантов]")
    variants = generate_polymorphic_payload(sample_code, iterations=3)
    print(f"Сгенерировано вариантов: {len(variants)}")
    for i, variant in enumerate(variants, 1):
        print(f"\nВариант {i} (первые 150 символов):")
        print(variant[:150] + "...")
