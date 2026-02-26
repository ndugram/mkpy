# Использование

## Базовый пример

Создайте файл `main.py`:

```python
from mkpy import Docs

docs = Docs(
    title="My Project",
    theme="dark",
    port=3000,
)
docs.run()
```

Затем создайте папку `docs` с Markdown-файлами:

```
project/
├── main.py
└── docs/
    └── index.md
```

Запустите:

```bash
python main.py
```

## Параметры конструктора Docs

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| `folder` | str | "docs" | Папка с Markdown-файлами |
| `title` | str | "MKPY" | Заголовок документации |
| `theme` | str | "light" | Тема: "light" или "dark" |
| `host` | str | "127.0.0.1" | Адрес сервера |
| `port` | int | 8000 | Порт сервера |
| `show_nav` | bool | True | Показывать навигацию |
| `custom_css` | str \| None | None | Кастомный CSS |
| `custom_js` | str \| None | None | Кастомный JavaScript |

## Примеры использования

### Смена темы

```python
docs = Docs(theme="dark")
```

### Изменение порта

```python
docs = Docs(port=8080)
```

### Кастомный CSS

```python
docs = Docs(custom_css=".my-class { color: red; }")
# или путь к файлу
docs = Docs(custom_css="styles/custom.css")
```

### Кастомный JavaScript

```python
docs = Docs(custom_js="console.log('Hello!');")
# или путь к файлу
docs = Docs(custom_js="scripts/main.js")
```

### Отключение навигации

```python
docs = Docs(show_nav=False)
```

## Автоматические папки

Создайте папки `css/` и `js/` внутри папки docs для автоматического подключения стилей и скриптов:

```
docs/
├── css/
│   └── style.css
├── js/
│   └── main.js
└── index.md
```

Все файлы из этих папок будут автоматически добавлены на каждую страницу.
