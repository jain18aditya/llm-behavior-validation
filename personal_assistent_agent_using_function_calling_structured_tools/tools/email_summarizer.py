def email_summarizer(email_text: str):
    sentences = email_text.split(".")
    summary = sentences[0].strip()
    return {
        "summary" : summary,
        "action" : "Yes" if "please" in summary else "No"
    }