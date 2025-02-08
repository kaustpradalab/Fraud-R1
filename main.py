import argparse
from attacks.BaselineAttack import BaselineAttack
from evaluation.ASR import ASRCalculator
from attacks.RefinementAttack import RefinementAttack
from attacks.BaseAttack import BaseAttack

def main():
    parser = argparse.ArgumentParser(description="Process fraud detection data using OpenAI API.")
    parser.add_argument("--mode", type=str, required=True, help="Mode: attack or eval")
    parser.add_argument("--model", type=str, help="Model name to use for baseline or refinement tasks as victim model")
    
    parser.add_argument("--task_type", type=str, help="Task type: baseline, base, refinement, or roleplay")
    parser.add_argument("--question_input_path", type=str, help="Path to input data file")
    parser.add_argument("--answer_save_path", type=str, help="Path to save processed data file")
    parser.add_argument("--eval_input_folder", type=str, help="Evaluation input folder")
    parser.add_argument("--eval_output_file", type=str, help="Evaluation output file")

    parser.add_argument("--attacker", type=str, help="attacker name to use for refinement tasks or role-play")
    parser.add_argument("--refine_cap", type=int, default=5, help="Maximum number of refinement rounds")
    
    args = parser.parse_args()

    if args.mode == "attack":
        if args.task_type == "baseline":
            baseline = BaselineAttack(args.question_input_path, args.model, args.answer_save_path)
            baseline.process_fraud_data()
        elif args.task_type == "refinement":
            # 调用 RefinementAttack，传入 attacker, victim, file_name, output_file, refine_cap
            refinement = RefinementAttack(
                args.attacker,          # attacker
                args.model,          # victim
                args.question_input_path,  # file_name
                args.answer_save_path,     # output_file
                args.refine_cap      # refine_cap
            )
            refinement.process_refinement()
        elif args.task_type == "base":
            baseline = BaseAttack(args.question_input_path, args.model, args.answer_save_path)
            baseline.process_fraud_data()
        elif args.task_type == "roleplay":
            # 根据实际需求实现 roleplay 模式
            pass
    elif args.mode == "eval":
        asr = ASRCalculator(args.eval_input_folder, args.eval_output_file)
        asr.run()
    
if __name__ == "__main__":
    main()
