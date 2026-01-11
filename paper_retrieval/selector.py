"""
Paper selection and ranking logic.
"""
import logging
import random
from typing import List
from paper_retrieval.models import PaperMetadata

logger = logging.getLogger(__name__)


class PaperSelector:
    """
    Handles intelligent selection and ranking of papers.
    """
    
    @staticmethod
    def rank_papers(papers: List[PaperMetadata]) -> List[PaperMetadata]:
        """
        Rank papers by: relevance (already sorted by API) → citationCount → year → openAccessPdf.
        
        The Semantic Scholar API already returns results sorted by relevance,
        so we maintain that order but then refine by other criteria.
        
        Args:
            papers: List of papers to rank
            
        Returns:
            Ranked list of papers
        """
        if not papers:
            return []
        
        def sort_key(paper: PaperMetadata) -> tuple:
            """
            Sort key: (has_pdf, citation_count, year)
            - has_pdf: False (0) comes before True (1), so we negate to prioritize True
            - citation_count: Higher is better (descending)
            - year: Higher is better (descending, recent papers preferred)
            """
            has_pdf = 1 if paper.has_open_pdf() else 0
            citation_count = paper.citationCount or 0
            year = paper.year or 0
            
            # Negate has_pdf so True (1) becomes -1, which sorts before False (0)
            # This means papers with PDFs come first
            return (-has_pdf, -citation_count, -year)
        
        ranked = sorted(papers, key=sort_key)
        logger.info(f"Ranked {len(ranked)} papers")
        return ranked
    
    @staticmethod
    def select_papers(
        papers: List[PaperMetadata],
        max_papers: int,
        prioritize_pdfs: bool = True,
        randomize: bool = False,
        diversity_factor: float = 0.0
    ) -> List[PaperMetadata]:
        """
        Select top papers based on ranking, with optional PDF prioritization.
        
        Args:
            papers: List of papers to select from
            max_papers: Maximum number of papers to select
            prioritize_pdfs: If True, prefer papers with open-access PDFs
            randomize: If True, randomly select from top-ranked papers instead of always top N
            diversity_factor: 0.0-1.0, how much to diversify selection (0=top only, 1=fully random)
                           Only used if randomize=True. Higher values select from wider range.
        
        Returns:
            Selected list of papers
        """
        if not papers:
            logger.warning("No papers provided for selection")
            return []
        
        # Rank papers
        ranked = PaperSelector.rank_papers(papers)
        
        if randomize and len(ranked) > max_papers:
            # Select from a wider pool for diversity
            # diversity_factor determines how far down the list we look
            # 0.0 = only top papers, 1.0 = entire list
            pool_size = max(
                max_papers,
                int(len(ranked) * (0.1 + 0.9 * diversity_factor))  # At least top 10%, up to 100%
            )
            pool = ranked[:pool_size]
            selected = random.sample(pool, min(max_papers, len(pool)))
            logger.info(f"Randomly selected {len(selected)} papers from top {pool_size} ranked papers")
        else:
            # Select top papers (deterministic)
            selected = ranked[:max_papers]
        
        # Count papers with PDFs
        papers_with_pdfs = sum(1 for p in selected if p.has_open_pdf())
        
        logger.info(
            f"Selected {len(selected)} papers "
            f"({papers_with_pdfs} with open-access PDFs)"
        )
        
        return selected

