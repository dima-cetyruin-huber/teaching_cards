import json
import os

# Таблица интервалов повторения для ступеней (повторы)
INTERVALS = {1: 1, 2: 2, 3: 4, 4: 7}
MAX_LEVEL = 4 # Некий "потолок"


def form_review_queue(cards, current_day, intervals):
    """Основной алгоритм: отбор карточек по интервалам и сортировка."""
    queue = []
    for card in cards:
        level = card.get('level')
        if level not in intervals:
            continue

        # Вычисляем день следующего повторения
        next_review = card['last_day'] + intervals[level]

        # Правило границы: если день наступил или прошел
        if next_review <= current_day:
            queue.append(card.copy())

    # Упорядочиваем по дате последнего повторения (от старых к новым)
    queue.sort(key=lambda x: x['last_day'])
    return queue


def main():
    current_day = 5  # Текущий учебный день для теста
    input_path = "cards.json"
    output_queue_path = "daily_queue.txt"
    output_updated_path = "cards_updated.json"

    print(f"=== Запуск программы формирования очереди (День {current_day}) ===")

    # 1. Чтение и валидация данных
    if not os.path.exists(input_path):
        print(f"[Ошибка] Файл данных {input_path} не найден!")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        try:
            cards = json.load(f)
        except json.JSONDecodeError:
            print("[Ошибка] Неверный формат JSON во входном файле!")
            return

    # 2. Выполнение предметного алгоритма
    queue = form_review_queue(cards, current_day, INTERVALS)

    # 3. Демонстрация результата на экране (Консольный вывод)
    print("\n[РЕЗУЛЬТАТ] Карточки, готовые к повторению на сегодня:")
    print("-" * 65)
    print(f"{'ID':<10} | {'Термин':<20} | {'Текущая ступень':<16} | {'День посл. повт.':<15}")
    print("-" * 65)

    if not queue:
        print(" Очередь пуста. Нет карточек для повторения на сегодня.")
    else:
        for card in queue:
            print(f"{card['id']:<10} | {card['term']:<20} | {card['level']:<16} | {card['last_day']:<15}")
    print("-" * 65)

    # 4. Сохранение результатов в файлы
    # Файл А: Текстовый протокол сегодняшней очереди для пользователя
    with open(output_queue_path, "w", encoding="utf-8") as f:
        f.write(f"Очередь повторения на день {current_day}\n")
        f.write("=" * 40 + "\n")
        for card in queue:
            f.write(f"ID: {card['id']} | Термин: {card['term']}\n")

    print(f"[Успех] Список текущей очереди сохранён в: {output_queue_path}")

    # 5 Симуляция ответов (для демонстрации обновления данных)
    # Предположим, студент ответил на первую карту в очереди верно, на вторую — неверно
    updated_cards = {c['id']: c.copy() for c in cards}

    if len(queue) > 0:
        # Первая карта отвечена ВЕРНО -> уровень растет
        c1_id = queue[0]['id']
        updated_cards[c1_id]['level'] = min(updated_cards[c1_id]['level'] + 1, MAX_LEVEL)
        updated_cards[c1_id]['last_day'] = current_day
        print(f"\n[Имитация] На карту {c1_id} дан ВЕРНЫЙ ответ. Ступень повышена.")

    if len(queue) > 1:
        # Вторая карта отвечена НЕВЕРНО -> сброс на уровень 1
        c2_id = queue[1]['id']
        updated_cards[c2_id]['level'] = 1
        updated_cards[c2_id]['last_day'] = current_day
        print(f"[Имитация] На карту {c2_id} дан НЕВЕРНЫЙ ответ. Ступень сброшена до 1.")

    # Файл Б: Сохранение обновленной базы данных карточек
    with open(output_updated_path, "w", encoding="utf-8") as f:
        json.dump(list(updated_cards.values()), f, ensure_ascii=False, indent=2)

    print(f"[Успех] Обновлённый статус всех карточек сохранён в: {output_updated_path}")


if __name__ == "__main__":
    main()