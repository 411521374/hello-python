"""Multilingual BMI / IMT Calculator Script (English, Bahasa Indonesia, 日本語).
Kalkulator Indeks Massa Tubuh (IMT / BMI) Multibahasa.
多言語対応 BMI（体格指数）計算スクリプト。

Supports:
- Three languages: English, Bahasa Indonesia, and 日本語 (Japanese)
- Two measurement systems: Metric (kg, cm/m) & Imperial/English (lbs, ft/in)
- Interactive console prompt & Command-Line Arguments
- Healthy weight range calculation in corresponding units
"""

from __future__ import annotations

import argparse
import sys
from typing import Tuple

# Ensure stdout and stderr handle UTF-8 properly on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


TRANSLATIONS = {
    "en": {
        "title": "BMI CALCULATOR (BODY MASS INDEX)",
        "select_lang": "Select Language / Pilih Bahasa / 言語を選択:",
        "lang_option_en": "1. English",
        "lang_option_id": "2. Bahasa Indonesia",
        "lang_option_ja": "3. 日本語 (Japanese)",
        "prompt_lang": "Enter choice (1, 2, or 3) [default: 1]: ",
        "select_unit": "Select Unit System:",
        "metric_option": "1. Metric (kilograms, meters / centimeters)",
        "imperial_option": "2. Imperial / English (pounds, feet and inches)",
        "prompt_unit": "Enter choice (1 or 2) [default: 1]: ",
        "prompt_weight_lbs": "Enter weight in pounds (lbs): ",
        "prompt_height_ft": "Enter height (feet): ",
        "prompt_height_in": "Enter remaining height (inches): ",
        "prompt_weight_kg": "Enter weight in kilograms (kg): ",
        "prompt_height_metric": "Enter height (in meters e.g. 1.75, or cm e.g. 175): ",
        "invalid_number": "Error: Please enter a valid positive number.",
        "negative_error": "Value must be strictly greater than zero.",
        "results_title": "BMI CALCULATION RESULTS",
        "height_label": "Height",
        "weight_label": "Weight",
        "bmi_label": "BMI Value",
        "category_label": "Category",
        "healthy_range_label": "Healthy weight range for this height",
        "cat_underweight": "Underweight (< 18.5)",
        "cat_normal": "Normal weight (18.5 - 24.9)",
        "cat_overweight": "Overweight (25.0 - 29.9)",
        "cat_obese1": "Obesity Class 1 - Moderate (30.0 - 34.9)",
        "cat_obese2": "Obesity Class 2 - Severe (35.0 - 39.9)",
        "cat_obese3": "Obesity Class 3 - Very severe / Morbid (>= 40.0)",
    },
    "id": {
        "title": "KALKULATOR IMT / BMI (INDEKS MASSA TUBUH)",
        "select_lang": "Pilih Bahasa / Select Language / 言語を選択:",
        "lang_option_en": "1. English",
        "lang_option_id": "2. Bahasa Indonesia",
        "lang_option_ja": "3. 日本語 (Japanese)",
        "prompt_lang": "Masukkan pilihan (1, 2, atau 3) [standar: 2]: ",
        "select_unit": "Pilih Sistem Satuan:",
        "metric_option": "1. Metrik (kilogram, meter / sentimeter)",
        "imperial_option": "2. Imperial / English (pon/lbs, kaki/feet dan inci)",
        "prompt_unit": "Masukkan pilihan (1 atau 2) [standar: 1]: ",
        "prompt_weight_lbs": "Masukkan berat badan dalam pon (lbs): ",
        "prompt_height_ft": "Masukkan tinggi badan (kaki / feet): ",
        "prompt_height_in": "Masukkan sisa tinggi badan (inci / inches): ",
        "prompt_weight_kg": "Masukkan berat badan dalam kilogram (kg): ",
        "prompt_height_metric": "Masukkan tinggi badan (dalam meter contoh: 1.75, atau cm contoh: 175): ",
        "invalid_number": "Kesalahan: Harap masukkan angka positif yang valid.",
        "negative_error": "Nilai harus lebih besar dari nol.",
        "results_title": "HASIL PERHITUNGAN IMT / BMI",
        "height_label": "Tinggi Badan",
        "weight_label": "Berat Badan",
        "bmi_label": "Nilai IMT / BMI",
        "category_label": "Kategori",
        "healthy_range_label": "Rentang berat badan sehat untuk tinggi ini",
        "cat_underweight": "Berat Badan Kurang / Kurus (< 18.5)",
        "cat_normal": "Berat Badan Normal / Ideal (18.5 - 24.9)",
        "cat_overweight": "Berat Badan Berlebih (25.0 - 29.9)",
        "cat_obese1": "Obesitas Tingkat 1 - Sedang (30.0 - 34.9)",
        "cat_obese2": "Obesitas Tingkat 2 - Berat (35.0 - 39.9)",
        "cat_obese3": "Obesitas Tingkat 3 - Sangat Berat / Morbid (>= 40.0)",
    },
    "ja": {
        "title": "BMI 計算機（体格指数）",
        "select_lang": "言語を選択してください / Select Language / Pilih Bahasa:",
        "lang_option_en": "1. English (英語)",
        "lang_option_id": "2. Bahasa Indonesia (インドネシア語)",
        "lang_option_ja": "3. 日本語 (Japanese)",
        "prompt_lang": "番号を入力してください (1, 2, または 3) [初期値: 3]: ",
        "select_unit": "単位系を選択してください:",
        "metric_option": "1. メートル法 (キログラム, メートル / センチメートル)",
        "imperial_option": "2. ヤード・ポンド法 (ポンド, フィート / インチ)",
        "prompt_unit": "番号を入力してください (1 または 2) [初期値: 1]: ",
        "prompt_weight_lbs": "体重を入力してください (ポンド / lbs): ",
        "prompt_height_ft": "身長を入力してください (フィート / ft): ",
        "prompt_height_in": "残りの身長を入力してください (インチ / in): ",
        "prompt_weight_kg": "体重を入力してください (キログラム / kg): ",
        "prompt_height_metric": "身長を入力してください (メートル 例: 1.75、またはセンチメートル 例: 175): ",
        "invalid_number": "エラー: 有効な正の数値を入力してください。",
        "negative_error": "値は0より大きい必要があります。",
        "results_title": "BMI 計算結果",
        "height_label": "身長",
        "weight_label": "体重",
        "bmi_label": "BMI値",
        "category_label": "判定結果",
        "healthy_range_label": "適正体重範囲（普通体重）",
        "cat_underweight": "低体重（やせ型） (< 18.5)",
        "cat_normal": "普通体重（適正体重） (18.5 - 24.9)",
        "cat_overweight": "肥満（1度） / 過体重 (25.0 - 29.9)",
        "cat_obese1": "肥満（2度） / 中度肥満 (30.0 - 34.9)",
        "cat_obese2": "肥満（3度） / 重度肥満 (35.0 - 39.9)",
        "cat_obese3": "肥満（4度 / 高度肥満） (>= 40.0)",
    },
}


