"""Unit tests for english_bmi_calculator.py."""

import unittest
from english_bmi_calculator import (
    calculate_bmi_english,
    get_bmi_category,
    get_healthy_weight_range_english,
)


class TestEnglishBMICalculator(unittest.TestCase):
    def test_calculate_bmi_normal(self):
        # 160 lbs, 5'10" (70 inches) -> (160 * 703) / (70^2) = 112480 / 4900 = 22.955...
        bmi = calculate_bmi_english(160, 70)
        self.assertAlmostEqual(bmi, 22.955, places=2)
        self.assertEqual(get_bmi_category(bmi), "Normal weight")

    def test_calculate_bmi_underweight(self):
        # 100 lbs, 68 inches -> (100 * 703) / (68^2) = 70300 / 4624 = 15.20...
        bmi = calculate_bmi_english(100, 68)
        self.assertAlmostEqual(bmi, 15.20, places=1)
        self.assertEqual(get_bmi_category(bmi), "Underweight")

    def test_calculate_bmi_overweight(self):
        # 190 lbs, 70 inches -> (190 * 703) / 4900 = 133570 / 4900 = 27.26...
        bmi = calculate_bmi_english(190, 70)
        self.assertAlmostEqual(bmi, 27.26, places=2)
        self.assertEqual(get_bmi_category(bmi), "Overweight")

    def test_calculate_bmi_obesity_classes(self):
        # Class 1: 30 <= BMI < 35
        bmi_obese1 = 32.0
        self.assertEqual(get_bmi_category(bmi_obese1), "Obesity (Class 1 - Moderate)")

        # Class 2: 35 <= BMI < 40
        bmi_obese2 = 37.5
        self.assertEqual(get_bmi_category(bmi_obese2), "Obesity (Class 2 - Severe)")

        # Class 3: >= 40
        bmi_obese3 = 42.0
        self.assertEqual(get_bmi_category(bmi_obese3), "Obesity (Class 3 - Very severe / Morbid)")

    def test_healthy_weight_range(self):
        # Height: 70 inches
        min_w, max_w = get_healthy_weight_range_english(70)
        # min = (18.5 * 4900) / 703 = 128.95
        # max = (24.9 * 4900) / 703 = 173.56
        self.assertAlmostEqual(min_w, 128.95, places=1)
        self.assertAlmostEqual(max_w, 173.56, places=1)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            calculate_bmi_english(-150, 70)
        with self.assertRaises(ValueError):
            calculate_bmi_english(150, 0)
        with self.assertRaises(ValueError):
            calculate_bmi_english(150, -60)


if __name__ == "__main__":
    unittest.main()
