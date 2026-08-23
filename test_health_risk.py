from health_risk import calculate_health_risk


test_cases = [
    {
        "steps": 2000,
        "water": 1.0,
        "calories": 200,
        "adherence": 50
    },
    {
        "steps": 4500,
        "water": 1.8,
        "calories": 400,
        "adherence": 75
    },
    {
        "steps": 9000,
        "water": 2.8,
        "calories": 500,
        "adherence": 95
    }
]


for i, test in enumerate(test_cases, 1):

    risk, score, warnings = calculate_health_risk(
        test["steps"],
        test["water"],
        test["calories"],
        test["adherence"]
    )

    print("=" * 60)
    print(f"TEST {i}")
    print(f"Steps: {test['steps']}")
    print(f"Water: {test['water']} L")
    print(f"Calories: {test['calories']}")
    print(f"Medication Adherence: {test['adherence']}%")
    print()
    print(f"Risk Level: {risk}")
    print(f"Risk Score: {score}")

    print("\nWarnings:")

    if warnings:
        for warning in warnings:
            print("-", warning)
    else:
        print("No major warnings.")

print("=" * 60)