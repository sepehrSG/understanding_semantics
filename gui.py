import tkinter as tk
from tkinter import messagebox
from utils import compare_semantics

def analyze(LLM, GT):
    """ Perform semantic analysis on press of Analyze button
    """
    llm_text = LLM.get("1.0", tk.END)
    gt_text = GT.get("1.0", tk.END)
    if llm_text and gt_text:
        result = compare_semantics(llm_text, gt_text)
        display_result(result)
        
    else:
        messagebox.showwarning("Input Error", "Please enter some text.")

def display_result(result):
    """ Displays result of semantic analysis
    """
    text_widget.config(state=tk.NORMAL)
    text_widget.delete("1.0", tk.END)
    result_list = result.split('\n')
    for res in result_list:
        r = res.split(' ')
        text_widget.insert(tk.END, ' '.join(r[:-1]) + " ")
        text_widget.insert(tk.END, r[-1] + "\n", r[-1])

    text_widget.config(state=tk.DISABLED)

# Set up layout of application
root = tk.Tk()
root.title("Understand Semantics")

tk.Label(root, text="LLM Output:").pack(pady=5)
LLM_text = tk.Text(root, wrap='word', height=5, width=60)
LLM_text.pack()

tk.Label(root, text="Ground Truth:").pack(pady=5)
GT_text = tk.Text(root, wrap='word', height=5, width=60)
GT_text.pack()

tk.Button(root, text="Analyze", command=lambda: analyze(LLM_text, GT_text)).pack(pady=10)

text_widget = tk.Text(root, wrap='word', height=20, width=80)
text_widget.pack()

# color code evals
text_widget.tag_configure("Contradicting", foreground='red')
text_widget.tag_configure("Consistent", foreground='green')
text_widget.tag_configure("Neutral", foreground='orange')

text_widget.config(state=tk.DISABLED)

root.mainloop()