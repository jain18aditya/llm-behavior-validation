import sys

if len(sys.argv) < 2:
    print("Usage: python main.py <experiment>")
    print("Options: exp1, exp2, exp3, exp4, exp5")
    exit()

exp = sys.argv[1]

if exp == "exp1":
    from experiments.temperature_experiment import run_exp
# elif exp == "exp2":
#     from experiments.exp2_token_impact import run
# elif exp == "exp3":
#     from experiments.exp3_json_output import run
# elif exp == "exp4":
#     from experiments.exp4_fewshot_vs_zeroshot import run
# elif exp == "exp5":
#     from experiments.exp5_prompt_debugging import run
# else:
#     print("Invalid experiment")
#     exit()

run_exp()