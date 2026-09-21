"""English / Imperial Body Mass Index (BMI) Calculator.

Calculates BMI using the English / Imperial measurement system:
    BMI = (weight_in_lbs * 703) / (height_in_inches ** 2)

Supports both interactive command-line prompts and direct CLI arguments.
"""

from __future__ import annotations

import argparse
import sys
from typing import Tuple


def calculate_bmi_english(weight_lbs: float, height_inches: float) -> float:
    """Calculate BMI using English / Imperial units (weight in lbs, height in inches).

    Formula:
        BMI = (weight_lbs * 703) / (height_inches ** 2)

    Args:
        weight_lbs: Body weight in pounds (lbs).
        height_inches: Total height in inches.

    Returns:
        The calculated BMI as a float.

    Raises:
        ValueError: If weight_lbs or height_inches is not strictly positive.
    """
    if height_inches <= 0:
        raise ValueError("Height must be greater than zero.")
    if weight_lbs <= 0:
        raise ValueError("Weight must be greater than zero.")

    return (weight_lbs * 703.0) / (height_inches ** 2)


def get_bmi_category(bmi: float) -> str:
    """Return the standard CDC / WHO BMI weight status category.

    Categories:
        - Below 18.5: Underweight
        - 18.5 - 24.9: Normal weight
        - 25.0 - 29.9: Overweight
        - 30.0 - 34.9: Obesity (Class 1 - Moderate)
        - 35.0 - 39.9: Obesity (Class 2 - Severe)
        - 40.0 and above: Obesity (Class 3 - Very severe / Morbid)

    Args:
        bmi: The Body Mass Index value.

    Returns:
        The category name as a string.
    """
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25.0:
        return "Normal weight"
    elif bmi < 30.0:
        return "Overweight"
    elif bmi < 35.0:
        return "Obesity (Class 1 - Moderate)"
    elif bmi < 40.0:
        return "Obesity (Class 2 - Severe)"
    else:
        return "Obesity (Class 3 - Very severe / Morbid)"


def get_healthy_weight_range_english(height_inches: float) -> Tuple[float, float]:
    """Calculate the healthy weight range (BMI 18.5 to 24.9) in pounds for a given height in inches.

    Args:
        height_inches: Total height in inches.

    Returns:
        A tuple of (min_weight_lbs, max_weight_lbs).
    """
    if height_inches <= 0:
        raise ValueError("Height must be greater than zero.")

    min_weight = (18.5 * (height_inches ** 2)) / 703.0
    max_weight = (24.9 * (height_inches ** 2)) / 703.0
    return min_weight, max_weight


def display_results(weight_lbs: float, height_inches: float, bmi: float) -> None:
    """Print formatted summary of the BMI calculation and health category."""
    feet = int(height_inches // 12)
    inches = height_inches % 12
    category = get_bmi_category(bmi)
    min_weight, max_weight = get_healthy_weight_range_english(height_inches)

    print("\n" + "=" * 50)
    print("           ENGLISH BMI CALCULATION REPORT")
    print("=" * 50)
    if feet > 0:
        print(f"  Height       : {feet} ft {inches:.1f} in ({height_inches:.1f} inches)")
    else:
        print(f"  Height       : {height_inches:.1f} inches")
    print(f"  Weight       : {weight_lbs:.1f} lbs")
    print(f"  BMI Value    : {bmi:.2f}")
    print(f"  Category     : {category}")
    print(f"  Healthy Range: {min_weight:.1f} lbs - {max_weight:.1f} lbs")
    print("=" * 50)


def prompt_positive_float(prompt_text: str) -> float:
    """Prompt the user for a numeric float value greater than zero."""
    while True:
        raw_val = input(prompt_text).strip()
        try:
            val = float(raw_val)
            if val <= 0:
                print("  [!] Please enter a positive number greater than 0.")
                continue
            return val
        except ValueError:
            print("  [!] Invalid input. Please enter a valid number.")


def run_interactive() -> None:
    """Run an interactive console prompt for English BMI calculation."""
    print("=" * 50)
    print("        ENGLISH / IMPERIAL BMI CALCULATOR")
    print("=" * 50)
    print("How would you like to enter your height?")
    print("  1. Feet and inches (e.g., 5 ft 10 in)")
    print("  2. Total inches (e.g., 70 in)")
    
    height_choice = input("\nEnter choice (1 or 2) [default: 1]: ").strip()
    if height_choice == "2":
        height_inches = prompt_positive_float("Enter height in inches: ")
    else:
        while True:
            try:
                raw_feet = input("Enter height (feet): ").strip()
                feet = float(raw_feet)
                if feet < 0:
                    print("  [!] Feet cannot be negative.")
                    continue

                raw_inches = input("Enter remaining height (inches): ").strip()
                inches = float(raw_inches)
                if inches < 0:
                    print("  [!] Inches cannot be negative.")
                    continue

                total_inches = feet * 12.0 + inches
                if total_inches <= 0:
                    print("  [!] Total height must be greater than zero.")
                    continue
                height_inches = total_inches
                break
            except ValueError:
                print("  [!] Please enter valid numerical values.")

    weight_lbs = prompt_positive_float("Enter weight in pounds (lbs): ")

    bmi = calculate_bmi_english(weight_lbs=weight_lbs, height_inches=height_inches)
    display_results(weight_lbs=weight_lbs, height_inches=height_inches, bmi=bmi)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="English / Imperial Body Mass Index (BMI) Calculator.",
        epilog="Example: python english_bmi_calculator.py --weight 160 --feet 5 --inches 10",
    )
    parser.add_argument(
        "-w", "--weight",
        type=float,
        help="Weight in pounds (lbs).",
    )
    parser.add_argument(
        "--feet",
        type=float,
        default=0.0,
        help="Height component in feet.",
    )
    parser.add_argument(
        "--inches",
        type=float,
        default=0.0,
        help="Height component in inches (added to --feet).",
    )
    parser.add_argument(
        "-i", "--total-inches",
        type=float,
        help="Total height in inches (alternative to specifying feet and inches).",
    )

    args = parser.parse_args()

    # If weight is provided via CLI arguments
    if args.weight is not None:
        if args.total_inches is not None:
            height_inches = args.total_inches
        else:
            height_inches = (args.feet * 12.0) + args.inches

        if height_inches <= 0:
            print("Error: Height must be greater than zero (use --total-inches or --feet/--inches).", file=sys.stderr)
            sys.exit(1)

        try:
            bmi = calculate_bmi_english(args.weight, height_inches)
            display_results(args.weight, height_inches, bmi)
        except ValueError as err:
            print(f"Error: {err}", file=sys.stderr)
            sys.exit(1)
    else:
        run_interactive()


if __name__ == "__main__":
    main()
