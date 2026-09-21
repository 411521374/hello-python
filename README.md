# BMI Calculator Project (0921_AIAA)

A Python-based Body Mass Index (BMI) calculator supporting English / Imperial units and standard WHO / CDC weight status classifications.

## Formula (English / Imperial Units)

$$\text{BMI} = \frac{\text{weight (lbs)} \times 703}{\left(\text{height in inches}\right)^2}$$

The healthy weight range ($\text{BMI } 18.5 - 24.9$) for a given height in inches is calculated as:
$$\text{Weight Range (lbs)} = \left[\frac{18.5 \times \text{height}^2}{703},\; \frac{24.9 \times \text{height}^2}{703}\right]$$

## Features

- **Interactive Prompts**: Prompts step-by-step for height (feet & inches or total inches) and weight in pounds (lbs).
- **Command-Line Interface**: Run directly with arguments (e.g. `--weight`, `--feet`, `--inches`, `--total-inches`).
- **Standard Classifications**: Classifies into Underweight, Normal weight, Overweight, and Obesity Classes 1, 2, and 3.
- **Unit Testing**: Complete `unittest` test suite included.

## Usage

### 1. Interactive Mode
```bash
python english_bmi_calculator.py
```

### 2. Command-Line Arguments Mode
```bash
python english_bmi_calculator.py --weight 160 --feet 5 --inches 10
```
Or with total inches:
```bash
python english_bmi_calculator.py --weight 200 --total-inches 72
```

### 3. Run Unit Tests
```bash
python -m unittest test_english_bmi_calculator.py
```
