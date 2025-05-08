import pandas as pd

def clean_recalls():
    dataset = pd.read_csv("./data/raw_csv/recall_data.csv", low_memory = False)

    dataset.columns = dataset.columns.str.upper()

    dataset["LINK"] = dataset["PRODUCTID"].apply(lambda x: f"https://www.accessdata.fda.gov/scripts/ires/?Product={x}")

    with_recall_link = dataset[
        ["FIRMFEINUM", "FIRMLEGALNAM", "FIRMSURVIVINGFEI", "FIRMSURVIVINGNAM", "LINK",
        "CENTERCLASSIFICATIONTYPETXT", "PHASETXT", "DISTRIBUTIONAREASUMMARYTXT", 
        "FIRMCITYNAM", "FIRMSTATEPRVNCNAM", "FIRMCOUNTRYNAM", "CENTERCLASSIFICATIONDT", 
        "PRODUCTSHORTREASONTXT", "PRODUCTDESCRIPTIONTXT", "RECALLEVENTID", "PRODUCTID"]
    ]

    with_recall_link.to_csv("./data/cleaned/recall_data.csv", index = False, encoding = "utf-8-sig")

    return

if __name__ == "__main__":
    clean_recalls()