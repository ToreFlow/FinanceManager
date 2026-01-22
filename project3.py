import datetime

records = []
expense_categories = {"Еда", "Транспорт", "Развлечения"}

def add():
    try:
        amount = float(input("Сумма: "))
        if amount <= 0:
            print("Сумма > 0"); return
    except:
        print("Неверная сумма"); return

    is_income = input("Доход(d)/Расход(e): ").lower() == 'd'
    record_type = "Доход" if is_income else "Расход"

    category = None
    if is_income:
        cat_input = input("Категория дохода (Enter — пропустить): ").strip()
        category = cat_input if cat_input else None
    else:
        print("Категории расходов:", ", ".join(sorted(expense_categories)))
        cat_input = input("Категория расхода (можно новую): ").strip()
        if not cat_input:
            print("Категория обязательна для расхода"); return
        category = cat_input
        expense_categories.add(category)  # Авто-добавление новой категории расхода

    date_str = input("Дата (ГГГГ-ММ-ДД, Enter=сегодня): ").strip()
    date = datetime.date.today() if not date_str else datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    desc = input("Описание: ").strip()

    records.append({
        "amount": amount,
        "type": record_type,
        "category": category,
        "date": date,
        "desc": desc
    })
    print("Запись добавлена")

def balance():
    inc = sum(r["amount"] for r in records if r["type"] == "Доход")
    exp = sum(r["amount"] for r in records if r["type"] == "Расход")
    print(f"\nБаланс: {inc - exp:.2f} | Доходы: {inc:.2f}, Расходы: {exp:.2f}")

def view():
    if not records:
        print("\nНет записей"); return
    s = input("Начало (ГГГГ-ММ-ДД): ").strip()
    e = input("Конец (ГГГГ-ММ-ДД): ").strip()
    cat = input("Категория (оставьте пустым для всех): ").strip()
    start = datetime.datetime.strptime(s, "%Y-%m-%d").date() if s else None
    end = datetime.datetime.strptime(e, "%Y-%m-%d").date() if e else None

    filtered = []
    for r in records:
        if start and r["date"] < start: continue
        if end and r["date"] > end: continue
        if cat and r["category"] != cat: continue  # Теперь фильтр работает и для доходов!
        filtered.append(r)

    if not filtered:
        print("Нет совпадений"); return
    for i, r in enumerate(filtered, 1):
        cat_part = f" | {r['category']}" if r["category"] is not None else ""
        print(f"{i}. [{r['date']}] {r['type']}{cat_part} | {r['amount']:.2f}" + (f" — {r['desc']}" if r['desc'] else ""))

def analyze():
    exp_by_cat = {}
    total_exp = 0.0
    for r in records:
        if r["type"] == "Расход":
            c = r["category"]
            exp_by_cat[c] = exp_by_cat.get(c, 0) + r["amount"]
            total_exp += r["amount"]
    if not exp_by_cat:
        print("\nНет расходов"); return
    print("\n--- Анализ расходов ---")
    for cat, amt in sorted(exp_by_cat.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {amt:.2f} ({amt/total_exp*100:.1f}%)")
    top = max(exp_by_cat, key=exp_by_cat.get)
    inc = sum(r["amount"] for r in records if r["type"] == "Доход")
    print(f"\nТоп-категория расходов: {top}")
    print(f"Соотношение расходов/доходов: {total_exp/inc:.2f}" if inc else "Доходы = 0")

def main():
    while True:
        print("\n1. Добавить  2. Баланс  3. Просмотр  4. Анализ  5. Выход")
        c = input("Выбор: ")
        if c == '1': add()
        elif c == '2': balance()
        elif c == '3': view()
        elif c == '4': analyze()
        elif c == '5': break
        else: print("Неверно")

if __name__ == "__main__":
    main()