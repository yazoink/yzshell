def write_file(src, dest):
    content = ""
    with open(src, "r") as f:
        content = f.read()
    with open(dest, "w") as f:
        f.write(content)

def prompt_y_n(prompt):
    yes = ["", "y", "yes"]
    no = ["n", "no"]
    while True:
        i = input(f">> {prompt} (Y/n): ").lower().strip()
        if i in yes:
            return True
        elif i in no:
            return False