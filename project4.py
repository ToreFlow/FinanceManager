import datetime

class FinanceManager:
    def __init__(self):
        self.records = []
        self.categories = {"Еда", "Транспорт", "Развлечения"}

    def add_record(self):
        print("\n--- Добавление записи ---")
        try:
            amount = float(input("Введите сумму: "))
            if amount <= 0:
                print("Сумма должна быть положительной.")
                return
        except ValueError:
            print("Некорректная сумма.")
            return

        type_ = input("Доход (d) или Расход (e)? ").strip().lower()
        if type_ not in ('d', 'e'):
            print("Неверный тип. Используйте 'd' для дохода или 'e' для расхода.")
            return
        record_type = "Доход" if type_ == 'd' else "Расход"

        print("Доступные категории:", ", ".join(sorted(self.categories)))
        category = input("Введите категорию (или новую): ").strip()
        if not category:
            print("Категория не может быть пустой.")
            return
        self.categories.add(category)

        date_str = input("Введите дату (ГГГГ-ММ-ДД) или оставьте пустым для сегодняшней: ").strip()
        if not date_str:
            date = datetime.date.today()
        else:
            try:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print("Неверный формат даты. Используйте ГГГГ-ММ-ДД.")
                return

        description = input("Описание (опционально): ").strip()

        self.records.append({
            "amount": amount,
            "type": record_type,
            "category": category,
            "date": date,
            "description": description
        })
        print("Запись добавлена.")

    def get_balance(self):
        total_income = sum(r["amount"] for r in self.records if r["type"] == "Доход")
        total_expense = sum(r["amount"] for r in self.records if r["type"] == "Расход")
        balance = total_income - total_expense
        print(f"\nИтоговый баланс: {balance:.2f}")
        print(f"Доходы: {total_income:.2f}, Расходы: {total_expense:.2f}")

    def view_records(self):
        if not self.records:
            print("\nНет записей.")
            return

        print("\n--- Фильтрация записей ---")
        start_date_str = input("Начальная дата (ГГГГ-ММ-ДД, опционально): ").strip()
        end_date_str = input("Конечная дата (ГГГГ-ММ-ДД, опционально): ").strip()
        category_filter = input("Категория (опционально): ").strip()

        start_date = None
        end_date = None

        if start_date_str:
            try:
                start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            except ValueError:
                print("Неверный формат начальной даты.")
                return
        if end_date_str:
            try:
                end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
            except ValueError:
                print("Неверный формат конечной даты.")
                return

        filtered = []
        for r in self.records:
            if start_date and r["date"] < start_date:
                continue
            if end_date and r["date"] > end_date:
                continue
            if category_filter and r["category"] != category_filter:
                continue
            filtered.append(r)

        if not filtered:
            print("Нет записей по заданным фильтрам.")
            return

        print(f"\nНайдено записей: {len(filtered)}")
        for i, r in enumerate(filtered, 1):
            desc = f" — {r['description']}" if r['description'] else ""
            print(f"{i}. [{r['date']}] {r['type']} | {r['category']} | {r['amount']:.2f}{desc}")

    def analyze_expenses(self):
        expenses_by_cat = {}
        total_expense = 0.0

        for r in self.records:
            if r["type"] == "Расход":
                cat = r["category"]
                if cat in expenses_by_cat:
                    expenses_by_cat[cat] += r["amount"]
                else:
                    expenses_by_cat[cat] = r["amount"]
                total_expense += r["amount"]

        if not expenses_by_cat:
            print("\nНет данных о расходах для анализа.")
            return

        print("\n--- Анализ расходов ---")
        sorted_categories = sorted(expenses_by_cat.items(), key=lambda x: x[1], reverse=True)
        print("Расходы по категориям:")
        for cat, amount in sorted_categories:
            percent = (amount / total_expense * 100) if total_expense > 0 else 0
            print(f"  {cat}: {amount:.2f} ({percent:.1f}%)")

        top_category = max(expenses_by_cat, key=expenses_by_cat.get)
        print(f"\nТоп-категория расходов: {top_category} ({expenses_by_cat[top_category]:.2f})")

        total_income = sum(r["amount"] for r in self.records if r["type"] == "Доход")
        if total_income > 0:
            ratio = total_expense / total_income
            print(f"\nСоотношение расходов к доходам: {ratio:.2f} (расходы / доходы)")
        else:
            print("\nСоотношение расходов к доходам: невозможно рассчитать (доходы = 0)")

    def run(self):
        while True:
            print("\n=== Учёт личных финансов ===")
            print("1. Добавить запись")
            print("2. Показать баланс")
            print("3. Просмотр записей")
            print("4. Анализ расходов")
            print("5. Выход")
            choice = input("Выберите действие: ").strip()

            if choice == '1':
                self.add_record()
            elif choice == '2':
                self.get_balance()
            elif choice == '3':
                self.view_records()
            elif choice == '4':
                self.analyze_expenses()
            elif choice == '5':
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    app = FinanceManager()
    app.run()