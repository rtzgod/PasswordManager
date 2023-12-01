import tkinter as tk
from tkinter import messagebox

class PasswordManager:
    def __init__(self, master):
        self.saved_service = []
        self.saved_password = []
        #change to work with db and change 

        self.master = master
        self.master.title("Password Manager")

        self.label_service = tk.Label(master, text="Service:", bg='#B9B4C7')
        self.label_password = tk.Label(master, text="Password:", bg='#B9B4C7')

        self.entry_service = tk.Entry(master, bg='#FAF0E6')
        self.entry_password = tk.Entry(master, show="*", bg='#FAF0E6')

        self.button_add = tk.Button(master, text="Add Password", command=self.add_password, bg='#5C5470')
        self.button_show_passwords = tk.Button(master, text="Show Passwords", command=self.show_passwords, bg='#5C5470')

        self.label_service.grid(row=0, column=0, sticky=tk.E)
        self.label_password.grid(row=1, column=0, sticky=tk.E)
        self.entry_service.grid(row=0, column=1, padx=10, pady=10)
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)
        self.button_add.grid(row=2, column=1, pady=10)
        self.button_show_passwords.grid(row=3, column=1, padx=10, pady=10)

    def add_password(self):
        service = self.entry_service.get()
        password = self.entry_password.get()

        if service and password:
            messagebox.showinfo("Success", f"Password for {service} added successfully!",)
            self.saved_passwords(service, password)
            # Here you can add code to save the password to a database or another storage.
        else:
            messagebox.showerror("Error", "Service and password are required.")

    def show_passwords(self):
        credentials_window = tk.Toplevel(self.master)
        credentials_window.title("Enter Credentials")
        credentials_window.configure(bg='#352F44')


        label_username = tk.Label(credentials_window, text="Username:", bg='#B9B4C7')
        label_password = tk.Label(credentials_window, text="Password:", bg='#B9B4C7')

        entry_username = tk.Entry(credentials_window, bg='#FAF0E6')
        entry_userpassword = tk.Entry(credentials_window, show="*", bg='#FAF0E6')

        button_check_credentials = tk.Button(
            credentials_window,
            text="Check Credentials",
            command=lambda: self.check_credentials(entry_username.get(), entry_userpassword.get(), credentials_window),
            bg='#5C5470'
        )

        label_username.grid(row=0, column=0, sticky=tk.E)
        label_password.grid(row=1, column=0, sticky=tk.E)
        entry_username.grid(row=0, column=1, padx=10, pady=10)
        entry_userpassword.grid(row=1, column=1, padx=10, pady=10)
        button_check_credentials.grid(row=2, column=1, pady=10)

    def saved_passwords(self, service, password):
          self.saved_service.append(service)
          self.saved_password.append(password)

    def saved_window(self):            
          saved_passwords_window = tk.Toplevel(self.master)
          saved_passwords_window.title("Your passwords")
          saved_passwords_window.configure(bg='#352F44')

          for i in range(len(self.saved_password)):
              label_username_text = tk.Label(saved_passwords_window, text="Username", bg='#B9B4C7')
              label_password_text = tk.Label(saved_passwords_window, text="Password", bg='#B9B4C7')
              label_username = tk.Label(saved_passwords_window, text=self.saved_service[i], bg='#B9B4C7')
              label_password = tk.Label(saved_passwords_window, text=self.saved_password[i], bg='#B9B4C7')
              
              label_username_text.grid(row=0, column=0, sticky=tk.E, padx=10, pady=10)
              label_password_text.grid(row=0, column=1, sticky=tk.E, padx=10, pady=10)
              label_username.grid(row=i+1, column=0, sticky=tk.E, padx=10, pady=10)
              label_password.grid(row=i+1, column=1, sticky=tk.E, padx=10, pady=10)

    def check_credentials(self, username, password, window):
        if self.user_correct(username, password):
            messagebox.showinfo("Access Granted", "Showing passwords!")
            window.destroy() 
            self.saved_window()
            # Add code here to retrieve and display passwords.
        else:
            messagebox.showerror("Access Denied", "Incorrect username or password.")

    def user_correct(self, username, password):
        return username == 'miewkee' and password == '123'

if __name__ == "__main__":
    root = tk.Tk()
    root['bg']='#352F44'
    app = PasswordManager(root)
    root.mainloop()
