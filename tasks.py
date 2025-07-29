import os, time, re, csv
from celery import Celery
from newspaper import Article, Config
from filelock import FileLock
import celeryconfig

app = Celery('scraper')
app.conf.update(celeryconfig.__dict__)

OUTPUT = os.getenv('OUTPUT_CSV')
LOCK = FileLock(OUTPUT + '.lock')
FIELDNAMES = ['URL', 'Actual_URL', 'title', 'text', 'published_date']

# Ensure header is present
if not os.path.exists(OUTPUT):
    with LOCK, open(OUTPUT,'w',newline='',encoding='utf-8') as f:
        csv.DictWriter(f,FIELDNAMES).writeheader()

# Newspaper3k setup
tconfig = Config(browser_user_agent="Mozilla/...", request_timeout=10)

def clean_text(text): return re.sub(r"\s+"," ",text).strip() if text else ''

def extract_content(url):
    info = {k: None for k in FIELDNAMES[2:]}
    try:
        art = Article(url, config=tconfig)
        art.download(); art.parse()
        info.update({
            'title': art.title,
            'text': clean_text(art.text),
            'published_date': art.publish_date.isoformat() if art.publish_date else None
        })
    except Exception as e:
        info['text'] = f"[Error] {e}"
    return info

@app.task(bind=True)
def resolve_url(self, wrapper_url):
    # Selenium logic...
    return {'URL': wrapper_url, 'Actual_URL': real_url}

@app.task(bind=True)
def scrape_article(self, data):
    rec = extract_content(data['Actual_URL']) if data['Actual_URL'] else {k: None for k in FIELDNAMES[2:]}
    rec.update({'URL': data['URL'], 'Actual_URL': data['Actual_URL']})
    with LOCK, open(OUTPUT,'a',newline='',encoding='utf-8') as f:
        csv.DictWriter(f,FIELDNAMES).writerow(rec)
    return rec
