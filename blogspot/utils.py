import re


def cleanuplabel(label):
    label = label.lower()
    categories = {
        "sales|sale|marketing": "sales&marketing",
        "management": "manegarial",
        "engineering": "engineering",
        "ict|information|technology": "ict",
        "human resources|human|resources": "human resources",
        "purchasing and supply chain|purchasing|supply": "purchasing & supply chain",
        "finance|banking|account": "finance&accounting",
        "administrative|admin|administrator": "administrative",
        "consult": "consulting",
        "research": "research",
        "analyst": "analyst",
        "business|development": "business development",
        "data": "datascience",
        "education|training": "education",
        "design|creative": "graphicdesign",
        "health|care|provider|doctor|hospital": "medical&healthcare",
        "building|appliances|electrical|electronics|manufacturing": "building&construction",
    }
    for pattern, category in categories.items():
        if re.search(pattern, label):
            return category
    return "Other"

def cleanupindustry(label):
    if re.search("hospitals|health|Care", label.lower()):
        label = "Hospitalsandhealthcare"
    elif re.search("government ", label.lower()):
        label = "government"
    elif re.search("business|finance|banking ", label.lower()):
        label = "business"
    elif re.search("non-profit|non-government|ngo|private", label.lower()):
        label = "ngo"
    elif re.search("computer|technology|software", label.lower()):
        label = "ict"
    else:
        label = "Other"
    
    return label

def createjoblevels(label, seniority, employment_type, industry):
    # Map seniority to seniority level
    seniority_map = {
        "Not Applicable": "entrylevel",
        "Executive": "seniorlevel",
        "High Level": "seniorlevel",
        "Mid-Senior level": "midlevel",
        "Mid Level": "midlevel",
    }
    seniority = seniority_map.get(seniority, seniority)

    label_combi = label + [seniority] + [employment_type] + industry

    return label_combi
