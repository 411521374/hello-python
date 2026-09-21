"""Unit tests for bilingual BMI calculator functions."""

import unittest
from english_bmi_calculator import (
    calculate_bmi_english,
    calculate_bmi_metric,
    get_bmi_category,
    get_healthy_weight_range_english,
    get_healthy_weight_range_metric,
)


class TestBilingualBMICalculator(unittest.TestCase):
    def test_calculate_bmi_english(self):
        # 160 lbs, 70 inches -> (160 * 703) / 4900 = 22.955...
        bmi = calculate_bmi_english(160, 70)
        self.assertAlmostEqual(bmi, 22.955, places=2)
        self.assertIn("Normal", get_bmi_category(bmi, lang="en"))

    def test_calculate_bmi_metric(self):
        # 70 kg, 1.75 m -> 70 / (1.75^2) = 22.857...
        bmi = calculate_bmi_metric(70, 1.75)
        self.assertAlmostEqual(bmi, 22.86, places=2)
        self.assertIn("Normal", get_bmi_category(bmi, lang="en"))
        self.assertIn("Normal", get_bmi_category(bmi, lang="id"))

    def test_categories_english(self):
        self.assertIn("Underweight", get_bmi_category(16.0, lang="en"))
        self.assertIn("Normal", get_bmi_category(22.0, lang="en"))
        self.assertIn("Overweight", get_bmi_category(27.5, lang="en"))
        self.assertIn("Obesity Class 1", get_bmi_category(32.0, lang="en"))
        self.assertIn("Obesity Class 2", get_bmi_category(36.0, lang="en"))
        self.assertIn("Obesity Class 3", get_bmi_category(42.0, lang="en"))

    def test_categories_indonesian(self):
        self.assertIn("Kurang", get_bmi_category(16.0, lang="id"))
        self.assertIn("Normal", get_bmi_category(22.0, lang="id"))
        self.assertIn("Berlebih", get_bmi_category(27.5, lang="id"))
        self.assertIn("Tingkat 1", get_bmi_category(32.0, lang="id"))
        self.assertIn("Tingkat 2", get_bmi_category(36.0, lang="id"))
        self.assertIn("Tingkat 3", get_bmi_category(42.0, lang="id"))

    def test_healthy_weight_ranges(self):
        # Metric: 1.75 m
        min_kg, max_kg = get_healthy_weight_range_metric(1.75)
        self.assertAlmostEqual(min_kg, 56.66, places=1)
        self.assertAlmostEqual(max_kg, 76.26, places=1)

        # English: 70 inches
        min_lbs, max_lbs = get_healthy_weight_range_english(70)
        self.assertAlmostEqual(min_lbs, 128.95, places=1)
        self.assertAlmostEqual(max_lbs, 173.56, places=1)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            calculate_bmi_english(-150, 70)
        with self.assertRaises(ValueError):
            calculate_bmi_english(150, 0)
        with self.assertRaises(ValueError):
            calculate_bmi_metric(-70, 1.75)
        with self.assertRaises(ValueError):
            calculate_bmi_metric(70, 0)


if __name__ == "__main__":
    unittest.main()
