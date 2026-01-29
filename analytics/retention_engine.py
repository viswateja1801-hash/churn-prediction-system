def retention_strategy(risk):
    if risk == "HIGH":
        return [
            "Offer 20% discount",
            "Assign retention specialist",
            "Priority customer support"
        ]
    elif risk == "MEDIUM":
        return [
            "Send loyalty offer",
            "Engagement email campaign"
        ]
    else:
        return [
            "Regular engagement",
            "Upsell premium features"
        ]
