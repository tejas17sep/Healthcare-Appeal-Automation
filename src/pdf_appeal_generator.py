from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter
from io import BytesIO
import pandas as pd
import os
import sys
import time
from datetime import datetime


# ============================================================
# DOCUMENT RULES
# ============================================================

DOCUMENT_RULES = {
    "Timely Filing": [
        "EOB.pdf",
        "Progress_Note.pdf"
    ],

    "Duplicate": [
        "EOB.pdf",
        "Progress_Note.pdf"
    ],

    "Bundling": [
        "EOB.pdf",
        "Progress_Note.pdf"
    ],

    "Medical Necessity": [
        "EOB.pdf",
        "Discharge_Summary.pdf",
        "History_and_Physical.pdf",
        "Lab_Report.pdf",
        "Progress_Note.pdf"
    ],

    "Missing Info": [
        "EOB.pdf",
        "Discharge_Summary.pdf",
        "History_and_Physical.pdf",
        "Lab_Report.pdf",
        "Progress_Note.pdf"
    ],

    "Authorization": [
        "EOB.pdf",
        "Discharge_Summary.pdf",
        "History_and_Physical.pdf",
        "Lab_Report.pdf",
        "Progress_Note.pdf"
    ]
}


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(PROJECT_ROOT)


# ============================================================
# IMPORT CONFIGURATION
# ============================================================

from config.templates import TEMPLATES

from config.coordinates import (
    AETNA_FIELDS,
    BCBS_FIELDS,
    UHC_FIELDS
)


# ============================================================
# EXCEL FILE
# ============================================================

excel_file = os.path.join(
    PROJECT_ROOT,
    "data",
    "Appeals_Master_100_Sample.xlsx"
)

appeals = pd.read_excel(excel_file)


# ============================================================
# DISPLAY EXCEL COLUMNS
# ============================================================

print("\n========================================")
print("Excel Columns")
print("========================================")

print(appeals.columns.tolist())


# ============================================================
# GET PAYER-SPECIFIC COORDINATES
# ============================================================

def get_fields(insurance):

    if insurance == "Aetna":
        return AETNA_FIELDS

    elif insurance == "BCBS":
        return BCBS_FIELDS

    elif insurance == "UHC":
        return UHC_FIELDS

    else:
        raise ValueError(
            f"Unsupported Insurance: {insurance}"
        )


# ============================================================
# GET REQUIRED DOCUMENTS
# ============================================================

def get_required_documents(row):

    claim_number = str(
        row["Claim_Number"]
    ).strip()

    denial_category = str(
        row["Denial_Category"]
    ).strip()

    folder_value = str(
        row["Medical_Record_Folder"]
    ).strip()


    # --------------------------------------------------------
    # Find Claim Folder
    # --------------------------------------------------------

    if (
        folder_value
        and folder_value.lower() != "nan"
    ):

        if os.path.isabs(folder_value):

            claim_folder = folder_value

        else:

            claim_folder = os.path.join(
                PROJECT_ROOT,
                "documents",
                "MRN",
                f"Claim{folder_value}"
            )

    else:

        claim_folder = os.path.join(
            PROJECT_ROOT,
            "documents",
            "MRN",
            f"Claim{claim_number}"
        )


    print(
        f"\nDocument Folder: {claim_folder}"
    )


    # --------------------------------------------------------
    # Check Folder
    # --------------------------------------------------------

    if not os.path.exists(claim_folder):

        print(
            f"WARNING: Document folder does not exist: "
            f"{claim_folder}"
        )

        return []


    # --------------------------------------------------------
    # Get Documents Based On Denial Category
    # --------------------------------------------------------

    required_files = DOCUMENT_RULES.get(
        denial_category,
        []
    )


    if not required_files:

        print(
            f"WARNING: No document rule found for "
            f"denial category: {denial_category}"
        )

        return []


    document_paths = []


    # --------------------------------------------------------
    # Find Each Required Document
    # --------------------------------------------------------

    for filename in required_files:

        # ----------------------------------------------
        # EOB filename comes from Excel
        # ----------------------------------------------

        if filename == "EOB.pdf":

            eob_filename = str(
                row["EOB_File"]
            ).strip()

            if (
                eob_filename
                and eob_filename.lower() != "nan"
            ):

                filename = eob_filename


        # ----------------------------------------------
        # Complete File Path
        # ----------------------------------------------

        file_path = os.path.join(
            claim_folder,
            filename
        )


        # ----------------------------------------------
        # Check File
        # ----------------------------------------------

        if os.path.exists(file_path):

            document_paths.append(
                file_path
            )

            print(
                f"Found: {filename}"
            )

        else:

            print(
                f"WARNING: {filename} not found "
                f"for Claim {claim_number}"
            )


    return document_paths


# ============================================================
# TODAY'S DATE
# ============================================================

today = datetime.today().strftime(
    "%m/%d/%Y"
)


