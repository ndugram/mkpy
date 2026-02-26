# Установка

## Требования

- Python 3.9 или выше

## Установка через pip

```bash
pip install mkpy-client
```

## Установка из исходников

```bash
git clone https://github.com/ndugram/mkpy.git
cd mkpy
pip install -e .
```

## Зависимости

mkpy автоматически устанавливает следующие зависимости:

- markdown - для конвертации Markdown в HTML
- annotated-doc - для документации параметров (опционально)

## Проверка установки

```python
from mkpy import __version__

print(__version__)  # Выведет версию mkpy
```

## Рекомендуемые зависимости

Для красивого вывода в консоли установите rich:

```bash
pip install rich
```

Без rich библиотека будет работать, но вывод в консоли будет простым текстом.
