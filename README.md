# NeetCRAB – независимые модули для обхода ETW/AMSI и обфускации кода

Просто скопируйте нужный `.py` файл в ваш проект и импортируйте.

## Модули

| Файл | Что делает |
|------|-------------|
| `etw_bypass.py` | Обход ETW (Event Tracing for Windows) через патчинг функций ntdll |
| `amsi_bypass.py` | Обход AMSI (Antimalware Scan Interface) |
| `obfuscator.py` | Обфускация Python кода (переименование, шифрование строк, анти-отладка) |
| `code_self_modify.py` | Полиморфизм, самомодификация кода во время выполнения |

## Быстрый старт

```python
# Обход ETW
from etw_bypass import ETWBypass
ETWBypass().bypass_all()

# Обход AMSI
from amsi_bypass import AMSIBypass
AMSIBypass().bypass_all()

# Обфускация кода
from obfuscator import obfuscate_code
code = "print('hello')"
config = {'obfuscation_level': 'high', 'rename_variables': True}
obfuscated = obfuscate_code(code, config)

# Самомодификация
from code_self_modify import CodeMutator
mutator = CodeMutator()
new_code = mutator.apply_metamorphism(code)
