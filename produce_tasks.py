import os
import pandas as pd
from celery import chain
from tasks import resolve_url, scrape_article

# Path to the input CSV of ~1.6 million URLs (set via env var)
input_path = os.getenv('MERGED_INPUT','merged_output.csv')
# For smoke test: use .head(1000); for full run on 1.6M URLs, remove .head()
df = pd.read_csv(input_path).head(1000)

for url in df['URL'].dropna():
    chain(resolve_url.s(url), scrape_article.s()).apply_async()
```python
import os
import pandas as pd
from celery import chain
from tasks import resolve_url, scrape_article

# Path to input CSV
input_path = os.getenv('MERGED_INPUT','merged_output.csv')
# For smoke test, use .head(1000); remove for full run
df = pd.read_csv(input_path).head(1000)

for url in df['URL'].dropna():
    chain(resolve_url.s(url), scrape_article.s()).apply_async()
