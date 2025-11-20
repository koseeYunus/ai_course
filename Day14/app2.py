import arxiv
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# ----------- 1. Fetch Academic Papers from arXiv -----------
def fetch_arxiv_papers(query="hydrogen energy", max_results=3):
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate
    )
    papers = []
    for result in search.results():
        papers.append({
            "title": result.title.strip(),
            "summary": result.summary.strip(),
            "url": result.entry_id
        })
    return papers

# ----------- 2. Fetch News from Google News RSS -----------
def fetch_google_news(query="hydrogen energy", max_articles=3):
    url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)
    news_items = []
    for entry in feed.entries[:max_articles]:
        news_items.append({
            "title": entry.title.strip(),
            "summary": entry.summary.strip(),
            "link": entry.link
        })
    return news_items

# ----------- 3. Scrape Company News from Plug Power -----------
def scrape_plug_power_news(max_articles=3):
    url = "https://www.plugpower.com/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select("div.news-list-item")
    news_items = []
    for article in articles[:max_articles]:
        title = article.select_one("h3").get_text(strip=True)
        summary = article.select_one("p").get_text(strip=True)
        link = article.find("a")["href"]
        news_items.append({
            "title": title,
            "summary": summary,
            "link": link
        })
    return news_items

# ----------- 4. Summarize using OpenRouter model -----------
def summarize_items_openrouter(items, section_title, api_key):
    combined_text = "\n\n".join([f"Title: {item['title']}\nSummary: {item['summary']}" for item in items])
    prompt = f"""You're an energy analyst. Summarize the following {section_title.lower()} into 3–5 concise bullet points:\n\n{combined_text}"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        json={
            "model": "qwen/qwen2.5-vl-32b-instruct:free",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        headers={
            "Authorization": f"Bearer {api_key}"
        }
    )

    result = response.json()
    return result["choices"][0]["message"]["content"].strip()

# ----------- 5. Build the Daily Report -----------
def build_daily_report(api_key):
    today = datetime.today().strftime('%Y-%m-%d')
    report = f"# 🔋 Daily Hydrogen Energy Report ({today})\n\n"

    print("Fetching academic papers from arXiv...")
    arxiv_data = fetch_arxiv_papers()

    print("Fetching news from Google News...")
    google_news_data = fetch_google_news()

    print("Scraping Plug Power company news...")
    plug_news_data = scrape_plug_power_news()

    print("Summarizing arXiv papers with OpenRouter...")
    arxiv_summary = summarize_items_openrouter(arxiv_data, "Academic Papers", api_key)
    report += "## 📘 Academic Papers (arXiv)\n" + arxiv_summary + "\n\n"

    print("Summarizing news articles with OpenRouter...")
    news_summary = summarize_items_openrouter(google_news_data, "News Articles", api_key)
    report += "## 🗞 News Articles (Google News)\n" + news_summary + "\n\n"

    print("Summarizing Plug Power news with OpenRouter...")
    company_summary = summarize_items_openrouter(plug_news_data, "Company News", api_key)
    report += "## 🏭 Company Update: Plug Power\n" + company_summary + "\n\n"

    return report

# ----------- 6. Run It! -----------
if __name__ == "__main__":
    API_KEY = "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"  # Replace with your actual API key
    final_report = build_daily_report(API_KEY)
    print(final_report)
