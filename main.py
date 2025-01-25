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
            self.root.withdraw()
            task_window = tk.Toplevel()
            app = TaskManager(task_window, self.root)
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects!")

class TaskManager:
    def __init__(self, master, login_window):
        self.master = master
        self.login_window = login_window
        self.master.title("Gestionnaire de Tâches")
        self.master.geometry("800x600")
        
        # Variables
        self.task_var = tk.StringVar()
        
        # Structure de données pour les tâches et leur état
        self.tasks = []  # Liste des tâches
        self.checkboxes = []  # Liste des variables de cases à cocher
        
        # Interface
        self.create_widgets()
        
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
        ttk.Button(input_frame, text="Supprimer sélectionnés", command=self.delete_selected_tasks).pack(side=tk.LEFT, padx=5)
        ttk.Button(input_frame, text="Éditer", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        
        # Frame pour la liste des tâches
        self.tasks_frame = ttk.Frame(self.master)
        self.tasks_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.tasks_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Canvas pour le scrolling
        self.canvas = tk.Canvas(self.tasks_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbar
        self.scrollbar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        
        # Frame pour les tâches dans le canvas
        self.tasks_list_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.tasks_list_frame, anchor='nw')
        
        # Boutons supplémentaires
        button_frame = ttk.Frame(self.master)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Sauvegarder", command=self.save_tasks).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Vider la liste", command=self.clear_tasks).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Déconnexion", command=self.logout).pack(side=tk.RIGHT, padx=5)
        
        # Configuration du scrolling avec la molette de la souris
        self.tasks_list_frame.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1*(event.delta//120), "units")
            
    def add_task(self):
        task = self.task_var.get().strip()
        if task:
            self.tasks.append(task)
            self.update_task_display()
            self.task_var.set("")
            
    def delete_selected_tasks(self):
        # Créer une nouvelle liste sans les tâches sélectionnées
        new_tasks = []
        new_checkboxes = []
        for i, (task, var) in enumerate(zip(self.tasks, self.checkboxes)):
            if not var.get():  # Si la case n'est pas cochée
                new_tasks.append(task)
                new_checkboxes.append(var)
        
        self.tasks = new_tasks
        self.checkboxes = new_checkboxes
        self.update_task_display()
            
    def edit_task(self):
        # Trouver la première tâche sélectionnée
        selected_index = None
        for i, var in enumerate(self.checkboxes):
            if var.get():
                selected_index = i
                break
        
        if selected_index is not None:
            # Créer une fenêtre d'édition
            edit_window = tk.Toplevel(self.master)
            edit_window.title("Éditer la tâche")
            
            edit_var = tk.StringVar(value=self.tasks[selected_index])
            ttk.Entry(edit_window, textvariable=edit_var, width=40).pack(padx=5, pady=5)
            
            def save_edit():
                self.tasks[selected_index] = edit_var.get()
                self.update_task_display()
                edit_window.destroy()
                
            ttk.Button(edit_window, text="Sauvegarder", command=save_edit).pack(pady=5)
        else:
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
            self.checkboxes.clear()
            self.update_task_display()
            
    def update_task_display(self):
        # Nettoyer le frame existant
        for widget in self.tasks_list_frame.winfo_children():
            widget.destroy()
        
        # Réinitialiser les checkboxes
        self.checkboxes = []
        
        # Ajouter les tâches avec leurs cases à cocher
        for i, task in enumerate(self.tasks):
            frame = ttk.Frame(self.tasks_list_frame)
            frame.pack(fill=tk.X, padx=5, pady=2)
            
            var = tk.BooleanVar()
            self.checkboxes.append(var)
            
            checkbox = ttk.Checkbutton(frame, variable=var)
            checkbox.pack(side=tk.LEFT)
            
            label = ttk.Label(frame, text=f"{i+1}. {task}")
            label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Mettre à jour la zone scrollable
        self.tasks_list_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            
    def logout(self):
        self.master.destroy()
        self.login_window.deiconify()

if __name__ == "__main__":
    root = tk.Tk()
    login = LoginWindow(root)
    root.mainloop()