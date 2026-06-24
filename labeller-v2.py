import pandas as pd
import re

df = pd.read_csv("cleaned_app_reviews.csv") # column: clean_text


def norm(text):
    text = "" if text is None else str(text).lower()
    text = re.sub(r"[^\w\s']", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

PHRASES = {
    "switch_trigger": [
        r"\b(?:i\s+am|i'm|we're|i'm\s+just|i\s+am\s+just)?\s*(?:switching|switched|moving|moved|going|went)\s+(?:to|over\s+to|back\s+to)\s+\w+",
        r"\b(?:deleted|uninstalled|cancelled|canceled|refunded)\b",
        r"\b(?:i\s+am\s+deleting|i'm\s+deleting|i\s+am\s+uninstalling|i'm\s+uninstalling)\b",
        r"\b(?:won't|will\s+not)\s+use\s+(?:this|it)\s+again\b",
        r"\b(?:never|not)\s+(?:using|use)\s+(?:this|it)\s+again\b",
        r"\b(?:back\s+to|returning\s+to|reverting\s+to)\s+\w+",
        r"\b(?:not\s+worth\s+(?:keeping|the\s+money|paying\s+for)|not\s+worth\s+it)\b",
        r"\b(?:getting|got)\s+a\s+refund\b",
    ],

    "trust_reliability_break": [
        r"\b(?:keeps?|keep)\s+(?:crashing|freezing|lagging|stopping|breaking)\b",
        r"\b(?:crash|freeze|hang|lock|bug|glitch)\w*\b",
        r"\b(?:app|system|service)\s+(?:is|was)\s+(?:broken|unstable|unreliable|buggy)\b",
        r"\b(?:does|do)\s+not\s+work\b",
        r"\b(?:won't|will\s+not)\s+(?:load|open|start|sync|save)\b",
        r"\b(?:lost|losing)\s+(?:all\s+my\s+)?data\b",
        r"\bdata\s+(?:loss|missing|gone|deleted)\b",
        r"\bsync(?:ing)?\s+(?:fails?|failed|failure|issues?|problems?)\b",
        r"\bwrong\s+(?:results?|answers?|data|information)\b",
        r"\b(?:cannot|can't|couldn't)\s+trust\s+(?:it|this\s+app)\b",
        r"\bbilling\s+(?:issue|error|problem|bug)\b",
        r"\bcharged\s+me\b",
        r"\bsubscription\s+(?:didn't\s+work|not\s+working|failed)\b",
    ],

    "core_job_blocked": [
        r"\b(?:cannot|can't|couldn't|unable\s+to)\s+(?:complete|finish|do|perform)\s+(?:the\s+)?(?:main|core|primary)\s+(?:task|job|workflow|purpose)\b",
        r"\b(?:main|core|primary)\s+(?:task|workflow|function|purpose)\s+(?:is\s+)?(?:broken|blocked|failing|not\s+working)\b",
        r"\b(?:app|this\s+app|it)\s+(?:is\s+)?(?:useless|unusable)\s+for\s+(?:my\s+)?(?:workflow|job|purpose|needs?)\b",
        r"\b(?:cannot|can't|couldn't|unable\s+to)\s+use\s+(?:it|this\s+app)\s+for\s+(?:my\s+)?(?:work|job|task|workflow)\b",
        r"\b(?:key|main|core)\s+workflow\s+(?:is\s+)?(?:broken|blocked|failing)\b",
        r"\b(?:the\s+)?(?:app|product)\s+fails?\s+at\s+(?:the\s+)?(?:main|core|primary)\s+(?:job|task|workflow)\b",
        r"\b(?:does|do)\s+not\s+let\s+me\s+(?:complete|finish|do)\s+(?:the\s+)?(?:task|job|workflow)\b",
        r"\b(?:cannot|can't)\s+use\s+this\s+for\s+its\s+intended\s+purpose\b",
    ],

    "painful_workaround": [
        r"\b(?:had|have)\s+to\s+use\s+(?:another|a\s+different)\s+(?:app|tool|service)\b",
        r"\b(?:had|have)\s+to\s+switch\s+to\s+(?:another|a\s+different)\s+(?:app|tool|service)\b",
        r"\b(?:manual|manually)\s+(?:export|enter|copy|paste|upload|sync|save)\b",
        r"\b(?:export|download|save)\s+(?:it|them)?\s+(?:every\s+time|each\s+time)\b",
        r"\b(?:repeat|redo|re-enter|retype)\s+(?:the\s+)?(?:same\s+)?(?:steps?|process|work)\b",
        r"\b(?:extra|more)\s+steps?\s+to\s+(?:get\s+it\s+to\s+work|do\s+anything|finish)\b",
        r"\b(?:workaround|hack|fix)\b",
        r"\b(?:copy\s+and\s+paste|copy-paste)\b",
        r"\b(?:doing\s+it\s+by\s+hand|do\s+it\s+by\s+hand)\b",
        r"\b(?:using\s+the\s+website|using\s+the\s+desktop\s+version|using\s+email)\s+instead\b",
    ],

    "must_have_gap": [
        r"\bneed\s+(?:an?\s+)?offline\s+mode\b",
        r"\bneed\s+(?:an?\s+)?export(?:ing)?\b",
        r"\bneed\s+(?:an?\s+)?backup\b",
        r"\bneed\s+(?:an?\s+)?search\b",
        r"\bneed\s+(?:an?\s+)?filter(?:s)?\b",
        r"\bneed\s+(?:an?\s+)?sync\b",
        r"\bwithout\s+(?:export|offline\s+mode|backup|sync)\s+(?:this|it)?\s*(?:is\s+)?(?:useless|unusable|pointless|hard\s+to\s+use)\b",
        r"\b(?:must\s+have|must-have)\b",
        r"\b(?:essential|required|critical|vital)\s+for\b",
        r"\bthis\s+app\s+needs\s+.+\s+to\s+be\s+(?:usable|useful|worth\s+using)\b",
        r"\bcan't\s+use\s+it\s+without\b",
        r"\bwon't\s+work\s+for\s+me\s+without\b",
        r"\bneed\s+the\s+ability\s+to\b",
        r"\bshould\s+have\b.*\b(?:otherwise|or\s+else)\b.*\b(?:can't use|won't use|useless)\b",
    ],
}

ORDER = [
    "switch_trigger",
    "trust_reliability_break",
    "core_job_blocked",
    "painful_workaround",
    "must_have_gap",
]

COMPILED = {k: [re.compile(p, re.I) for p in v] for k, v in PHRASES.items()}

def tag_review(text):
    t = norm(text)
    out = [label for label in ORDER if any(p.search(t) for p in COMPILED[label])]
    return out or ["none"]


# Example:
df["code"] = df["clean_text"].apply(tag_review)

print(df[["clean_text", "code"]].head(10)) # Display the cleaned review text and labels for the first 10 rows

# Save the DataFrame with the new columns to a new CSV file
df.to_csv("coded_app_reviews.csv", index=False) 
print("Saved reviews to coded_app_reviews.csv")