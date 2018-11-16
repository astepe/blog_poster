from ttkthemes import themed_tk as tk
from blog_poster.views import Login
import argparse
import os


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--debug', action='store_true')
    args = parser.parse_args()

    if args.debug:
        os.environ['API_URL'] = 'http://127.0.0.1:5000/api'
        print('debug: on')
    else:
        os.environ['API_URL'] = 'https://ari-blog.herokuapp.com/api'

    login_master = tk.ThemedTk()
    login_master.get_themes()
    login_master.set_theme("radiance")
    login = Login(login_master)

    login_master.mainloop()
