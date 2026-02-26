# Кастомизация

## Кастомный CSS

Есть несколько способов добавить свой CSS:

### Inline CSS

```python
docs = Docs(
    custom_css="""
    .my-header {
        background: #ff6600;
        padding: 20px;
    }
    """
)
```

### Путь к файлу

```python
docs = Docs(
    custom_css="styles/custom.css"
)
```

### Папка css/

Создайте папку `docs/css/` и поместите туда файлы .css:

```
docs/
├── css/
│   ├── header.css
│   └── footer.css
└── index.md
```

Все CSS-файлы автоматически объединятся и добавятся на каждую страницу.

## Кастомный JavaScript

### Inline JavaScript

```python
docs = Docs(
    custom_js="""
    console.log('Page loaded!');
    document.querySelector('h1').addEventListener('click', () => {
        alert('Hello!');
    });
    """
)
```

### Путь к файлу

```python
docs = Docs(
    custom_js="scripts/main.js"
)
```

### Папка js/

Создайте папку `docs/js/` и поместите туда файлы .js:

```
docs/
├── js/
│   └── main.js
└── index.md
```

## Порядок подключения

CSS и JavaScript подключаются в следующем порядке:

1. Встроенные темы mkpy
2. CSS из папки `docs/css/` (по алфавиту)
3. Кастомный CSS из параметра `custom_css`

Аналогично для JavaScript:

1. Встроенные скрипты mkpy (подсветка текущей страницы, плавный скролл)
2. JS из папки `docs/js/` (по алфавиту)
3. Кастомный JS из параметра `custom_js`

## Примеры кастомизации

### Добавление своего шрифта

```python
docs = Docs(
    custom_css="""
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    body {
        font-family: 'Roboto', sans-serif;
    }
    """
)
```

### Добавление аналитики

```python
docs = Docs(
    custom_js="""
    // Google Analytics
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'UA-XXXXX-Y');
    """
)
```

### Изменение стиля навигации

```python
docs = Docs(
    custom_css="""
    .mkpy-nav {
        background: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
    }
    .mkpy-nav a {
        color: #333;
        margin-right: 15px;
    }
    """
)
```
