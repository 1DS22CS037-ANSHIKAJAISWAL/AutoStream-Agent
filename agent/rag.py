import json

with open("data/knowledge_base.json") as f:
    KB = json.load(f)

def retrieve_knowledge(query: str) -> str:
    q = query.lower()

    if "policy" in q or "refund" in q or "support" in q:
        return (
            "Company Policies:\n"
            "- No refunds after 7 days\n"
            "- 24/7 support available only on Pro plan"
        )

    basic = KB["pricing"]["basic"]
    pro = KB["pricing"]["pro"]

    return (
        "AutoStream Pricing:\n\n"
        f"Basic Plan:\nPrice: {basic['price']}\nFeatures: {', '.join(basic['features'])}\n\n"
        f"Pro Plan:\nPrice: {pro['price']}\nFeatures: {', '.join(pro['features'])}"
    )
