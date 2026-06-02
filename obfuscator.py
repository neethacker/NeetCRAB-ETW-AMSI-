# -*- coding: utf-8 -*-
import ast
import random
import string
import base64
import zlib
from typing import Dict, Set, List

class CodeObfuscator:
    """
    Продвинутый обфускатор Python кода с множественными техниками.
    """

    def __init__(self, config: Dict):
        self.config = config
        self.name_map = {}
        self.string_pool = []
        self.obf_level = config.get('obfuscation_level', 'medium')

    def _generate_random_name(self, prefix: str = '') -> str:
        """Генерирует случайное имя переменной."""
        if self.obf_level == 'low':
            length = random.randint(8, 12)
        elif self.obf_level == 'medium':
            length = random.randint(12, 20)
        else:  # high
            length = random.randint(20, 35)

        # Используем смесь букв разных алфавитов для усложнения
        chars = string.ascii_letters + '_'
        if self.obf_level == 'high':
            # Добавляем unicode символы для максимальной обфускации
            chars += 'αβγδεζηθικλμνξοπρστυφχψω'

        name = prefix + ''.join(random.choice(chars) for _ in range(length))
        return name

    def _obfuscate_strings(self, code: str) -> str:
        """Обфусцирует строковые литералы."""
        if not self.config.get('obfuscate_strings', True):
            return code

        lines = code.split('\n')
        result = []

        for line in lines:
            # Пропускаем комментарии и импорты
            if line.strip().startswith('#') or line.strip().startswith('import') or line.strip().startswith('from'):
                result.append(line)
                continue

            # Простая обфускация строк через base64
            if '"' in line or "'" in line:
                # Ищем строки в кавычках
                import re
                def replace_string(match):
                    s = match.group(0)
                    quote = s[0]
                    content = s[1:-1]

                    # Пропускаем очень короткие строки и специальные
                    if len(content) < 3 or content in ['r', 'b', 'f', 'u']:
                        return s

                    try:
                        encoded = base64.b64encode(content.encode()).decode()
                        return f'base64.b64decode("{encoded}").decode()'
                    except:
                        return s

                # Обрабатываем строки в двойных и одинарных кавычках
                line = re.sub(r'"[^"]{3,}"', replace_string, line)
                line = re.sub(r"'[^']{3,}'", replace_string, line)

            result.append(line)

        return '\n'.join(result)

    def _rename_variables(self, code: str) -> str:
        """Переименовывает переменные и функции."""
        if not self.config.get('rename_variables', True):
            return code

        try:
            tree = ast.parse(code)
        except:
            return code

        # Собираем все имена для переименования
        names_to_rename = set()
        builtin_names = set(dir(__builtins__))

        class NameCollector(ast.NodeVisitor):
            def visit_FunctionDef(self, node):
                if node.name not in builtin_names and not node.name.startswith('__'):
                    names_to_rename.add(node.name)
                self.generic_visit(node)

            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Store) and node.id not in builtin_names:
                    names_to_rename.add(node.id)
                self.generic_visit(node)

        collector = NameCollector()
        collector.visit(tree)

        # Создаём маппинг старых имён на новые
        for name in names_to_rename:
            if name not in self.name_map:
                self.name_map[name] = self._generate_random_name('_')

        # Заменяем имена в коде
        for old_name, new_name in self.name_map.items():
            # Используем границы слов для точной замены
            import re
            pattern = r'\b' + re.escape(old_name) + r'\b'
            code = re.sub(pattern, new_name, code)

        return code

    def _add_junk_code(self, code: str) -> str:
        """Добавляет мусорный код для усложнения анализа."""
        if not self.config.get('add_junk_code', False):
            return code

        junk_snippets = [
            f"_{self._generate_random_name()} = {random.randint(1000, 9999)}",
            f"_{self._generate_random_name()} = '{self._generate_random_name()}'",
            f"_{self._generate_random_name()} = lambda x: x * {random.randint(2, 10)}",
            f"if {random.randint(1, 100)} > {random.randint(101, 200)}: pass",
        ]

        lines = code.split('\n')
        result = []

        for i, line in enumerate(lines):
            result.append(line)
            # Добавляем мусор после некоторых строк
            if i % 10 == 0 and line.strip() and not line.strip().startswith('#'):
                result.append(random.choice(junk_snippets))

        return '\n'.join(result)

    def _control_flow_obfuscation(self, code: str) -> str:
        """Обфусцирует поток управления."""
        if not self.config.get('control_flow_obfuscation', False):
            return code

        # Простая обфускация: оборачиваем блоки кода в лямбды
        lines = code.split('\n')
        result = []

        for line in lines:
            if line.strip().startswith('def ') and not line.strip().startswith('def __'):
                # Добавляем декоратор-обфускатор
                indent = len(line) - len(line.lstrip())
                result.append(' ' * indent + f'# obf_{random.randint(1000, 9999)}')
            result.append(line)

        return '\n'.join(result)

    def _compress_code(self, code: str) -> str:
        """Сжимает и кодирует весь код."""
        if not self.config.get('compress_code', False):
            return code

        # Сжимаем код через zlib и base64
        compressed = zlib.compress(code.encode(), level=9)
        encoded = base64.b64encode(compressed).decode()

        # Создаём лоадер
        loader = f'''# -*- coding: utf-8 -*-
import base64, zlib
exec(zlib.decompress(base64.b64decode("{encoded}")))
'''
        return loader

    def _add_anti_debug(self, code: str) -> str:
        """Добавляет анти-отладочные проверки."""
        if not self.config.get('anti_debug', True):
            return code

        anti_debug_code = '''
# Anti-debug checks
import ctypes, sys, os, time

def _check_debug():
    try:
        if ctypes.windll.kernel32.IsDebuggerPresent():
            os._exit(0)
    except: pass

    try:
        import psutil
        for proc in psutil.process_iter(['name']):
            pname = proc.info['name'].lower()
            if any(x in pname for x in ['ida', 'olly', 'x64dbg', 'windbg', 'ghidra', 'processhacker']):
                os._exit(0)
    except: pass

    # Timing check
    _t1 = time.time()
    sum([i**2 for i in range(1000)])
    _t2 = time.time()
    if (_t2 - _t1) > 0.5:
        os._exit(0)

_check_debug()
'''
        return anti_debug_code + '\n' + code

    def _split_strings(self, code: str) -> str:
        """Разбивает строки на части для усложнения поиска."""
        if self.obf_level != 'high':
            return code

        import re

        def split_string(match):
            s = match.group(0)
            quote = s[0]
            content = s[1:-1]

            if len(content) < 10:
                return s

            # Разбиваем строку на части
            mid = len(content) // 2
            part1 = content[:mid]
            part2 = content[mid:]

            return f'({quote}{part1}{quote} + {quote}{part2}{quote})'

        code = re.sub(r'"[^"]{10,}"', split_string, code)
        code = re.sub(r"'[^']{10,}'", split_string, code)

        return code

    def obfuscate(self, code: str) -> str:
        """
        Применяет все техники обфускации к коду.

        Args:
            code: Исходный Python код

        Returns:
            str: Обфусцированный код
        """
        # Применяем техники в определённом порядке
        if self.config.get('anti_debug', True):
            code = self._add_anti_debug(code)

        if self.config.get('rename_variables', True):
            code = self._rename_variables(code)

        if self.config.get('obfuscate_strings', True):
            code = self._obfuscate_strings(code)

        if self.config.get('add_junk_code', False):
            code = self._add_junk_code(code)

        if self.config.get('control_flow_obfuscation', False):
            code = self._control_flow_obfuscation(code)

        if self.obf_level == 'high':
            code = self._split_strings(code)

        # Сжатие применяем в последнюю очередь
        if self.config.get('compress_code', False):
            code = self._compress_code(code)

        return code


def obfuscate_code(code: str, config: Dict) -> str:
    """
    Обфусцирует Python код с заданными настройками.

    Args:
        code: Исходный код
        config: Конфигурация обфускации

    Returns:
        str: Обфусцированный код
    """
    obfuscator = CodeObfuscator(config)
    return obfuscator.obfuscate(code)
