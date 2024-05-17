def save_fb(name, email, feedback):
    new_feedback_line = f"{name};{email};{feedback}"
    fb_file_path = r"C:\\Users\\user\\study\\python_cc\\web_app\\eng_project\\data\\feedback.csv"
    with open(fb_file_path, "r", encoding="utf-8") as f:
        existing_fbs = [line.strip("\n") for line in f.readlines()]
        title = existing_fbs[0]
        old_terms = existing_fbs[1:]
    fbs_all = old_terms + [new_feedback_line]
    new_fbs = [title] + fbs_all
    with open(fb_file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_fbs))
