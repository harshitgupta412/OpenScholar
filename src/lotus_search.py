from lotus.web_search import WebSearchCorpus, web_search
import pandas as pd
from datetime import timedelta, datetime
import time

def search_paper_via_query(query, max_paper_num=10, corpus=[WebSearchCorpus.ARXIV], end_date: datetime | None = None):
    collected_results = []
    for corpus in corpus:
        count = 5
        while True:
            try:
                df = web_search(
                    corpus,
                    query,
                    max_paper_num,
                    None,
                    False,
                )
                break
            except Exception as e:
                print(f"Error searching for query: {query}")
                print(e)
                time.sleep(1)
                count -= 1
                if count == 0:
                    df = pd.DataFrame(columns=["title", "url", "snippet", "query", "context"])
                    break
        if len(df) == 0:
            print(f"No results found for query: {query}")
            continue
        df["query"] = query
        if corpus == WebSearchCorpus.ARXIV:
            df.rename(
                columns={
                    "abstract": "snippet",
                    "link": "url",
                    "published": "date",
                },
                inplace=True,
            )
            df["date"] = df["date"].astype(str)
        elif (
            corpus == WebSearchCorpus.GOOGLE
            or corpus == WebSearchCorpus.GOOGLE_SCHOLAR
        ):
            df.rename(columns={"link": "url"}, inplace=True)
        elif corpus == WebSearchCorpus.BING:
            df.rename(columns={"name": "title"}, inplace=True)
        elif corpus == WebSearchCorpus.TAVILY:
            df.rename(columns={"content": "snippet"}, inplace=True)

        if end_date and "date" in df.columns:
            end_date = end_date - timedelta(days=1)
            try:
                df["_date"] = pd.to_datetime(df["date"], errors='coerce')
                df = df[df["_date"].dt.date <= end_date.date()]
                df.drop(columns=["_date"], inplace=True)
            except Exception as e:
                print(f"Error processing date for query: {query}")
                print(e)
                continue

        if len(df) > max_paper_num:
            df = df.head(max_paper_num)

        for _, row in df.iterrows():
            result = {
                "paperId": row["url"],
                "url": row["url"],
                "title": row["title"],
                "year": row["date"].split("-")[0] if row["date"] else None,
                "publicationDate": row["date"] if row["date"] else None,
                "abstract": row["snippet"],
                "text": row["snippet"],
                "citationCount": -1,
            }
            collected_results.append(result)
    return collected_results