import os
import json

VALID_JUDGES = {"YES", "NO", "NEXT ROUND"}

class DSRCalculatorONE:
    def __init__(self, input_folder, output_folder):
        self.input_folder = input_folder
        self.macro_output_file = output_folder + "/by_model_results.json"
        self.micro_output_file = output_folder + "/by_cat_by_model_results.json"
        os.makedirs(output_folder, exist_ok=True)
        os.makedirs(output_folder, exist_ok=True)

    def process_file(self, file_path):
        """
        Reads the JSON file (assumed to be a list of records) and returns:
          - macro_counts: overall counts for each valid 'one-round judge' plus a 'total'
          - micro_counts: counts per category (using the "category" field)
        """
        macro_counts = {"YES": 0, "NO": 0, "NEXT ROUND": 0, "total": 0}
        micro_counts = {}  # key: category, value: dict with counts and total
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for record in data:
                    judge = record.get("one-round judge", "")
                    if judge not in VALID_JUDGES:
                        continue
                    macro_counts[judge] += 1
                    macro_counts["total"] += 1

                    category = record.get("category", "unknown")
                    if category not in micro_counts:
                        micro_counts[category] = {"YES": 0, "NO": 0, "NEXT ROUND": 0, "total": 0}
                    micro_counts[category][judge] += 1
                    micro_counts[category]["total"] += 1
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
        return macro_counts, micro_counts

    def compute_rates(self, counts):
        """
        Given a counts dictionary (with keys "YES", "NO", "NEXT ROUND", and "total"),
        compute the rate for each valid judge value in percentage (multiplied by 100)
        and round the result to 2 decimal places.
        """
        rates = {}
        total = counts.get("total", 0)
        if total > 0:
            for key in VALID_JUDGES:
                rate = (counts[key] / total) * 100
                rates[key] = round(rate, 2)
        else:
            for key in VALID_JUDGES:
                rates[key] = 0.00
        return rates

    def average_rates(self, rate1, rate2):
        """
        Averages two rate dictionaries key-wise.
        (Not used for overall, but kept for intra-task averaging if needed.)
        """
        avg = {}
        for key in VALID_JUDGES:
            avg[key] = round((rate1.get(key, 0) + rate2.get(key, 0)) / 2, 2)
        return avg

    def sum_counts(self, counts1, counts2):
        """
        Sum two counts dictionaries.
        """
        result = {}
        for key in {"YES", "NO", "NEXT ROUND", "total"}:
            result[key] = counts1.get(key, 0) + counts2.get(key, 0)
        return result

    def run(self):
        """
        Process the folder structure, calculate detailed macro and micro results for each model,
        and save the final results into two JSON files: one for macro and one for micro.
        Also compute the overall (assistant + roleplay)/combined score per model and per category
        by summing the counts and then computing the percentages.
        """
        tasks = ["assistant", "roleplay"]
        macro_results = {}
        micro_results = {}

        # Process each task separately.
        for task in tasks:
            task_path = os.path.join(self.input_folder, task)
            if not os.path.isdir(task_path):
                continue

            macro_results[task] = {}
            micro_results[task] = {}

            for model_name in os.listdir(task_path):
                model_path = os.path.join(task_path, model_name)
                if not os.path.isdir(model_path):
                    continue

                # File paths for Chinese and English results.
                chinese_file = os.path.join(model_path, "FP-base-Chinese.json")
                english_file = os.path.join(model_path, "FP-base-English.json")

                if os.path.exists(chinese_file):
                    macro_chinese, micro_chinese = self.process_file(chinese_file)
                else:
                    macro_chinese, micro_chinese = {"YES": 0, "NO": 0, "NEXT ROUND": 0, "total": 0}, {}

                if os.path.exists(english_file):
                    macro_english, micro_english = self.process_file(english_file)
                else:
                    macro_english, micro_english = {"YES": 0, "NO": 0, "NEXT ROUND": 0, "total": 0}, {}

                # For each model, compute the results for each language then combine them.
                rates_macro_chinese = self.compute_rates(macro_chinese)
                rates_macro_english = self.compute_rates(macro_english)
                combined_macro_counts = self.sum_counts(macro_chinese, macro_english)
                avg_macro = self.compute_rates(combined_macro_counts)

                # Process micro view (by category).
                all_categories = set(micro_chinese.keys()) | set(micro_english.keys())
                micro_details = {}
                for cat in all_categories:
                    counts_ch = micro_chinese.get(cat, {"YES": 0, "NO": 0, "NEXT ROUND": 0, "total": 0})
                    counts_en = micro_english.get(cat, {"YES": 0, "NO": 0, "NEXT ROUND": 0, "total": 0})
                    combined_cat_counts = self.sum_counts(counts_ch, counts_en)
                    avg_cat = self.compute_rates(combined_cat_counts)

                    micro_details[cat] = {
                        "chinese": {
                            "counts": counts_ch,
                            "rates": self.compute_rates(counts_ch)
                        },
                        "english": {
                            "counts": counts_en,
                            "rates": self.compute_rates(counts_en)
                        },
                        "combined_counts": combined_cat_counts,
                        "average_rates": avg_cat
                    }

                # Save macro and micro results for the current model under this task.
                macro_results[task][model_name] = {
                    "chinese": {
                        "counts": macro_chinese,
                        "rates": rates_macro_chinese
                    },
                    "english": {
                        "counts": macro_english,
                        "rates": rates_macro_english
                    },
                    "combined_counts": combined_macro_counts,
                    "average_rates": avg_macro
                }
                micro_results[task][model_name] = micro_details

        # Compute overall results by summing counts across tasks for each model.
        overall_macro = {}
        all_models = set()
        for task in macro_results:
            all_models.update(macro_results[task].keys())
        for model in all_models:
            # Get the combined counts from assistant and roleplay, if available.
            assistant_counts = {"YES": 0, "NO": 0, "NEXT ROUND": 0, "total": 0}
            roleplay_counts = {"YES": 0, "NO": 0, "NEXT ROUND": 0, "total": 0}
            if "assistant" in macro_results and model in macro_results["assistant"]:
                assistant_counts = macro_results["assistant"][model]["combined_counts"]
            if "roleplay" in macro_results and model in macro_results["roleplay"]:
                roleplay_counts = macro_results["roleplay"][model]["combined_counts"]
            overall_counts = self.sum_counts(assistant_counts, roleplay_counts)
            overall_macro[model] = self.compute_rates(overall_counts)

        overall_micro = {}
        all_models_micro = set()
        for task in micro_results:
            all_models_micro.update(micro_results[task].keys())
        for model in all_models_micro:
            overall_micro[model] = {}
            categories = set()
            if "assistant" in micro_results and model in micro_results["assistant"]:
                categories.update(micro_results["assistant"][model].keys())
            if "roleplay" in micro_results and model in micro_results["roleplay"]:
                categories.update(micro_results["roleplay"][model].keys())
            for cat in categories:
                assistant_counts = {"YES": 0, "NO": 0, "NEXT ROUND": 0, "total": 0}
                roleplay_counts = {"YES": 0, "NO": 0, "NEXT ROUND": 0, "total": 0}
                if "assistant" in micro_results and model in micro_results["assistant"] and cat in micro_results["assistant"][model]:
                    assistant_counts = micro_results["assistant"][model][cat]["combined_counts"]
                if "roleplay" in micro_results and model in micro_results["roleplay"] and cat in micro_results["roleplay"][model]:
                    roleplay_counts = micro_results["roleplay"][model][cat]["combined_counts"]
                overall_cat_counts = self.sum_counts(assistant_counts, roleplay_counts)
                overall_micro[model][cat] = self.compute_rates(overall_cat_counts)

        # Add the overall results as a top-level key in both outputs.
        macro_results["overall"] = overall_macro
        micro_results["overall"] = overall_micro

        # Save the macro results to a separate JSON file.
        try:
            with open(self.macro_output_file, "w", encoding="utf-8") as f_out:
                json.dump(macro_results, f_out, indent=4, ensure_ascii=False)
            print(f"Macro results saved to {self.macro_output_file}")
        except Exception as e:
            print(f"Error saving macro results: {e}")

        # Save the micro results to a separate JSON file.
        try:
            with open(self.micro_output_file, "w", encoding="utf-8") as f_out:
                json.dump(micro_results, f_out, indent=4, ensure_ascii=False)
            print(f"Micro results saved to {self.micro_output_file}")
        except Exception as e:
            print(f"Error saving micro results: {e}")
