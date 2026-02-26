# mkpy

mkpy - минималистичная Python-библиотека для генерации и запуска документации из Markdown-файлов.

## Возможности

- Автоматическое чтение Markdown-файлов из папки
- Конвертация в HTML и подъем HTTP-сервера
- Автоматическое построение маршрутов на основе структуры файлов
- Встроенные темы (light и dark)
- Поддержка кастомных CSS и JavaScript
- Автоматическое обнаружение папок css/ и js/
- Красивый вывод в консоли

## Быстрый старт

```python
from mkpy import Docs

docs = Docs(
    title="My Project",
    theme="dark",
    port=3000,
)
docs.run()
```

## Установка

```bash
pip install mkpy
```

## Структура маршрутов

Если структура файлов такая:

```
docs/
├── index.md
├── about.md
└── guide/
    └── install.md
```

То mkpy создаст маршруты:

- `/` -> index.md
- `/about` -> about.md
- `/guide/install` -> guide/install.md

## Смотрите также

- [Установка и требования](install.md)
- [Подробное использование](usage.md)
- [Темы оформления](themes.md)
- [Кастомизация](customization.md)
- [Командная строка (CLI)](cli.md)
