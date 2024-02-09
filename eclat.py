import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from efficient_apriori import apriori
import matplotlib.pyplot as plt
import threading

class EclatGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("ECLAT Frequent Item Set Mining")
        self.rules = None
        
        self.create_widgets()
    
    def create_widgets(self):
        self.file_label = tk.Label(self.master, text="Select Dataset:")
        self.file_label.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        
        self.file_entry = tk.Entry(self.master, width=50, state='disabled')
        self.file_entry.grid(row=0, column=1, columnspan=2, padx=10, pady=5)
        
        self.browse_button = tk.Button(self.master, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=3, padx=5, pady=5)
        
        self.min_support_label = tk.Label(self.master, text="Minimum Support:")
        self.min_support_label.grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        
        self.min_support_entry = tk.Entry(self.master, width=10)
        self.min_support_entry.grid(row=1, column=1, padx=10, pady=5)
        
        self.run_button = tk.Button(self.master, text="Run ECLAT", command=self.run_eclat)
        self.run_button.grid(row=1, column=2, padx=5, pady=5)
        
        self.export_button = tk.Button(self.master, text="Export Rules", state='disabled', command=self.export_rules)
        self.export_button.grid(row=1, column=3, padx=5, pady=5)
        
        self.result_text = tk.Text(self.master, height=20, width=60, state='disabled')
        self.result_text.grid(row=2, column=0, columnspan=4, padx=10, pady=5)
        
        self.plot_button = tk.Button(self.master, text="Plot Support vs. Itemsets", state='disabled', command=self.plot_support)
        self.plot_button.grid(row=3, column=0, columnspan=4, padx=10, pady=5)
    
    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if filename:
            self.file_entry.config(state='normal')
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(tk.END, filename)
            self.file_entry.config(state='disabled')
    
    def run_eclat(self):
        def run():
            try:
                min_support_str = self.min_support_entry.get()
                min_support = float(min_support_str)
                if min_support <= 0 or min_support >= 1:
                    raise ValueError("Minimum support must be between 0 and 1")
                
                dataset = pd.read_csv(self.file_entry.get())
                _, self.rules = apriori(dataset.values.tolist(), min_support=min_support)
                
                self.result_text.config(state='normal')
                self.result_text.delete('1.0', tk.END)
                self.result_text.insert(tk.END, "Frequent Itemsets:\n")
                self.result_text.insert(tk.END, str(_))
                self.result_text.config(state='disabled')
                self.export_button.config(state='normal')
                self.plot_button.config(state='normal')
            except ValueError as ve:
                messagebox.showerror("Error", str(ve))
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        threading.Thread(target=run).start()
    
    def export_rules(self):
        try:
            if self.rules is not None and len(self.rules) > 0:
                rules_list = [(list(rule.lhs), list(rule.rhs), rule.support, rule.confidence) for rule in self.rules]
                rules_df = pd.DataFrame(rules_list, columns=['Left Hand Side', 'Right Hand Side', 'Support', 'Confidence'])
                filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
                if filename:
                    rules_df.to_csv(filename, index=False)
                    messagebox.showinfo("Export Successful", "Association rules exported successfully.")
            else:
                messagebox.showwarning("No Rules", "No association rules found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def plot_support(self):
        try:
            if self.rules is not None and len(self.rules) > 0:
                supports = [rule.support for rule in self.rules]
                itemsets = [f"{rule.lhs} -> {rule.rhs}" for rule in self.rules]
                plt.barh(itemsets, supports)
                plt.xlabel('Support')
                plt.ylabel('Itemsets')
                plt.title('Support vs. Itemsets')
                plt.show()
            else:
                messagebox.showwarning("No Rules", "No association rules found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = EclatGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
