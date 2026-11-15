from backend.validation import validate_opportunities


def process_opportunities(opportunities):
    validate_opportunities(opportunities)

    return {
        "total_opportunities": len(opportunities),
        "message": "Opportunities validated successfully"
    }