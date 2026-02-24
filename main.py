import sys

if len(sys.argv) < 2:
    print("Usage: python main.py <experiment>")
    print("Options: exp1, exp2, exp3, exp4, exp5")
    exit()

exp = sys.argv[1]

if exp == "exp1":
    from experiments.experiment1_temperature import run_exp
elif exp == "exp2":
    from experiments.experiment2_token_size import run_exp
elif exp == "exp3":
    from experiments.experiment3_hallucination import run_exp
elif exp == "exp4":
    from experiments.experiment4_zero_vs_fewshot_prompt import run_exp
elif exp == "exp5":
    from experiments.experiment5_prompt_debug import run_exp
else:
    print("Invalid experiment")
    exit()

run_exp()