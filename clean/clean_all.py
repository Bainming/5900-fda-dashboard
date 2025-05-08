from . import clean_483s
from . import clean_inspections
from . import clean_recalls
from . import clean_comliances
from . import compute_firms

def clean_all():
    clean_483s.monitor_and_clean_folder()
    print("Cleaned 483 forms")

    clean_inspections.merge_classification_and_citation()
    print("Cleaned Inspections")

    clean_recalls.clean_recalls()
    print("Cleaned Recalls")

    clean_comliances.preprocess_compliance_data()
    print("Cleaned Compliances")

    compute_firms.merge_firms()
    print("Created company list")

