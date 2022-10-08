## Локальный запуск:

Запуск с docker-compose:
- запускаем из корня
- <code>docker-compose up --build</code>
- http://localhost:8000/health_check
- пересобираем без кэша при необходимости <code>docker-compose build --no-cache</code>
- документацию можно посмотреть здесь http://localhost:8000/swagger
- 
## Эндпоинт <code>http://localhost:8000/api/news/relevant_news</code> принимает на вход роль и выдает релевантные новости