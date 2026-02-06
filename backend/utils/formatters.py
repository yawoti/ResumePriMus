import re


class Formatters:
    """Text formatting utilities"""

    @staticmethod
    def clean_text(text):
        """
        Clean and normalize text

        Args:
            text (str): Input text

        Returns:
            str: Cleaned text
        """
        if not text:
            return ""

        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)

        # Remove multiple newlines (keep max 2)
        text = re.sub(r'\n{3,}', '\n\n', text)

        # Trim whitespace
        text = text.strip()

        return text

    @staticmethod
    def format_section_header(header):
        """
        Format section header consistently

        Args:
            header (str): Section header

        Returns:
            str: Formatted header
        """
        return header.strip().upper()

    @staticmethod
    def truncate_text(text, max_length=500, suffix="..."):
        """
        Truncate text to maximum length

        Args:
            text (str): Input text
            max_length (int): Maximum length
            suffix (str): Suffix to add if truncated

        Returns:
            str: Truncated text
        """
        if not text or len(text) <= max_length:
            return text

        return text[:max_length - len(suffix)] + suffix

    @staticmethod
    def extract_keywords(text, top_n=20):
        """
        Extract potential keywords from text
        (Simple implementation - can be enhanced with NLP)

        Args:
            text (str): Input text
            top_n (int): Number of keywords to extract

        Returns:
            list: List of keywords
        """
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that',
            'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they'
        }

        # Split into words and filter
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        keywords = [w for w in words if w not in stop_words]

        # Count frequency
        from collections import Counter
        word_freq = Counter(keywords)

        # Return top N most common
        return [word for word, count in word_freq.most_common(top_n)]
