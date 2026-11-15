
def validate_opportunities(opportunities):
    if not isinstance(opportunities, list):
        raise ValueError("Opportunities must be a list")

    for index, opportunity in enumerate(opportunities):

        if not isinstance(opportunity, dict):
            raise ValueError(f"Opportunity {index}: Invalid record")

        if "amount" not in opportunity:
            raise ValueError(f"Opportunity {index}: Amount is missing")

        if "probability" not in opportunity:
            raise ValueError(f"Opportunity {index}: Probability is missing")

        amount = opportunity["amount"]
        probability = opportunity["probability"]

        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            raise ValueError("Amount must be numeric")

        if amount < 0:
            raise ValueError("Amount cannot be negative")

        if not isinstance(probability, (int, float)) or isinstance(probability, bool):
            raise ValueError("Probability must be numeric")

        if probability < 0 or probability > 100:
            raise ValueError("Probability must be between 0 and 100")

    return True

