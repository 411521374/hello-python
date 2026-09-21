"""
Bilingual BMI / IMT Calculator Script (English & Bahasa Indonesia)
Kalkulator Indeks Massa Tubuh (IMT / BMI) Bilingual (Bahasa Inggris & Bahasa Indonesia)

Supports both metric (kg, meters/cm) and imperial (lbs, feet/inches) units,
via either interactive prompts or command-line arguments.
"""

import argparse
import sys

TRANSLATIONS = {
    "en": {
        "title": "BMI CALCULATOR",
        "select_unit": "Select unit system:",
        "metric_option": "1. Metric (kilograms, meters or centimeters)",
        "imperial_option": "2. Imperial (pounds, feet and inches)",
        "prompt_unit": "Enter choice (1 or 2) [default: 1]: ",
        "prompt_weight_lbs": "Enter weight in pounds (lbs): ",
        "prompt_height_ft": "Enter height (feet): ",
        "prompt_height_in": "Enter remaining height (inches): ",
        "prompt_weight_kg": "Enter weight in kilograms (kg): ",
        "prompt_height_metric": "Enter height (in meters e.g. 1.75, or cm e.g. 175): ",
        "invalid_number": "Error: Please enter valid numbers for weight and height.",
        "results_title": "RESULTS",
        "height_label": "Height",
        "weight_label": "Weight",
        "bmi_label": "BMI",
        "category_label": "Category",
        "healthy_range_label": "Healthy weight range for this height",
        "err_height_positive": "Height must be greater than zero.",
        "err_weight_positive": "Weight must be greater than zero.",
        "cat_underweight": "Underweight",
        "cat_normal": "Normal weight",
        "cat_overweight": "Overweight",
        "cat_obese1": "Obesity Class I (Moderate)",
        "cat_obese2": "Obesity Class II (Severe)",
        "cat_obese3": "Obesity Class III (Very severe / Morbidly obese)",
    },
    "id": {
        "title": "KALKULATOR IMT / BMI",
        "select_unit": "Pilih sistem satuan:",
        "metric_option": "1. Metrik (kilogram, meter atau sentimeter)",
        "imperial_option": "2. Imperial (pon, kaki dan inci)",
        "prompt_unit": "Masukkan pilihan (1 atau 2) [standar: 1]: ",
        "prompt_weight_lbs": "Masukkan berat badan dalam pon (lbs): ",
        "prompt_height_ft": "Masukkan tinggi badan (kaki / feet): ",
        "prompt_height_in": "Masukkan sisa tinggi badan (inci / inches): ",
        "prompt_weight_kg": "Masukkan berat badan dalam kilogram (kg): ",
        "prompt_height_metric": "Masukkan tinggi badan (dalam meter contoh: 1.75, atau cm contoh: 175): ",
        "invalid_number": "Kesalahan: Harap masukkan angka yang valid untuk berat dan tinggi badan.",
        "results_title": "HASIL PERHITUNGAN",
        "height_label": "Tinggi Badan",
        "weight_label": "Berat Badan",
        "bmi_label": "Nilai IMT / BMI",
        "category_label": "Kategori",
        "healthy_range_label": "Rentang berat badan sehat untuk tinggi badan ini",
        "err_height_positive": "Tinggi badan harus lebih besar dari nol.",
        "err_weight_positive": "Berat badan harus lebih besar dari nol.",
        "cat_underweight": "Berat Badan Kurang (Kurus)",
        "cat_normal": "Berat Badan Normal (Ideal)",
        "cat_overweight": "Berat Badan Berlebih (Kelebihan berat badan)",
        "cat_obese1": "Obesitas Tingkat I (Sedang)",
        "cat_obese2": "Obesitas Tingkat II (Berat)",
        "cat_obese3": "Obesitas Tingkat III (Sangat Berat / Morbid)",
    },
}


def calculate_bmi(weight_kg: float, height_m: float, lang: str = "en") -> float:
    """Calculate BMI given weight in kilograms and height in meters."""
    t = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    if height_m <= 0:
        raise ValueError(t["err_height_positive"])
    if weight_kg <= 0:
        raise ValueError(t["err_weight_positive"])
    return weight_kg / (height_m ** 2)


def get_bmi_category(bmi: float, lang: str = "en") -> str:
    """Return the WHO / Kemenkes BMI category for a given BMI value in the chosen language."""
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


