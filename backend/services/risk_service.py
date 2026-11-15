
from backend.validation import validate_opportunities


def identify_risks(opportunities):
    validate_opportunities(opportunities)

    risky_deals = []

    for deal in opportunities:
        reasons = []

        if deal.get("days_open", 0) >= 60:
            reasons.append("Opportunity is open for too long")

        if deal["probability"] <= 25:
            reasons.append("Low conversion probability")

        if reasons:
            risk_level = "High" if len(reasons) == 2 else "Medium"

            risky_deals.append({
                "name": deal.get("name", "Unnamed opportunity"),
                "amount": deal["amount"],
                "risk_level": risk_level,
                "reasons": reasons
            })

    return risky_deals

