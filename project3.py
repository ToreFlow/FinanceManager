import datetime

records = []
categories = {"Еда", "Транспорт", "Развлечения"}

def add():
    try:
        a = float(input("Сумма: "))
        if a <= 0: return
    except:
        print("Неверная сумма"); return
    t = "Доход" if input("Доход(d)/Расход(e): ").lower() == 'd' else "Расход"
    c = input(f"Категория ({', '.join(sorted(categories))}): ").strip()
    if not c: return
    categories.add(c)
    d = input("Дата (ГГГГ-ММ-ДД, Enter=сегодня): ").strip()
    date = datetime.date.today() if not d else datetime.datetime.strptime(d, "%Y-%m-%d").date()
    desc = input("Описание: ").strip()
    records.append({"amount": a, "type": t, "category": c, "date": date, "desc": desc})
    print("Добавлено")

def balance():
    inc = sum(r["amount"] for r in records if r["type"] == "Доход")
    exp = sum(r["amount"] for r in records if r["type"] == "Расход")
    print(f"\nБаланс: {inc - exp:.2f} | Доходы: {inc:.2f}, Расходы: {exp:.2f}")

def view():
    if not records: print("\nНет записей"); return
    s = input("Начало (ГГГГ-ММ-ДД): ").strip()
    e = input("Конец (ГГГГ-ММ-ДД): ").strip()
    cat = input("Категория: ").strip()
    start = datetime.datetime.strptime(s, "%Y-%m-%d").date() if s else None
    end = datetime.datetime.strptime(e, "%Y-%m-%d").date() if e else None
    f = [r for r in records if
         (not start or r["date"] >= start) and
         (not end or r["date"] <= end) and
         (not cat or r["category"] == cat)]
    if not f: print("Нет совпадений"); return
    for i, r in enumerate(f, 1):
        print(f"{i}. [{r['date']}] {r['type']} | {r['category']} | {r['amount']:.2f}" + (f" — {r['desc']}" if r['desc'] else ""))

def analyze():
    exp_by_cat = {}
    total_exp = 0
    for r in records:
        if r["type"] == "Расход":
            cat = r["category"]
            exp_by_cat[cat] = exp_by_cat.get(cat, 0) + r["amount"]
            total_exp += r["amount"]
    if not exp_by_cat: print("\nНет расходов"); return
    print("\n--- Анализ ---")
    for cat, amt in sorted(exp_by_cat.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {amt:.2f} ({amt/total_exp*100:.1f}%)")
    top = max(exp_by_cat, key=exp_by_cat.get)
    inc = sum(r["amount"] for r in records if r["type"] == "Доход")
    print(f"\nТоп: {top}")
    print(f"Соотношение: {total_exp/inc:.2f}" if inc else "Доходы = 0")

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