# ============================================================
# CREATE PDF OVERLAY
# ============================================================

def create_overlay(row, insurance):

    packet = BytesIO()

    fields = get_fields(insurance)


    # --------------------------------------------------------
    # Dates
    # --------------------------------------------------------

    dob = pd.to_datetime(
        row["DOB"]
    ).strftime("%m/%d/%Y")


    dos_from = pd.to_datetime(
        row["DOS_From"]
    ).strftime("%m/%d/%Y")


    dos_to = pd.to_datetime(
        row["DOS_To"]
    ).strftime("%m/%d/%Y")


    # ========================================================
    # FIELD VALUES
    # ========================================================

    field_values = {

        "Generated_Date":
            today,

        "Member_ID":
            str(row["Member_ID"]),

        "Group_Number":
            str(row["Group_Number"]),

        "DOB":
            dob,

        "Provider_Name":
            str(row["Provider_Name"]),

        "Provider_Group":
            str(row["Provider_Group"]),

        "NPI":
            str(row["NPI"]),

        "TIN":
            str(row.get("TIN", "")),

        "Provider_Address":
            str(row["Provider_Address"]),

        "Provider_City":
            str(row["Provider_City"]),

        "Provider_Full_Address":
            f"{row['Provider_Address']}, "
            f"{row['Provider_City']}",

        "Provider_State":
            str(row["Provider_State"]),

        "Provider_Zip_Code":
            str(row["Provider_ZIP"]),

        "Patient_Last_Name":
            str(row["Patient_Last_Name"]),

        "Patient_First_Name":
            str(row["Patient_First_Name"]),

        "Patient_Last_Name1":
            str(row["Patient_Last_Name"]),

        "Patient_First_Name1":
            str(row["Patient_First_Name"]),

        "Patient_Name":
            f"{row['Patient_Last_Name']}, "
            f"{row['Patient_First_Name']}",

        "DOS_From":
            dos_from,

        "DOS_To":
            dos_to,

        "Billed_Amount":
            str(row["Billed_Amount"]),

        "Paid_Amount":
            str(row["Paid_Amount"]),

        "Expected_Outcome":
            str(row["Expected_Outcome"]),

        "Contact_Name":
            str(row["Contact_Name"]),

        "Contact_Phone":
            str(row["Contact_Phone"]),

        "Contact_Fax":
            str(row["Contact_Fax"]),

        "Title":
            str(row.get("Contact_Title", "")),

        "Contact_Email":
            str(row.get("Contact_Email", "")),

        "Claim_Number":
            str(row["Claim_Number"]),

        "Reference_Number":
            str(row["Reference_Number"]),

        "Denial_Code":
            str(row["Denial_Code"]),

        "Appeal_Reason":
            str(row["Appeal_Reason"])
    }


    # ========================================================
    # AETNA
    # ========================================================

    if insurance == "Aetna":

        can = canvas.Canvas(packet)

        page_fields = fields

        for field, (x, y) in page_fields.items():

            can.drawString(
                x,
                y,
                field_values.get(field, "")
            )

        can.save()


    # ========================================================
    # BCBS
    # ========================================================

    elif insurance == "BCBS":

        can = canvas.Canvas(packet)

        page_fields = fields[1]

        for field, (x, y) in page_fields.items():

            can.drawString(
                x,
                y,
                field_values.get(field, "")
            )

        can.save()


    # ========================================================
    # UHC
    # ========================================================

    elif insurance == "UHC":

        can = canvas.Canvas(packet)


        # ----------------------------------------------
        # Page 1
        # ----------------------------------------------

        for field, (x, y) in fields[1].items():

            can.drawString(
                x,
                y,
                field_values.get(field, "")
            )


        can.showPage()


        # ----------------------------------------------
        # Page 2
        # ----------------------------------------------

        for field, (x, y) in fields[2].items():

            can.drawString(
                x,
                y,
                field_values.get(field, "")
            )


        can.save()


    packet.seek(0)

    return packet


# ============================================================
# TIME FORMAT FUNCTION
# ============================================================

def format_time(seconds):

    seconds = int(seconds)

    hours, remainder = divmod(
        seconds,
        3600
    )

    minutes, seconds = divmod(
        remainder,
        60
    )


    if hours > 0:

        return (
            f"{hours} hr "
            f"{minutes} min "
            f"{seconds} sec"
        )

    elif minutes > 0:

        return (
            f"{minutes} min "
            f"{seconds} sec"
        )

    else:

        return f"{seconds} sec"


# ============================================================
# START OVERALL TIMER
# ============================================================

process_start_time = time.time()

total_claims = len(appeals)

completed_claims = 0


print("\n========================================")
print(
    f"Total appeals to process: "
    f"{total_claims}"
)
print("Processing started...")
print("========================================")


# ============================================================
# MAIN PROCESSING LOOP
# ============================================================

