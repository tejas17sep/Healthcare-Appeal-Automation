AETNA_FIELDS = {

    "Generated_Date": (55, 595),
    "Member_ID": (220, 595),
    "Group_Number": (480, 595),

    "Patient_First_Name": (80, 550),
    "Patient_Last_Name": (240, 550),
    "DOB": (470, 550),

    "Provider_Name": (90, 505),
    "NPI": (360, 505),
    "Provider_Group": (500, 505),

    "Contact_Name": (100, 480),
    "Provider_Address": (120, 450),

    "Contact_Phone": (80, 420),
    "Contact_Fax": (230, 420),
    "Contact_Email": (430, 420),

    "Claim_Number": (90, 345),
    "Reference_Number": (260, 345),
    "DOS_From": (480, 345),

    "Denial_Code": (90, 285),
    "Appeal_Reason": (80, 190),

}

BCBS_FIELDS = {

    1: {
        # Provider Information
        # "Provider_Name": (319, 785),
        # "NPI": (594, 826),
        # "TPI": (1241, 826),
        # "TIN": (310, 874),
        # "Street_Address": (316, 924),
        # "City": (194,963),
        # "State": (880, 963),
        # "Zip_Code": (1128, 963),

        
         "Provider_Name": (120, 532),
         "NPI": (200, 515),
        #  "TPI": (300, 520),
        #  "TIN": (220, 520),
         "Provider_Address": (120, 485),
         "Provider_City": (120, 470),
         "Provider_State": (300, 470),
         "Provider_Zip_Code": (420, 470),

        # Claim Information
            "Patient_Name": (120, 375),
            "DOB": (320, 375),
            "Member_ID": (185, 358),
            "Claim_Number": (270, 341),
            "DOS_From": (208, 327),
            "DOS_To": (275, 327),

            "Billed_Amount": (160, 305),
            "Paid_Amount": (400, 305),
            "Appeal_Reason": (80, 253),
            "Expected_Outcome": (120, 191),

                "Contact_Name": (152, 176),
                "Title": (350, 176),
                "Contact_Phone": (105, 161),
                "Contact_Fax": (380, 161),
                "Generated_Date": (360, 145)
    }
}



UHC_FIELDS = {

    1: {

         "Generated_Date": (155, 338),
         "Member_ID": (340, 338),
         "Claim_Number": (50, 305),
         "DOS_From": (330, 305),
         "Billed_Amount": (470, 305),

         "Patient_Last_Name": (50, 275),
         "Patient_First_Name": (250, 275),

         "Provider_Full_Address": (50, 240),
         "Provider_State": (370, 240),
         "Provider_Zip_Code": (490, 240),

         "Patient_Last_Name1": (50, 210),
         "Patient_First_Name1": (250, 210),

         "TIN": (50, 155),
         "Contact_Phone": (390, 155),
         "Contact_Email": (80, 133)
        

        # "Provider_Name": (150, 380),
        # "TIN": (150, 350),
        # "Contact_Phone": (450, 350),
        # "Contact_Email": (150, 320)

    },


    2: {

        "Provider_Name": (100, 655),

        "Provider_Address": (120, 630),

        "Provider_City": (90, 608),

        "Provider_State": (310, 608), 

        "Provider_Zip_Code": (460, 608),

        "Group_Number": (80, 573),

        "Contact_Name": (300, 573),

        "Expected_Outcome": (80, 545),

        "Contact_Fax": (300, 545),

    }

}