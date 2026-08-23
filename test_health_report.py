from health_report import generate_health_report


fitness_data = [
    (1, 8000, 400, 2.5),
    (2, 9000, 450, 2.8),
    (3, 10000, 500, 3.0)
]

medicines = [
    (1, "Paracetamol", "500mg", "9:00 AM"),
    (2, "Vitamin C", "500mg", "6:00 PM")
]

report = generate_health_report(
    fitness_data,
    medicines,
    adherence=85,
    steps_goal=10000,
    water_goal=3.0,
    calories_goal=500
)

print(report)