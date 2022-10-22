from typing import List
from collections import Counter
from discord import Message
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


class BotStats:
    @staticmethod
    def top_words(messages: List[Message]) -> Counter:
        all_words: List[str] = []
        for msg in messages:
            tokens: List[str] = [
                word.lower() for word in word_tokenize(msg.content) if word.isalpha()
            ]
            tokens = BotStats.remove_stopwords(tokens)
            all_words += tokens
        all_words_count: Counter = Counter(all_words)
        return all_words_count

    @staticmethod
    def top_words_per_member(messages: List[Message], member: str):
        all_words: List[str] = []
        for msg in messages:
            if msg.author.name == member:
                tokens: List[str] = [
                    word.lower()
                    for word in word_tokenize(msg.content)
                    if word.isalpha()
                ]
                tokens = BotStats.remove_stopwords(tokens)
                all_words += tokens
        all_words_count: Counter = Counter(all_words)
        return all_words_count

    @staticmethod
    def remove_stopwords(tokens: List[str]) -> List[str]:
        """Remove french and english stopwords from a list of tokens.

        Parameters
        ----------
        tokens : list
            A list of raw tokens without punctuation.

        Returns
        -------
        list
            A list of tokens without stopwords.
        """
        tokens_no_stopwords: List[str] = []
        for token in tokens:
            if token not in stopwords.words("french"):
                if token not in stopwords.words("english"):
                    tokens_no_stopwords.append(token)
        return tokens_no_stopwords