def calculate_bmi_metric(weight_kg: float, height_m: float) -> float:
    """Calculate BMI using metric units (kg, meters)."""
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    if weight_kg <= 0:
        raise ValueError("Weight must be greater than zero.")
    return weight_kg / (height_m ** 2)


def calculate_bmi_english(weight_lbs: float, height_inches: float) -> float:
    """Calculate BMI using English / Imperial units (lbs, inches)."""
    if height_inches <= 0:
        raise ValueError("Height must be greater than zero.")
    if weight_lbs <= 0:
        raise ValueError("Weight must be greater than zero.")
    return (weight_lbs * 703.0) / (height_inches ** 2)


def get_bmi_category(bmi: float, lang: str = "en") -> str:
    """Return the BMI category for a given BMI in the selected language."""
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    if bmi < 18.5:
        return t["cat_underweight"]
    elif bmi < 25.0:
        return t["cat_normal"]
    elif bmi < 30.0:
        return t["cat_overweight"]
    elif bmi < 35.0:
        return t["cat_obese1"]
    elif bmi < 40.0:
        return t["cat_obese2"]
    else:
        return t["cat_obese3"]


def get_healthy_weight_range_metric(height_m: float) -> Tuple[float, float]:
    """Calculate healthy weight range (BMI 18.5 - 24.9) in kilograms."""
    if height_m <= 0:
        raise ValueError("Height must be greater than zero.")
    return 18.5 * (height_m ** 2), 24.9 * (height_m ** 2)


