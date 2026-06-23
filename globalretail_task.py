# ============================================================
#  GlobalRetail – מבחן קוד מעשי
#  קובץ: globalretail_task.py
#  הרצה: python globalretail_task.py
#  פלט:  output.txt (יישמר באותה תיקייה)
# ============================================================
# דרישות: Python 3 בלבד, ספריית csv ו-collections מובנות.
# אין צורך להתקין חבילות חיצוניות.
# ============================================================

import csv
import os
from collections import defaultdict

INPUT_FILE = "sales_data.csv"
OUTPUT_FILE = "output.txt"

lines = []


def log(text=""):
    """הדפסה למסך ושמירה לרשימה"""
    print(text)
    lines.append(text)


# ============================================================
# עזר – המרת ערך למספר עשרוני, עם טיפול בשגיאות
# ============================================================
def to_float(value):
    """
    ממירה מחרוזת למספר עשרוני.
    מחזירה None אם הערך חסר, לא-מספרי, או שלילי (עסקאות לא תקינות).

    TODO: השלימי את הפונקציה.
    כרגע היא תמיד מחזירה None – יש לתקן.
    """
    if value is None or value == "" or value == "N/A":
        return None
    
    try:
        num = float(value)
        if num < 0:
            return None
        return num
    except ValueError:
        return None


# ============================================================
# שאלה 6 – פילטר, ניתוח וסיכום לפי קטגוריה
# ============================================================
def analyze_sales(rows):
    """
    מקבלת רשימת שורות CSV (כל שורה היא dict).
    מבצעת:
      1. סינון שורות עם Total_Amount לא תקין (ע"י to_float).
      2. מיון השורות לפי Total_Amount מהגבוה לנמוך.
      3. מיון השורות לפי Profit_Margin מהגבוה לנמוך.
      4. חישוב סכום ומיצוע Total_Amount לפי Category.
      5. יצירת עמודה Gross_Profit = Total_Amount * Profit_Margin לכל שורה תקינה.
      6. מיון הקטגוריות לפי סך Gross_Profit וכתיבה לפלט.

    TODO: השלימי את כל הסעיפים.
    """
    log("=" * 60)
    log("שאלה 6 – ניתוח מכירות")
    log("=" * 60)

    # --- שלב 1: סינון שורות לא תקינות ---
    valid_rows = []
    skipped = 0
    for row in rows:
        amount = to_float(row.get("Total_Amount", ""))
        margin = to_float(row.get("Profit_Margin", ""))
        if amount is None or margin is None:
            skipped += 1
            continue
        row["_amount"] = amount
        row["_margin"] = margin
        valid_rows.append(row)

    log(f"\nסה\"כ שורות בקובץ:   {len(rows)}")
    log(f"שורות תקינות:        {len(valid_rows)}")
    log(f"שורות שדולגו:        {skipped}")

    # --- שלב 2: מיון לפי Total_Amount ---
    log("\n--- מיון לפי Total_Amount (גבוה ← נמוך) ---")
    sorted_by_amount = sorted(valid_rows, key=lambda x: x["_amount"], reverse=True)
    for r in sorted_by_amount[:5]:
        log(f"  {r['Category']:<15}  Total_Amount: {r['_amount']:>10.2f}")

    # --- שלב 3: מיון לפי Profit_Margin ---
    log("\n--- מיון לפי Profit_Margin (גבוה ← נמוך) ---")
    sorted_by_margin = sorted(valid_rows, key=lambda x: x["_margin"], reverse=True)
    for r in sorted_by_margin[:5]:
        log(f"  {r['Category']:<15}  Profit_Margin: {r['_margin']:>6.2f}")

    # --- שלב 4: סכום ומיצוע לפי קטגוריה ---
    log("\n--- סכום ומיצוע Total_Amount לפי Category ---")
    category_totals = defaultdict(float)
    category_counts = defaultdict(int)
    for row in valid_rows:
        cat = row["Category"]
        category_totals[cat] += row["_amount"]
        category_counts[cat] += 1

    for cat in sorted(category_totals):
        avg = category_totals[cat] / category_counts[cat] if category_counts[cat] else 0
        log(f"  {cat:<15} סכום: {category_totals[cat]:>10.2f}   מיצוע: {avg:>8.2f}")

    # --- שלב 5 + 6: Gross_Profit לפי קטגוריה ---
    log("\n--- דירוג קטגוריות לפי Gross_Profit כולל ---")
    category_profit = defaultdict(float)
    for row in valid_rows:
        gross = row["_amount"] * row["_margin"]
        category_profit[row["Category"]] += gross

    sorted_cats = sorted(category_profit.items(), key=lambda x: x[1], reverse=True)
    for rank, (cat, profit) in enumerate(sorted_cats, 1):
        log(f"  #{rank}  {cat:<15}  Gross Profit: {profit:>10.2f}")

    return valid_rows


