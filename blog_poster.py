from tkinter import ttk
from ttkthemes import themed_tk as tk
from blog_poster.views import Login

login_master = tk.ThemedTk()
login_master.get_themes()
login_master.set_theme("radiance")
login = Login(login_master)

if __name__ == '__main__':
    login_master.mainloop()
