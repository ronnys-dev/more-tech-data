include .env
export
e=.env


main.py:  # Запустить основное приложение
	python ./backend/main.py

beauty:  # запуск проверок перед коммитом
	pre-commit run --all-files