for index, row in appeals.iterrows():


    # --------------------------------------------------------
    # Start Timer For Current Claim
    # --------------------------------------------------------

    claim_start_time = time.time()


    # --------------------------------------------------------
    # Basic Claim Information
    # --------------------------------------------------------

    insurance = str(
        row["Insurance"]
    ).strip()

    claim_number = str(
        row["Claim_Number"]
    ).strip()

    denial_category = str(
        row["Denial_Category"]
    ).strip()


    # --------------------------------------------------------
    # Display Current Claim
    # --------------------------------------------------------

    print("\n")
    print("========================================")

    print(
        f"Generating {insurance} PDF "
        f"{index + 1}/{total_claims}"
    )

    print(
        f"Claim Number: {claim_number}"
    )

    print(
        f"Denial Category: "
        f"{denial_category}"
    )

    print("========================================")


    # ========================================================
    # GET APPEAL TEMPLATE
    # ========================================================

    template = TEMPLATES[
        insurance
    ]["file"]


    # ========================================================
    # CREATE OUTPUT FOLDER
    # ========================================================

    output_folder = os.path.join(
        PROJECT_ROOT,
        "output",
        "Appeals",
        insurance
    )


    os.makedirs(
        output_folder,
        exist_ok=True
    )


    # ========================================================
    # CREATE OVERLAY
    # ========================================================

    overlay = create_overlay(
        row,
        insurance
    )


    # ========================================================
    # READ TEMPLATE PDF
    # ========================================================

    template_pdf = PdfReader(
        template
    )


    overlay_pdf = PdfReader(
        overlay
    )


    writer = PdfWriter()


    # ========================================================
    # MERGE OVERLAY WITH TEMPLATE
    # ========================================================

    for page_number, page in enumerate(
        template_pdf.pages
    ):

        if page_number < len(
            overlay_pdf.pages
        ):

            page.merge_page(
                overlay_pdf.pages[page_number]
            )

        writer.add_page(page)


    # ========================================================
    # GET REQUIRED DOCUMENTS
    # ========================================================

    required_documents = (
        get_required_documents(row)
    )


    print(
        f"\nAttaching "
        f"{len(required_documents)} "
        f"documents "
        f"for Claim {claim_number}"
    )


    # ========================================================
    # APPEND MEDICAL RECORDS + EOB
    # ========================================================

    for document_path in required_documents:

        print(
            f"Appending: "
            f"{os.path.basename(document_path)}"
        )


        document_pdf = PdfReader(
            document_path
        )


        for document_page in (
            document_pdf.pages
        ):

            writer.add_page(
                document_page
            )


    # ========================================================
    # OUTPUT FILE
    # ========================================================

    output_file = os.path.join(
        output_folder,
        f"{claim_number}.pdf"
    )


    # ========================================================
    # WRITE FINAL PDF
    # ========================================================

    with open(
        output_file,
        "wb"
    ) as f:

        writer.write(f)


    print(
        f"\nCreated: {output_file}"
    )


    # ========================================================
    # CALCULATE TIMING
    # ========================================================

    claim_end_time = time.time()


    # Current claim processing time

    claim_time = (
        claim_end_time
        - claim_start_time
    )


    # Increase completed count

    completed_claims += 1


    # Total elapsed time

    elapsed_time = (
        claim_end_time
        - process_start_time
    )


    # Average processing time

    average_time = (
        elapsed_time
        / completed_claims
    )


    # Remaining claims

    remaining_claims = (
        total_claims
        - completed_claims
    )


    # Estimated remaining time

    estimated_remaining_time = (
        remaining_claims
        * average_time
    )


    # ========================================================
    # DISPLAY PROGRESS
    # ========================================================

    print("\n----------------------------------------")

    print(
        f"Progress: "
        f"{completed_claims}/"
        f"{total_claims}"
    )

    print(
        f"Current claim time: "
        f"{format_time(claim_time)}"
    )

    print(
        f"Total elapsed time: "
        f"{format_time(elapsed_time)}"
    )

    print(
        f"Average time per claim: "
        f"{format_time(average_time)}"
    )

    print(
        f"Estimated remaining time: "
        f"{format_time(estimated_remaining_time)}"
    )

    print("----------------------------------------")


# ============================================================
# FINAL PROCESSING TIME
# ============================================================

total_end_time = time.time()


total_processing_time = (
    total_end_time
    - process_start_time
)


# ============================================================
# FINAL RESULT
# ============================================================

print("\n")

print("========================================")
print("ALL APPEAL PDFs CREATED SUCCESSFULLY")
print("========================================")

print(
    f"Completed appeals: "
    f"{completed_claims}/"
    f"{total_claims}"
)

print(
    f"Total processing time: "
    f"{format_time(total_processing_time)}"
)


if completed_claims > 0:

    print(
        f"Average time per appeal: "
        f"{format_time(total_processing_time / completed_claims)}"
    )


print("========================================")