def get_healthy_weight_range(height_m: float) -> tuple[float, float]:
    """Calculate the healthy weight range (BMI 18.5 to 24.9) in kg for a given height."""
    min_weight = 18.5 * (height_m ** 2)
    max_weight = 24.9 * (height_m ** 2)
    return min_weight, max_weight


def run_interactive(lang: str = None):
    """Run an interactive console session to select language, units, and show results."""
    # If language was not passed via CLI flag, let user pick
    if not lang or lang not in TRANSLATIONS:
        print("=" * 45)
        print("Select Language / Pilih Bahasa:")
        print("  1. English")
        print("  2. Bahasa Indonesia")
        lang_choice = input("\nEnter choice (1 or 2) [default: 1]: ").strip()
        lang = "id" if lang_choice == "2" else "en"

    t = TRANSLATIONS[lang]

    print("\n" + "=" * 45)
    print(f"               {t['title']}")
    print("=" * 45)
    print(t["select_unit"])
    print(f"  {t['metric_option']}")
    print(f"  {t['imperial_option']}")

    choice = input(f"\n{t['prompt_unit']}").strip()

    if choice == "2":
        try:
            weight_lbs = float(input(t["prompt_weight_lbs"]))
            feet = float(input(t["prompt_height_ft"]))
            inches = float(input(t["prompt_height_in"]))

            total_inches = feet * 12 + inches
            weight_kg = weight_lbs * 0.45359237
            height_m = total_inches * 0.0254
        except ValueError:
            print(t["invalid_number"])
            return
    else:
        try:
            weight_kg = float(input(t["prompt_weight_kg"]))
            height_input = float(input(t["prompt_height_metric"]))
            # Automatically detect centimeters if input is greater than 3
            height_m = height_input / 100.0 if height_input > 3 else height_input
        except ValueError:
            print(t["invalid_number"])
            return

    try:
        bmi = calculate_bmi(weight_kg, height_m, lang=lang)
        category = get_bmi_category(bmi, lang=lang)
        min_weight, max_weight = get_healthy_weight_range(height_m)

        print("\n" + "-" * 45)
        print(f"               {t['results_title']}")
        print("-" * 45)
        print(f"{t['height_label']:<15}: {height_m:.2f} m ({height_m * 100:.1f} cm)")
        print(f"{t['weight_label']:<15}: {weight_kg:.1f} kg")
        print(f"{t['bmi_label']:<15}: {bmi:.2f}")
        print(f"{t['category_label']:<15}: {category}")
        print(f"{t['healthy_range_label']}: {min_weight:.1f} kg - {max_weight:.1f} kg")
        print("-" * 45)
    except ValueError as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Bilingual Body Mass Index (BMI / IMT) Calculator (English & Indonesian)."
    )
    parser.add_argument(
        "--lang",
        choices=["en", "id"],
        help="Language preference: 'en' for English, 'id' for Bahasa Indonesia",
    )
    parser.add_argument(
        "--weight",
        type=float,
        help="Weight (in kg by default, or lbs if --imperial is passed)",
    )
    parser.add_argument(
        "--height",
        type=float,
        help="Height (in meters or cm if > 3; in total inches if --imperial is passed)",
    )
    parser.add_argument(
        "--imperial",
        action="store_true",
        help="Treat inputs as imperial units (pounds and inches)",
    )

    args = parser.parse_args()
    lang = args.lang if args.lang else "en"
    t = TRANSLATIONS[lang]

    # If calculation arguments are provided directly via CLI
    if args.weight is not None and args.height is not None:
        try:
            if args.imperial:
                weight_kg = args.weight * 0.45359237
                height_m = args.height * 0.0254
            else:
                weight_kg = args.weight
                height_m = args.height / 100.0 if args.height > 3 else args.height

            bmi = calculate_bmi(weight_kg, height_m, lang=lang)
            category = get_bmi_category(bmi, lang=lang)
            min_weight, max_weight = get_healthy_weight_range(height_m)

            print(f"{t['bmi_label']}: {bmi:.2f}")
            print(f"{t['category_label']}: {category}")
            print(f"{t['healthy_range_label']}: {min_weight:.1f} kg - {max_weight:.1f} kg")
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        run_interactive(lang=args.lang)


if __name__ == "__main__":
    main()
