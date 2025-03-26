import re

class Utils:
    def __init__(self):
        self.patterns = {
            'price': [
                r'\b(?:\$|€|£|USD|EUR|GBP)?\s?(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)\b',
                r'\b(?:\$|€|£)?(\d+(?:\.\d{1,2})?)\s*[-~]\s*(?:\$|€|£)?(\d+(?:\.\d{1,2})?)\b',
                r'\b(\d+(?:\.\d{1,2})?)([KkMmBbTt])\b',
                r'\b(?:\$|€|£)?(\d{4,})(?:\$|€|£)?\b'
            ],
            'year': [
                r'\b(19\d{2}|20\d{2})\b',
                r'\b(\d{4})\s*(?:model|year|edition|released|version)\b'
            ],
            'model_number': [
                r'\b([A-Z]+(?:\s?\d{1,4}[A-Z]*)+)\b',
                r'\b(\d{3,4}\s?[A-Z]?)\b',
                r'\b([A-Z]\s?\d{3,4})\b'
            ]
        }

    def format_large_number(self, number):
        units = ['', 'K', 'M', 'B', 'T']
        abs_number = abs(number)
        i = 0
        while abs_number >= 1000 and i < len(units) - 1:
            abs_number /= 1000
            i += 1
        formatted_number = f'{abs_number:.1f}'.rstrip('0').rstrip('.')
        sign = '-' if number < 0 else ''
        return f'{sign}{formatted_number}{units[i]}'

    def parse_suffix_number(self, value, suffix):
        multipliers = {'K': 1_000, 'M': 1_000_000, 'B': 1_000_000_000, 'T': 1_000_000_000_000}
        return float(value) * multipliers.get(suffix.upper(), 1)

    def extract_matches(self, query, pattern):
        matches = re.findall(pattern, query)
        extracted = []
        for match in matches:
            if isinstance(match, tuple) and len(match) == 2:
                extracted.append(self.parse_suffix_number(match[0], match[1]))
            else:
                extracted.append(float(match.replace(',', '')) if isinstance(match, str) and match.replace(',',
                                                                                                           '').isdigit() else match)
        return extracted

    def extract_years(self, query):
        years = []
        for pattern in self.patterns['year']:
            years.extend(self.extract_matches(query, pattern))
        return sorted(set(int(y) for y in years))

    def extract_model_numbers(self, query):
        models = []
        for pattern in self.patterns['model_number']:
            models.extend(self.extract_matches(query, pattern))

        models = [m.strip() for m in models if isinstance(m, str)]
        return sorted(set(models))

    def extract_prices(self, query):
        prices = []
        for pattern in self.patterns['price']:
            prices.extend(self.extract_matches(query, pattern))

        years = self.extract_years(query)
        models = self.extract_model_numbers(query)

        prices = [p for p in prices if p not in years and str(int(p)) not in models]

        return sorted(set(prices))

    def classify_numbers(self, query):
        years = self.extract_years(query)
        models = self.extract_model_numbers(query)
        prices = self.extract_prices(query)

        return prices
