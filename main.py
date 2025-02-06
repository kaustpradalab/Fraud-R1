import argparse
from attacks.BaselineAttack import BaselineAttack
from evaluation.ASR import ASRCalculator

def main():
    parser = argparse.ArgumentParser(description="Process fraud detection data using OpenAI API.")
    parser.add_argument("--mode", type=str, required=True)
    parser.add_argument("--model", type=str, default="gpt-4o-mini")

    parser.add_argument("--task_type", type=str)
    parser.add_argument("--question_input_path", type=str)
    parser.add_argument("--answer_save_path", type=str)

    parser.add_argument("--eval_input_folder", type=str)
    parser.add_argument("--eval_output_file", type=str)
    
    args = parser.parse_args()

    if args.mode == "attack":
        if args.task_type == "baseline":
            baseline = BaselineAttack()
            baseline.process_fraud_data(args.question_input_path, args.model, args.answer_save_path)
        elif args.task_type == "refine":
            pass
        elif args.task_type == "roleplay":
            pass
    elif args.mode == "eval":
        asr = ASRCalculator(args.eval_input_folder, args.eval_output_file)
        asr.run()
    
if __name__ == "__main__":
    main()
