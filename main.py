import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Connexion")
        self.root.geometry("300x200")
        
        # Variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        
        # Interface
        tk.Label(root, text="Nom d'utilisateur:").pack(pady=10)
        tk.Entry(root, textvariable=self.username_var).pack()
        
        tk.Label(root, text="Mot de passe:").pack(pady=10)
        tk.Entry(root, textvariable=self.password_var, show="*").pack()
        
        tk.Button(root, text="Se connecter", command=self.login).pack(pady=20)
        
    def login(self):
        if self.username_var.get() == "admin" and self.password_var.get() == "admin":
            self.root.withdraw()  # Cache la fenêtre de connexion
            task_window = tk.Toplevel()
            app = TaskManager(task_window, self.root)
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects!")

class TaskManager:
    def __init__(self, master, login_window):
        self.master = master
        self.login_window = login_window
        self.master.title("Gestionnaire de Tâches")
        self.master.geometry("500x600")
        
        # Variables
        self.task_var = tk.StringVar()
        
        # Interface
        self.create_widgets()
        
        # Liste pour stocker les tâches
        self.tasks = []
        
        # Charger les tâches existantes
        self.load_tasks()
        
    def create_widgets(self):
        # Frame pour l'entrée et les boutons
        input_frame = ttk.Frame(self.master)
        input_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Entrée de tâche
        self.task_entry = ttk.Entry(input_frame, textvariable=self.task_var, width=40)
        self.task_entry.pack(side=tk.LEFT, padx=5)
        
        # Boutons
        ttk.Button(input_frame, text="Ajouter", command=self.add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Supprimer", command=self.delete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Éditer", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        
        # Zone de texte pour les tâches
        self.task_area = ScrolledText(self.master, width=50, height=20)
        self.task_area.pack(padx=5, pady=5)
        
        # Boutons supplémentaires
        button_frame = ttk.Frame(self.master)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Sauvegarder", command=self.save_tasks).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Vider la liste", command=self.clear_tasks).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Déconnexion", command=self.logout).pack(side=tk.RIGHT, padx=5)
        
    def add_task(self):
        task = self.task_var.get().strip()
        if task:
            self.tasks.append(task)
            self.update_task_display()
            self.task_var.set("")  # Vider l'entrée
            
    def delete_task(self):
        try:
            # Obtenir la ligne sélectionnée
            selected = self.task_area.get("sel.first", "sel.last")
            start_idx = self.task_area.index("sel.first").split('.')[0]
            self.tasks.pop(int(start_idx) - 1)
            self.update_task_display()
        except tk.TclError:
            messagebox.showwarning("Attention", "Veuillez sélectionner une tâche à supprimer.")
            
    def edit_task(self):
        try:
            selected = self.task_area.get("sel.first", "sel.last")
            start_idx = self.task_area.index("sel.first").split('.')[0]
            task_idx = int(start_idx) - 1
            
            # Créer une fenêtre d'édition
            edit_window = tk.Toplevel(self.master)
            edit_window.title("Éditer la tâche")
            
            edit_var = tk.StringVar(value=self.tasks[task_idx])
            ttk.Entry(edit_window, textvariable=edit_var, width=40).pack(padx=5, pady=5)
            
            def save_edit():
                self.tasks[task_idx] = edit_var.get()
                self.update_task_display()
                edit_window.destroy()
                
            ttk.Button(edit_window, text="Sauvegarder", command=save_edit).pack(pady=5)
            
        except tk.TclError:
            messagebox.showwarning("Attention", "Veuillez sélectionner une tâche à éditer.")
            
    def save_tasks(self):
        with open("tasks.txt", "w", encoding="utf-8") as file:
            for task in self.tasks:
                file.write(task + "\n")
        messagebox.showinfo("Succès", "Tâches sauvegardées avec succès!")
        
    def load_tasks(self):
        try:
            with open("tasks.txt", "r", encoding="utf-8") as file:
                self.tasks = [line.strip() for line in file.readlines()]
            self.update_task_display()
        except FileNotFoundError:
            pass
            
    def clear_tasks(self):
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment vider la liste?"):
            self.tasks.clear()
            self.update_task_display()
            
    def update_task_display(self):
        self.task_area.delete(1.0, tk.END)
        for i, task in enumerate(self.tasks, 1):
            self.task_area.insert(tk.END, f"{i}. {task}\n")
            
    def logout(self):
        self.master.destroy()
        self.login_window.deiconify()  # Réaffiche la fenêtre de connexion

if __name__ == "__main__":
    root = tk.Tk()
    login = LoginWindow(root)
    root.mainloop()