def get_healthy_weight_range_english(height_inches: float) -> Tuple[float, float]:
    """Calculate healthy weight range (BMI 18.5 - 24.9) in pounds."""
    if height_inches <= 0:
        raise ValueError("Height must be greater than zero.")
    return (18.5 * (height_inches ** 2)) / 703.0, (24.9 * (height_inches ** 2)) / 703.0


def display_results_metric(weight_kg: float, height_m: float, bmi: float, lang: str = "en") -> None:
    """Display calculation results for metric units."""
    t = TRANSLATIONS[lang]
    category = get_bmi_category(bmi, lang=lang)
    min_w, max_w = get_healthy_weight_range_metric(height_m)

    print("\n" + "=" * 55)
    print(f"       {t['results_title']}")
    print("=" * 55)
    print(f"  {t['height_label']:<15}: {height_m:.2f} m ({height_m * 100:.1f} cm)")
    print(f"  {t['weight_label']:<15}: {weight_kg:.1f} kg")
    print(f"  {t['bmi_label']:<15}: {bmi:.2f}")
    print(f"  {t['category_label']:<15}: {category}")
    print(f"  {t['healthy_range_label']}: {min_w:.1f} kg - {max_w:.1f} kg")
    print("=" * 55)


def display_results_english(weight_lbs: float, height_inches: float, bmi: float, lang: str = "en") -> None:
    """Display calculation results for English / imperial units."""
    t = TRANSLATIONS[lang]
    feet = int(height_inches // 12)
    inches = height_inches % 12
    category = get_bmi_category(bmi, lang=lang)
    min_w, max_w = get_healthy_weight_range_english(height_inches)

    print("\n" + "=" * 55)
    print(f"       {t['results_title']}")
    print("=" * 55)
    if feet > 0:
        print(f"  {t['height_label']:<15}: {feet} ft {inches:.1f} in ({height_inches:.1f} in)")
    else:
        print(f"  {t['height_label']:<15}: {height_inches:.1f} in")
    print(f"  {t['weight_label']:<15}: {weight_lbs:.1f} lbs")
    print(f"  {t['bmi_label']:<15}: {bmi:.2f}")
    print(f"  {t['category_label']:<15}: {category}")
    print(f"  {t['healthy_range_label']}: {min_w:.1f} lbs - {max_w:.1f} lbs")
    print("=" * 55)


def prompt_positive_float(prompt_text: str, err_text: str) -> float:
    """Prompt user repeatedly until a positive float is provided."""
    while True:
        raw_val = input(prompt_text).strip()
        try:
            val = float(raw_val)
            if val <= 0:
                print(f"  [!] {err_text}")
                continue
            return val
        except ValueError:
            print(f"  [!] {err_text}")


def run_interactive(lang: str | None = None) -> None:
    """Interactive session supporting language and unit selection."""
    if not lang or lang not in TRANSLATIONS:
        print("=" * 55)
        print("  Select Language / Pilih Bahasa / 言語を選択:")
        print("    1. English")
        print("    2. Bahasa Indonesia")
        print("    3. 日本語 (Japanese)")
        choice = input("\n  Enter choice / 選択 (1, 2, 3) [default: 1]: ").strip()
        if choice == "3":
            lang = "ja"
        elif choice == "2":
            lang = "id"
        else:
            lang = "en"

    t = TRANSLATIONS[lang]

    print("\n" + "=" * 55)
    print(f"        {t['title']}")
    print("=" * 55)
    print(f"  {t['select_unit']}")
    print(f"    {t['metric_option']}")
    print(f"    {t['imperial_option']}")

    unit_choice = input(f"\n  {t['prompt_unit']}").strip() or "1"

    if unit_choice == "2":
        # Imperial / English Units
        try:
            weight_lbs = prompt_positive_float(f"  {t['prompt_weight_lbs']}", t["invalid_number"])
            while True:
                try:
                    feet_input = input(f"  {t['prompt_height_ft']}").strip()
                    feet = float(feet_input)
                    if feet < 0:
                        print(f"  [!] {t['invalid_number']}")
                        continue

                    inches_input = input(f"  {t['prompt_height_in']}").strip()
                    inches = float(inches_input)
                    if inches < 0:
                        print(f"  [!] {t['invalid_number']}")
                        continue

                    total_inches = (feet * 12.0) + inches
                    if total_inches <= 0:
                        print(f"  [!] {t['invalid_number']}")
                        continue
                    break
                except ValueError:
                    print(f"  [!] {t['invalid_number']}")

            bmi = calculate_bmi_english(weight_lbs, total_inches)
            display_results_english(weight_lbs, total_inches, bmi, lang=lang)
        except (ValueError, KeyboardInterrupt):
            print(f"\n{t['invalid_number']}")
    else:
        # Metric Units
        try:
            weight_kg = prompt_positive_float(f"  {t['prompt_weight_kg']}", t["invalid_number"])
            height_input = prompt_positive_float(f"  {t['prompt_height_metric']}", t["invalid_number"])
            # If height entered is > 3, assume centimeters (e.g. 175 cm -> 1.75 m)
            height_m = height_input / 100.0 if height_input > 3.0 else height_input

            bmi = calculate_bmi_metric(weight_kg, height_m)
            display_results_metric(weight_kg, height_m, bmi, lang=lang)
        except (ValueError, KeyboardInterrupt):
            print(f"\n{t['invalid_number']}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Multilingual BMI / IMT Calculator (English, Bahasa Indonesia, 日本語).",
        epilog="Examples:\n"
               "  python bmi_calculator.py --lang ja\n"
               "  python bmi_calculator.py --lang ja --weight 65 --height 170\n"
               "  python bmi_calculator.py --lang en --weight 160 --feet 5 --inches 10 --imperial\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--lang",
        choices=["en", "id", "ja"],
        help="Language preference: 'en' for English, 'id' for Indonesian, 'ja' for Japanese",
    )
    parser.add_argument(
        "-w", "--weight",
        type=float,
        help="Body weight (kg by default, or lbs if --imperial is passed)",
    )
    parser.add_argument(
        "-H", "--height",
        type=float,
        help="Height (in meters or cm if > 3; in inches if --imperial is passed)",
    )
    parser.add_argument(
        "--feet",
        type=float,
        default=0.0,
        help="Height feet component (for imperial)",
    )
    parser.add_argument(
        "--inches",
        type=float,
        default=0.0,
        help="Height inches component (added to --feet for imperial)",
    )
    parser.add_argument(
        "--imperial",
        action="store_true",
        help="Use English / Imperial units (pounds and inches)",
    )

    args = parser.parse_args()
    lang = args.lang if args.lang else "en"

    if args.weight is not None:
        if args.imperial:
            height_in = args.height if args.height is not None else ((args.feet * 12.0) + args.inches)
            if height_in <= 0:
                print("Error: Height must be greater than zero.", file=sys.stderr)
                sys.exit(1)
            bmi = calculate_bmi_english(args.weight, height_in)
            display_results_english(args.weight, height_in, bmi, lang=lang)
        else:
            if args.height is None or args.height <= 0:
                print("Error: Height must be specified and greater than zero.", file=sys.stderr)
                sys.exit(1)
            height_m = args.height / 100.0 if args.height > 3.0 else args.height
            bmi = calculate_bmi_metric(args.weight, height_m)
            display_results_metric(args.weight, height_m, bmi, lang=lang)
    else:
        run_interactive(lang=args.lang)


if __name__ == "__main__":
    main()
