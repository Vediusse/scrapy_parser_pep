import csv
from datetime import datetime
from pathlib import Path

from pep_parse.items import PepParseItem

BASE_DIR = Path(__file__).absolute().parent.parent
DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"


class PepParsePipeline:
    def __init__(self):
        self.pep_statuses = {}

    def open_spider(self, spider):
        pass

    def process_item(self, item: PepParseItem, spider):
        pep_status = item["status"]
        if pep_status not in self.pep_statuses.keys():
            self.pep_statuses[pep_status] = 1
        else:
            self.pep_statuses[pep_status] += 1

        return item

    def close_spider(
            self,
            spider,
    ):
        results = [("Статус", "Количество")]
        for keys, values in self.pep_statuses.items():
            results.append((keys, values))
        results.append(
            ("Total", sum(self.pep_statuses.values())),
        )

        results_dir = BASE_DIR / "results"
        results_dir.mkdir(exist_ok=True)

        now = datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f"status_summary_{now_formatted}.csv"
        file_path = results_dir / file_name
        with open(file_path, "w", encoding="utf-8") as f:
            writer = csv.writer(f, dialect="unix")
            writer.writerows(results)
