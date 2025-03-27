import logging
import os
import csv
import docs.appendices as appendices


class AdditelError(Exception):
    _error_lookup = None

    def __init__(self, error_code, error_message):
        self.error_code = error_code
        self.error_message = error_message

        if AdditelError._error_lookup is None:
            AdditelError._error_lookup = self._load_error_lookup()

        err_desc, err_explain = AdditelError._error_lookup.get(
            error_code, ("Unknown error", "No explanation available.")
        )

        self.error_description = err_desc
        self.error_explanation = err_explain

        message = f"[{error_code}] {error_message} — {err_desc}: {err_explain}"
        logging.error(f"Error reading response: {message}")
        super().__init__(message)

    @staticmethod
    def _load_error_lookup():
        lookup = {}
        path = os.path.join(appendices.__path__[0], "Table 3 - Error Definition.csv")
        with open(path, mode="r", newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    code = int(row["Error code"].strip())
                    desc = row["Error description"].strip()
                    explain = row["Explain"].strip()
                    lookup[code] = (desc, explain)
                except (ValueError, KeyError):
                    continue  # skip malformed rows
        return lookup