# ============================================================
# שאלה 7 (בונוס) – ניקוי ועיבוד שגיאות נתונים
# ============================================================
def clean_and_report(rows):
    """
    מזהה ומדווחת על בעיות איכות נתונים בקובץ.

    TODO: השלימי את הפונקציה.
    יש לזהות ולדווח על:
      - ערכים חסרים (ריק / None / N/A) בעמודות Total_Amount ו-Profit_Margin
      - ערכים שליליים ב-Total_Amount
      - עמודות לא צפויות (אם יש)
    """
    log("\n" + "=" * 60)
    log("שאלה 7 (בונוס) – ניקוי ואיכות נתונים")
    log("=" * 60)

    missing_amount = 0
    missing_margin = 0
    negative_amount = 0
    unexpected_columns = 0
    
    for row in rows:
        amount_value = row.get("Total_Amount", "")
        margin_value = row.get("Profit_Margin", "")
        
        if amount_value is None or amount_value == "" or amount_value == "N/A":
            missing_amount += 1
        else:
            try:
                amount_num = float(amount_value)
                if amount_num < 0:
                    negative_amount += 1
            except ValueError:
                pass
        
        if margin_value is None or margin_value == "" or margin_value == "N/A":
            missing_margin += 1
        
        if None in row:
            unexpected_columns += 1

    log(f"\nערכים חסרים ב-Total_Amount:    {missing_amount}")
    log(f"ערכים חסרים ב-Profit_Margin:   {missing_margin}")
    log(f"ערכים שליליים ב-Total_Amount:  {negative_amount}")
    log(f"שורות עם עמודות לא צפויות:     {unexpected_columns}")
    
    total_issues = missing_amount + missing_margin + negative_amount + unexpected_columns
    log(f"\nסה\"כ בעיות איכות נתונים:       {total_issues}")
    
    if total_issues > 0:
        log("\nסיכום בעיות:")
        if missing_amount > 0:
            log(f"  - {missing_amount} שורות עם Total_Amount חסר")
        if missing_margin > 0:
            log(f"  - {missing_margin} שורות עם Profit_Margin חסר")
        if negative_amount > 0:
            log(f"  - {negative_amount} שורות עם Total_Amount שלילי (עסקאות לא תקינות)")
        if unexpected_columns > 0:
            log(f"  - {unexpected_columns} שורות עם עמודות לא צפויות")
        log("\nהמלצה: יש לנקות את הנתונים ולתקן את השורות הבעייתיות לפני ניתוח נוסף.")
    else:
        log("\nאיכות הנתונים: מצוינת - לא נמצאו בעיות.")


# ============================================================
# ריצה ראשית
# ============================================================
def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(script_dir, INPUT_FILE)
    output_path = os.path.join(script_dir, OUTPUT_FILE)

    if not os.path.exists(input_path):
        print(f"שגיאה: הקובץ {INPUT_FILE} לא נמצא. וודאי ששני הקבצים באותה תיקייה.")
        return

    with open(input_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    log("GlobalRetail – תוצאות מבחן קוד")
    log(f"קובץ קלט: {INPUT_FILE}  |  שורות: {len(rows)}")

    valid_rows = analyze_sales(rows)
    clean_and_report(rows)

    log("\n" + "=" * 60)
    log("סיום הרצה")
    log("=" * 60)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n✓ הפלט נשמר ב: {output_path}")
    print("  שלחי את הקובץ output.txt במייל חוזר יחד עם קובץ ה-Python שכתבת.")


if __name__ == "__main__":
    main()
