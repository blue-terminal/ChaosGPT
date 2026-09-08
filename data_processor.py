"""
data_processor.py
-----------------
Script pratico per l'analisi statistica e la manipolazione di testi e dati.
Mostra l'uso di:
- Espressioni regolari (regex) per la pulizia del testo
- Strutture dati standard (Counter, dict, list)
- Funzioni modulari e type hints
"""

import re
from collections import Counter
from typing import Dict, List, Any


class TextProcessor:
    # Parole comuni italiane da escludere nell'analisi delle parole chiave
    STOPWORDS = {
        "il", "lo", "la", "i", "gli", "le", "un", "uno", "una",
        "di", "a", "da", "in", "con", "su", "per", "tra", "fra",
        "e", "o", "ma", "che", "chi", "cui", "non", "si", "ci",
        "ed", "ad", "ha", "hanno", "sono", "era", "stato", "come"
    }

    def __init__(self, text: str):
        self.raw_text = text.strip()

    def clean_words(self) -> List[str]:
        """Estrae tutte le parole, rimuovendo punteggiatura e convertendo in minuscolo."""
        # Trova tutte le sequenze di caratteri alfanumerici
        words = re.findall(r'\b[a-zA-ZàèéìòùÀÈÉÌÒÙ]+\b', self.raw_text.lower())
        return words

    def calculate_stats(self) -> Dict[str, Any]:
        """Calcola le metriche statistiche fondamentali del testo."""
        words = self.clean_words()
        total_words = len(words)
        unique_words = len(set(words))
        
        # Conteggio dei caratteri (inclusi ed esclusi spazi)
        chars_with_spaces = len(self.raw_text)
        chars_no_spaces = len(self.raw_text.replace(" ", ""))

        # Calcolo frasi (stima basata sulla punteggiatura finale)
        sentences = [s.strip() for s in re.split(r'[.!?]+', self.raw_text) if s.strip()]
        total_sentences = max(1, len(sentences))

        # Lunghezza media della parola
        avg_word_len = sum(len(w) for w in words) / max(1, total_words)

        # Stima tempo di lettura (velocità media: ~200 parole al minuto)
        reading_time_seconds = round((total_words / 200) * 60, 1)

        return {
            "total_words": total_words,
            "unique_words": unique_words,
            "total_sentences": total_sentences,
            "chars_total": chars_with_spaces,
            "chars_no_spaces": chars_no_spaces,
            "avg_word_length": round(avg_word_len, 2),
            "estimated_reading_seconds": reading_time_seconds
        }

    def get_top_keywords(self, top_n: int = 5) -> List[tuple]:
        """Identifica le parole chiave più rilevanti escludendo le stopwords."""
        words = self.clean_words()
        # Filtra le parole vuote o troppo corte (< 3 caratteri)
        meaningful_words = [
            w for w in words if w not in self.STOPWORDS and len(w) >= 3
        ]
        counter = Counter(meaningful_words)
        return counter.most_common(top_n)

    def generate_report(self) -> str:
        """Formatta i risultati in un report leggibile da console."""
        stats = self.calculate_stats()
        keywords = self.get_top_keywords(5)

        lines = [
            "=" * 50,
            "         REPORT ANALISI DEL TESTO",
            "=" * 50,
            f"Parole totali:              {stats['total_words']}",
            f"Parole uniche (vocabolario): {stats['unique_words']}",
            f"Frasi totali:               {stats['total_sentences']}",
            f"Caratteri (con spazi):      {stats['chars_total']}",
            f"Caratteri (senza spazi):    {stats['chars_no_spaces']}",
            f"Lunghezza media parole:     {stats['avg_word_length']} caratteri",
            f"Tempo di lettura stimato:   {stats['estimated_reading_seconds']} secondi",
            "-" * 50,
            "TOP PAROLE CHIAVE PIÙ FREQUENTI:"
        ]

        for rank, (word, count) in enumerate(keywords, start=1):
            lines.append(f"  {rank}. '{word}': {count} occorrenze")

        lines.append("=" * 50)
        return "\n".join(lines)


if __name__ == "__main__":
    # Testo di prova
    sample_text = (
        "La programmazione e l'informatica sono strumenti potenti per automatizzare compiti "
        "e risolvere problemi complessi. Scrivere codice pulito ed efficiente richiede pratica "
        "e comprensione delle strutture dati. In Python, è semplice manipolare testi e numeri, "
        "creando applicazioni affidabili e modulari."
    )

    processor = TextProcessor(sample_text)
    print(processor.generate_report())
