import argparse
from evaluation.OneRoundDSR import DSRCalculatorONE
from evaluation.MultiRoundDSR import DSRCalculatorMUL
from attacks.LevelAttack import LevelAttack
from datacreation.Inducement import InducementCreate

def main():
    parser = argparse.ArgumentParser(description="Process fraud detection data using OpenAI API.")
    parser.add_argument("--mode", type=str, required=True, help="Mode: attack or eval")
    parser.add_argument("--model", type=str, help="Model name to use for baseline or refinement tasks as victim model")
    
    parser.add_argument("--attack_type", type=str, choices=["baseline", "LevelAttack"], help="Task type: baseline, LevelAttack")
    parser.add_argument("--sub_task", type=str, choices=["one-round", "multi-round", "one-round-eval"], help="sub_task type: one-round, multi-round or one-round-eval")
    parser.add_argument("--scenario", type=str, choices=["assistant", "roleplay"], help="Scenario type: assistant or roleplay")
    
    parser.add_argument("--question_input_path", type=str, help="Path to input data file")
    parser.add_argument("--answer_save_path", type=str, help="Path to save processed data file")

    parser.add_argument("--eval_input_folder", type=str, help="Evaluation input folder")
    parser.add_argument("--eval_output_file", type=str, help="Evaluation output file")
    parser.add_argument("--eval_type", type=str, help="one-round or multi-round")

    parser.add_argument("--attacker", type=str, help="attacker name to use for refinement tasks or role-play")
    parser.add_argument("--refine_cap", type=int, default=5, help="Maximum number of refinement rounds")
    
    args = parser.parse_args()

    if args.mode == "attack":
        if args.attack_type == "baseline":
            baseline = BaselineAttack(args.question_input_path, args.model, args.answer_save_path)
            baseline.process_fraud_data()
        elif args.attack_type == "LevelAttack":
            level = LevelAttack(args.question_input_path, args.model, args.answer_save_path, args.sub_task, args.scenario)
            level.process_fraud_data()
    elif args.mode == "eval":
        if args.eval_type == "one-round":
            dsr = DSRCalculatorONE(args.eval_input_folder, args.eval_output_file)
            dsr.run()
        elif args.eval_type == "multi-round":
            dsr = DSRCalculatorMUL(args.eval_input_folder, args.eval_output_file)
            dsr.run()
    elif args.mode == "data":
        r1 = InducementCreate(args.question_input_path, args.answer_save_path)
        r1.process_data_generation()
    
if __name__ == "__main__":
    main()
