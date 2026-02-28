# CLI

mkpy поставляется с удобным интерфейсом командной строки.

## Установка

```bash
pip install mkpy-client
```

## Основные команды

### mkpy serve

Запускает сервер документации.

```bash
mkpy serve
```

С параметрами:

```bash
mkpy serve --folder docs --theme dark --port 3000
```

### mkpy build

Генерирует статический сайт из markdown файлов.

```bash
mkpy build
```

С параметрами:

```bash
mkpy build --folder docs --output site --theme dark
```

### mkpy version

Показывает версию mkpy.

```bash
mkpy version
```

## Опции serve

| Опция | Кратко | Описание | По умолчанию |
|-------|--------|----------|--------------|
| `--folder` | `-f` | Папка с markdown файлами | docs |
| `--title` | `-t` | Заголовок документации | MKPY |
| `--theme` | | Тема: light или dark | light |
| `--host` | | Адрес сервера | 127.0.0.1 |
| `--port` | `-p` | Порт сервера | 8000 |
| `--no-nav` | | Отключить навигацию | false |

## Опции build

| Опция | Кратко | Описание | По умолчанию |
|-------|--------|----------|--------------|
| `--folder` | `-f` | Папка с markdown файлами | docs |
| `--output` | `-o` | Выходная папка для HTML | project |
| `--title` | `-t` | Заголовок документации | MKPY |
| `--theme` | | Тема: light или dark | light |
| `--no-nav` | | Отключить навигацию | false |

## Примеры

### Генерация статического сайта

```bash
# Базовое использование - создаст папку project с HTML файлами
mkpy build

# С указанием папки и вывода
mkpy build --folder docs --output mysite

# С темной темой
mkpy build --theme dark

# Всё вместе
mkpy build --folder docs --output site --theme dark --title "My Docs"
```

### Запуск с параметрами

```bash
mkpy serve --folder my_docs --theme dark --port 8080
```

### Запуск из файла конфигурации

```bash
mkpy serve main.py
```

Где `main.py`:

```python
from mkpy import Docs

docs = Docs(
    folder="docs",
    title="My Project",
    theme="dark",
    port=3000,
)
```

### Запуск с отключенной навигацией

```bash
mkpy serve --no-nav
```

## Автодополнение

Для удобства можно включить автодополнение в терминале:

```bash
# Bash
mkpy --install-completion bash

# Zsh
mkpy --install-completion zsh

# Fish
mkpy --install-completion fish
```
