import sys
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify

# 1) Use googlesearch-python to scrape Google results (no API key needed)
#    Install via: pip install googlesearch-python
try:
    from googlesearch import search
except ImportError:
    print("ERROR: please install googlesearch-python: pip install googlesearch-python")
    sys.exit(1)

# 2) LangChain + Ollama
#    Install via: pip install langchain langchain-community langchain-ollama
from langchain_community.llms import Ollama
from langchain import LLMChain, PromptTemplate

# ── CONFIGURATION ───────────────────────────────────────────────────────────────
LLM_MODEL = "gemma2:latest"       # Make sure: ollama pull gemma2:latest
TOP_K = 3                         # how many Google URLs to fetch
MAX_CHARS_PER_PAGE = 2000         # truncate each page to ~2k chars
TRUNCATE_THRESHOLD = 3500         # truncate combined context at ~3.5k chars
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}
# ────────────────────────────────────────────────────────────────────────────────

app = Flask(__name__)

# Build a LangChain PromptTemplate + LLMChain for summarization
prompt_template = PromptTemplate(
    input_variables=["context"],
    template=(
        "Below are excerpts from live web pages relevant to your query.\n\n"
        "{context}\n\n"
        "Please write a vibrant, engaging summary in 3–5 bullet points. "
        "Highlight the most important facts and any interesting insights. "
        "Use descriptive language and mention why each point matters.\n"
    ),
)
llm = Ollama(model=LLM_MODEL)
summarization_chain = LLMChain(llm=llm, prompt=prompt_template)


def fetch_page_text(url: str, max_chars: int = MAX_CHARS_PER_PAGE) -> str:
    """
    Download `url` with a realistic headers block and return up to `max_chars` of visible text.
    If the response status is not 200 (e.g., 401 or 403), return an empty string.
    """
    try:
        resp = requests.get(url, timeout=8, headers=HEADERS)
        resp.raise_for_status()
    except Exception:
        return ""

    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "header", "footer", "nav", "aside"]):
        tag.decompose()
    visible = soup.get_text(separator=" ", strip=True)
    return visible[:max_chars]


def internet_summary(query: str, top_k: int = TOP_K) -> str:
    """
    1. Use googlesearch.search() to get the top_k URLs for `query`.
    2. Download each page’s visible text (skip any that return non-200).
    3. Concatenate & truncate into a single context string.
    4. Use LLMChain.invoke(...) to summarize that context with Gemma 2.
       Extract and return the 'text' field from the result dict.
    """
    print(f"\n>> Performing Google search for: {query!r} (top {top_k} results)")
    try:
        urls = []
        for u in search(query, num_results=top_k):
            urls.append(u)
            if len(urls) >= top_k:
                break
    except Exception as e:
        print(f"  [!] googlesearch failed: {e}")
        urls = []

    if not urls:
        print("  [!] No URLs found. Exiting.")
        return ""

    page_texts = []
    for idx, u in enumerate(urls, start=1):
        print(f"  • Fetching page {idx}: {u}")
        excerpt = fetch_page_text(u)
        if excerpt:
            page_texts.append(f"--- Page {idx}: {u} ---\n{excerpt}")

    if not page_texts:
        print("  [!] Could not fetch any page text. Exiting.")
        return ""

    combined = "\n\n".join(page_texts)
    if len(combined) > TRUNCATE_THRESHOLD:
        combined = combined[:TRUNCATE_THRESHOLD] + "\n\n[...truncated...]"

    # .invoke(...) returns a dict like {"text": "..."}
    result_dict = summarization_chain.invoke({"context": combined})
    return result_dict.get("text", "")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json or {}
    user_query = data.get("prompt", "").strip()
    if not user_query:
        return jsonify({"error": "Empty prompt"}), 400

    summary_text = internet_summary(user_query)
    if not summary_text:
        return jsonify({"error": "Failed to retrieve or summarize pages."}), 500
    return jsonify({"response": summary_text})


if __name__ == "__main__":
    # Run on port 5050, debug=True for development
    app.run(port=5050, debug=True)

