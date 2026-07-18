import arxiv


class SearchAgent:
    def search_papers(self, query: str, max_results: int = 5):
        """
        Search arXiv for research papers.
        """

        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )

        papers = []

        for result in search.results():
            papers.append(
                {
                    "title": result.title,
                    "authors": [author.name for author in result.authors],
                    "summary": result.summary,
                    "published": str(result.published.date()),
                    "pdf_url": result.pdf_url,
                }
            )

        return papers