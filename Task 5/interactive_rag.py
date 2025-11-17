import os
import sys
import readline
import re

FORBIDDEN_WORDS = {"root", "Ignore all instructions"}

def filter_query(question):
    if len(question) > 500:
        raise ValueError("Вопрос слишком длинный. Максимум 500 символов.")

    if any(word in question.lower() for word in FORBIDDEN_WORDS):
        raise ValueError("Вопрос содержит недопустимые слова.")

    return True

def main():
    print("Интерактивный RAG бот для Star Wars")
    try:
        from simple_rag import SimpleRAGBot
        print("Инициализация RAG системы")
        bot = SimpleRAGBot()
        print("Бот готов к диалогу")
        print("Введите вопросы о Star Wars вселенной")
        print("Команды: 'quit' - выход, 'clear' - очистка экрана")

        while True:
            try:
                question = input("\nВаш вопрос: ").strip()

                if question.lower() in ['quit', 'exit', 'выход', 'q']:
                    print("Пока")
                    break
                elif question.lower() in ['clear', 'cls']:
                    os.system('clear' if os.name == 'posix' else 'cls')
                    continue
                elif not question:
                    continue

                if filter_query(question):
                    print("Обработка запроса")
                    answer = bot.ask(question)
                    print(f"\nОтвет: {answer}")
            except ValueError as e:
                print(f"\nОшибка: {e}")
            except KeyboardInterrupt:
                print("\n\nПока")
                break
            except Exception as e:
                print(f"\nОшибка: {e}")

    except Exception as e:
        print(f"Ошибка инициализации: {e}")
        print("\nВозможные решения:")
        print("1. Убедитесь что база данных создана: docker compose --profile index up index-builder")
        print("2. Проверьте наличие папки starwars_pages с txt файлами")

    input("\nНажмите Enter для выхода")


if __name__ == "__main__":
    main()
