import json
import csv
import io
import xml.etree.ElementTree as ET


# ============================================================
# EXPORT HEALTH DATA TO JSON
# ============================================================

def export_json(fitness_data):

    data = []

    for record in fitness_data:

        data.append({
            "id": record[0],
            "steps": record[1],
            "calories": record[2],
            "water": record[3]
        })

    return json.dumps(
        data,
        indent=4
    )


# ============================================================
# EXPORT HEALTH DATA TO CSV
# ============================================================

def export_csv(fitness_data):

    output = io.StringIO()

    writer = csv.writer(output)

    # CSV Header
    writer.writerow([
        "id",
        "steps",
        "calories",
        "water"
    ])

    # Add fitness records
    for record in fitness_data:

        writer.writerow([
            record[0],
            record[1],
            record[2],
            record[3]
        ])

    return output.getvalue()


# ============================================================
# EXPORT HEALTH DATA TO XML
# ============================================================

def export_xml(fitness_data):

    root = ET.Element(
        "health_data"
    )

    # Add each fitness record
    for record in fitness_data:

        fitness = ET.SubElement(
            root,
            "fitness"
        )

        ET.SubElement(
            fitness,
            "id"
        ).text = str(record[0])

        ET.SubElement(
            fitness,
            "steps"
        ).text = str(record[1])

        ET.SubElement(
            fitness,
            "calories"
        ).text = str(record[2])

        ET.SubElement(
            fitness,
            "water"
        ).text = str(record[3])

    return ET.tostring(
        root,
        encoding="unicode"
    )


# ============================================================
# IMPORT HEALTH DATA FROM JSON
# ============================================================

def import_json(uploaded_file):

    content = uploaded_file.read()

    # Convert bytes to string
    if isinstance(
        content,
        bytes
    ):

        content = content.decode(
            "utf-8"
        )

    # Convert JSON string to Python data
    return json.loads(
        content
    )


# ============================================================
# IMPORT HEALTH DATA FROM CSV
# ============================================================

def import_csv(uploaded_file):

    content = uploaded_file.read()

    # Convert bytes to string
    if isinstance(
        content,
        bytes
    ):

        content = content.decode(
            "utf-8"
        )

    # Read CSV data
    reader = csv.DictReader(
        io.StringIO(content)
    )

    return list(
        reader
    )


# ============================================================
# IMPORT HEALTH DATA FROM XML
# ============================================================

def import_xml(uploaded_file):

    content = uploaded_file.read()

    # Convert bytes to string
    if isinstance(
        content,
        bytes
    ):

        content = content.decode(
            "utf-8"
        )

    # Convert XML string to XML tree
    root = ET.fromstring(
        content
    )

    data = []

    # Read each fitness record
    for fitness in root.findall(
        "fitness"
    ):

        record = {

            "id": fitness.findtext(
                "id"
            ),

            "steps": fitness.findtext(
                "steps"
            ),

            "calories": fitness.findtext(
                "calories"
            ),

            "water": fitness.findtext(
                "water"
            )
        }

        data.append(
            record
        )

    return data