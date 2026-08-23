
# ============================================================
# MEDICATION INTERACTION CHECKER
# ============================================================

def normalize_medicine_name(medicine):
    """
    Cleans and normalizes a medicine name.
    """

    if not medicine:
        return ""

    return medicine.strip().lower()


def check_medication_interaction(medicine1, medicine2):
    """
    Checks a limited educational database for known
    medication interactions.

    This feature is for educational purposes only and
    does not replace advice from a doctor or pharmacist.
    """

    # --------------------------------------------------------
    # NORMALIZE INPUT
    # --------------------------------------------------------

    medicine1 = normalize_medicine_name(
        medicine1
    )

    medicine2 = normalize_medicine_name(
        medicine2
    )

    # --------------------------------------------------------
    # VALIDATE INPUT
    # --------------------------------------------------------

    if not medicine1 or not medicine2:

        return (
            "⚠️ Please enter both medicine names."
        )

    # --------------------------------------------------------
    # SAME MEDICINE CHECK
    # --------------------------------------------------------

    if medicine1 == medicine2:

        return (
            "⚠️ You entered the same medicine twice.\n\n"
            "Please enter two different medicines to "
            "check for a possible interaction."
        )

    # --------------------------------------------------------
    # BASIC INTERACTION DATABASE
    # --------------------------------------------------------

    interactions = {

        ("warfarin", "aspirin"):
            (
                "Warfarin and aspirin may increase the "
                "risk of bleeding."
            ),

        ("aspirin", "ibuprofen"):
            (
                "Aspirin and ibuprofen may increase the "
                "risk of stomach irritation and bleeding."
            ),

        ("ibuprofen", "warfarin"):
            (
                "Ibuprofen and warfarin may increase the "
                "risk of bleeding."
            ),

        ("paracetamol", "alcohol"):
            (
                "Combining paracetamol and alcohol may "
                "increase the risk of liver damage."
            ),

        ("warfarin", "acetaminophen"):
            (
                "Acetaminophen may interact with warfarin "
                "and may affect bleeding risk depending "
                "on use and dose."
            )
    }

    # --------------------------------------------------------
    # CREATE BOTH COMBINATIONS
    # --------------------------------------------------------

    combination1 = (
        medicine1,
        medicine2
    )

    combination2 = (
        medicine2,
        medicine1
    )

    # --------------------------------------------------------
    # CHECK INTERACTION
    # --------------------------------------------------------

    if combination1 in interactions:

        interaction_message = interactions[
            combination1
        ]

        return (
            "⚠️ **Potential Medication Interaction**\n\n"
            f"{interaction_message}\n\n"
            "🩺 **Recommendation:**\n"
            "Please consult a doctor or pharmacist before "
            "combining these substances."
        )

    elif combination2 in interactions:

        interaction_message = interactions[
            combination2
        ]

        return (
            "⚠️ **Potential Medication Interaction**\n\n"
            f"{interaction_message}\n\n"
            "🩺 **Recommendation:**\n"
            "Please consult a doctor or pharmacist before "
            "combining these substances."
        )

    # --------------------------------------------------------
    # UNKNOWN COMBINATION
    # --------------------------------------------------------

    else:

        return (
            "ℹ️ **Interaction Information Not Available**\n\n"
            "No interaction information was found for "
            "this combination in our limited educational "
            "database.\n\n"
            "⚠️ This does NOT mean the medicines are safe "
            "to combine.\n\n"
            "🩺 Please consult a doctor or pharmacist "
            "before taking medicines together."
        )
