# Крамниця — простий онлайн-магазин на Django

Каталог товарів за категоріями, кошик на сесіях, оформлення замовлення
**без онлайн-оплати** (клієнт лишає заявку — ім'я, телефон, адресу,
коментар — а ви зв'язуєтесь і домовляєтесь про оплату/доставку самі).
Усім керує стандартна адмінка Django.

## Запуск локально (PyCharm Community теж підходить)

Python 3.10+ має бути встановлений.

```bash
git clone <посилання-на-твій-репозиторій>
cd shop_store
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Сайт: http://127.0.0.1:8000/
Адмінка: http://127.0.0.1:8000/admin/

Хочеш одразу побачити кілька товарів, не заповнюючи все вручну:

```bash
python manage.py load_demo_data
```

Це створить 3 категорії й по 2 товари в кожній — щоб одразу побачити,
як виглядає каталог. Потім просто видали їх з адмінки і додай свої.

## Як працювати з адмінкою

- **Товари** → додаєш назву, категорію, ціну, опис, фото. Slug (для
  посилання) генерується сам із назви.
- **Категорії** → так само, slug сам.
- **Замовлення** → тут з'являються всі заявки з сайту. Можна змінити
  статус (Нове → Підтверджено → Виконано) прямо у списку, без
  відкриття картки.

## Фото товарів і Render

У Render файлова система **ефемерна** — все, що завантажене через
адмінку (фото товарів), зникає після кожного деплою чи перезапуску
сервера. Щоб фото не зникали:

1. Зареєструйся безкоштовно на [cloudinary.com](https://cloudinary.com)
2. У дашборді Cloudinary візьми `Cloud name`, `API Key`, `API Secret`
3. Додай їх як змінні середовища на Render (Environment → Add):
   `CLOUDINARY_CLOUD_NAME`, `CLOUDINARY_API_KEY`, `CLOUDINARY_API_SECRET`

Якщо цього не зробити — все буде працювати, але фото товарів варто
буде перезаливати після кожного деплою.

## Деплой на Render

### Варіант А — через render.yaml (найшвидше)

1. Заливаєш проєкт у свій репозиторій на GitHub.
2. На [render.com](https://render.com) → **New** → **Blueprint** →
   вибираєш свій репозиторій. Render сам прочитає `render.yaml`,
   створить і вебсервіс, і безкоштовну Postgres-базу, і згенерує
   `SECRET_KEY`.
3. Після першого деплою додай (за бажанням) змінні Cloudinary з
   попереднього розділу.
4. Заходиш у Render Shell для сервісу і виконуєш:
   ```bash
   python manage.py createsuperuser
   ```

### Варіант Б — вручну, як минулого разу

1. **New** → **Web Service** → підключаєш репозиторій.
2. Build Command: `./build.sh`
3. Start Command: `gunicorn shop_store.wsgi:application`
4. Окремо створюєш **New** → **PostgreSQL** (безкоштовний план),
   копіюєш Internal Database URL.
5. У Environment вебсервісу додаєш:
   - `SECRET_KEY` — будь-який довгий випадковий рядок
   - `DEBUG` = `False`
   - `ALLOWED_HOSTS` = `<твій-сервіс>.onrender.com`
   - `CSRF_TRUSTED_ORIGINS` = `https://<твій-сервіс>.onrender.com`
   - `DATABASE_URL` — те, що скопіювала з Postgres
6. Deploy. Потім через Render Shell: `python manage.py createsuperuser`.

## Структура проєкту

```
shop_store/
├── catalog/                # увесь магазин: моделі, адмінка, кошик, views
│   ├── models.py            # Category, Product, Order, OrderItem
│   ├── admin.py
│   ├── cart.py              # кошик на сесіях, без БД
│   ├── views.py
│   ├── forms.py
│   └── management/commands/load_demo_data.py
├── templates/                # HTML-шаблони
├── static/css/style.css      # стилі
├── shop_store/                # налаштування Django-проєкту
├── build.sh                   # команда збірки для Render
├── render.yaml                 # blueprint для деплою одним кліком
└── requirements.txt
```

## Що можна додати пізніше

- Онлайн-оплату (LiqPay/Fondy) — якщо вирішиш, що заявок замало.
- Пошук і фільтр по ціні.
- Email-сповіщення на твою скриньку при новому замовленні (через
  Django `send_mail`, є вже готова форма — додати треба буквально
  кілька рядків у `order_create`).
