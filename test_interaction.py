from medication_interaction import check_medication_interaction


tests = [
    ("warfarin", "aspirin"),
    ("ASPIRIN", "ibuprofen"),
    ("Paracetamol", "Alcohol"),
    ("Paracetamol", "Vitamin C"),
    ("Paracetamol", "paracetamol")
]


for medicine1, medicine2 in tests:

    print("=" * 60)

    print(
        f"Medicine 1: {medicine1}"
    )

    print(
        f"Medicine 2: {medicine2}"
    )

    result = check_medication_interaction(
        medicine1,
        medicine2
    )

    print("\nResult:")
    print(result)

    print()