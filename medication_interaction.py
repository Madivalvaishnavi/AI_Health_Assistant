def check_medication_interaction(medicine1, medicine2):
    """
    Checks for a few basic known medication interactions.
    This feature is for educational purposes only.
    """

    medicine1 = medicine1.lower().strip()
    medicine2 = medicine2.lower().strip()

    if not medicine1 or not medicine2:
        return "Please enter both medicine names."

    if medicine1 == medicine2:
        return "You entered the same medicine twice."

    interactions = {
        ("warfarin", "aspirin"):
            "Warfarin and aspirin may increase the risk of bleeding.",

        ("ibuprofen", "aspirin"):
            "Ibuprofen and aspirin may increase the risk of stomach irritation and bleeding.",

        ("warfarin", "ibuprofen"):
            "Warfarin and ibuprofen may increase the risk of bleeding.",

        ("paracetamol", "alcohol"):
            "Combining paracetamol and alcohol may increase the risk of liver damage."
    }

    combination1 = (medicine1, medicine2)
    combination2 = (medicine2, medicine1)

    if combination1 in interactions:
        return (
            "⚠️ Interaction Warning: "
            + interactions[combination1]
            + " Please consult a doctor or pharmacist."
        )

    elif combination2 in interactions:
        return (
            "⚠️ Interaction Warning: "
            + interactions[combination2]
            + " Please consult a doctor or pharmacist."
        )

    else:
        return (
            "✅ No interaction found in our basic interaction database. "
            "This does not guarantee that the medicines are safe to combine. "
            "Please consult a doctor or pharmacist before taking medicines together."
        )