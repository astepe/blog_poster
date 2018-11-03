from tkinter import *
from tkinter import filedialog, ttk
from ttkthemes import themed_tk as tk
from blog_poster.controller import Api
from datetime import datetime
import os, time
from blog_poster.html_previewer import PreviewWindow

BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Login:
    """
    login window
    """

    def __init__(self, master):

        self.master = master
        self.master.title('Login')

        self.frame = ttk.Frame(self.master)

        self.logo = PhotoImage(file=BASEDIR + "/blogposterlogo.png")
        ttk.Label(self.frame, image=self.logo).pack()
        self.username_label = ttk.Label(self.frame, text='Username', font='Courier 15', padding=3)
        self.username_field = ttk.Entry(self.frame, font="Courier")
        self.password_label = ttk.Label(self.frame, text='Password', font='Courier 15', padding=3)
        self.password_field = ttk.Entry(self.frame, font="Courier", show='*')

        self.login_button = ttk.Button(self.frame, text='Login', width=25, command=self.login)

        self.username_label.pack()
        self.username_field.pack()
        self.password_label.pack()
        self.password_field.pack()
        self.login_button.pack()
        self.frame.pack()

    def login(self):

        username = self.username_field.get()
        password = self.password_field.get()

        api = Api(username, password)

        if api.token is None:

            self.username_field.delete(0, END)
            self.password_field.delete(0, END)
            return None

        self.master.destroy()
        ListPosts(api)



class ListPosts:
    """
    lists blogposts to edit/delete
    """

    def __init__(self, api):

        self.api = api
        self.master = tk.ThemedTk()
        self.master.get_themes()
        self.master.set_theme("radiance")
        self.master.title('Blog Posts')

        # set frame that holds image and create button
        self.image_frame = ttk.Frame(self.master)
        self.logo = PhotoImage(file=BASEDIR + "/blogposterlogo.png")
        ttk.Label(self.image_frame, image=self.logo, padding=15).pack(side='top')
        _create = lambda: Edit(self, self.api)
        ttk.Button(self.image_frame, text='Create', command=_create).pack(side='bottom')
        self.image_frame.pack(side='left')

        self.show_posts()

    def show_posts(self):

        self.post_frame = ttk.Frame(self.master)

        # api call to retrieve blog posts
        self.blogposts = self.api.get_blogposts()

        for blogpost in self.blogposts:

            _edit = lambda blogpost=blogpost: Edit(parent=self, api=self.api, blogpost=blogpost)
            _delete = lambda id=blogpost['id']: self.confirm_delete(id)
            _frame = ttk.Frame(self.post_frame)

            ttk.Label(_frame, text=blogpost["title"], font='Courier 15 bold', padding=10).pack(side="left")
            ttk.Button(_frame, text='Edit', command=_edit).pack(side="right")
            ttk.Button(_frame, text='Delete', command=_delete).pack(side="right")

            _frame.pack(side='top')

        self.post_frame.pack(side='right')

    def confirm_delete(self, id):

        delete_master = Toplevel(self.master)
        delete_master.title('Confirm Delete')
        delete_frame = ttk.Frame(delete_master)

        def delete():

            self.api.delete_blogpost(id)
            delete_master.destroy()
            self.post_frame.destroy()
            self.show_posts()

        for dict in self.blogposts:
            if dict['id'] == id:
                blogpost = dict

        Message(delete_frame, relief=RAISED, width=200,
                text='Are you sure that you want to delete this blog post?', font='Courier').pack()
        ttk.Label(delete_frame, text=f'Title: {blogpost["title"]} \nDate: {blogpost["date"]}').pack()
        ttk.Button(delete_frame, text='Delete Post', command=delete).pack()

        delete_frame.pack()


class Edit:
    """
    Text editor for creating and editing blog posts
    """

    def __init__(self, parent, api, **kwargs):

        self.parent = parent
        self.api = api

        # set themes for window
        self.master = tk.ThemedTk()
        self.master.get_themes()
        self.master.set_theme("radiance")
        self.master.title('Editor')

        # create form fields
        self.title_frame = ttk.Frame(self.master)
        self.title_label = ttk.Label(self.title_frame, text='Title:', font='Courier')
        self.title_field = ttk.Entry(self.title_frame, font="Courier")
        self.body_frame = ttk.Frame(self.master)
        self.body_label = ttk.Label(self.body_frame, text='Body:', font='Courier')
        self.body_field = Text(self.body_frame)
        self.pic_frame = ttk.Frame(self.master)
        self.pic_label = ttk.Label(self.pic_frame, text='Image:', font='Courier')
        self.pic_field = ttk.Entry(self.pic_frame, font="Courier")


        # if editing a pre-existing post, populate text into fields
        if 'blogpost' in kwargs:

            self.blogpost = kwargs['blogpost']
            self.html_preview = PreviewWindow(self.blogpost['body'])
            self.title_field.insert(0, self.blogpost['title'])
            self.body_field.insert(END, self.blogpost['body'])
            self.pic_field.insert(0, (self.blogpost['image']))
        else:
            self.html_preview = PreviewWindow()

        def onclick(event):
            event.widget.focus_set()

        def keyrelease(event):
            text = event.widget.get(1.0, END)
            self.html_preview.update_preview(text)

        self.body_field.bind("<KeyRelease>", keyrelease)
        self.body_field.bind('<Button-1>', onclick)

        # create buttons
        self.button_frame = ttk.Frame(self.master)
        self.post_button = ttk.Button(self.button_frame, text='Post',
                                      command=self.send_blogpost)

        self.cancel_button = ttk.Button(self.button_frame, text='Cancel',
                                        command=self.master.destroy)

        self.pic_button = ttk.Button(self.pic_frame, text='Import Image',
                                 command=self.open_image)

        # pack all elements into frame
        self.title_label.pack(side='left', ipadx=5, ipady=8)
        self.title_field.pack(side='left')
        self.title_frame.pack()
        self.pic_label.pack(side='left', ipadx=5, ipady=8)
        self.pic_field.pack(side='left')
        self.pic_button.pack()
        self.pic_frame.pack()
        self.body_label.pack()
        self.body_field.pack()
        self.body_frame.pack()
        self.post_button.pack(side='left')
        self.cancel_button.pack(side='right')
        self.button_frame.pack(side='bottom')

    def send_blogpost(self):

        title = self.title_field.get()
        body = self.body_field.get(1.0, END)
        image = self.pic_field.get()

        try:
            id = self.blogpost['id']
            self.api.update_blogpost(id, title=title, body=body, image=image)
        except:
            self.api.create_blogpost(title=title, body=body, image=image)

        self.reset_parent()

    def reset_parent(self):

        self.master.destroy()
        self.parent.post_frame.destroy()
        self.parent.show_posts()

    def open_image(self):

        filename = filedialog.askopenfilename(initialdir="~/Desktop",
                                              title="Select Image",
                                              filetypes=(("jpg files", "*.jpg"),
                                                         ("png files", "*.png*"),
                                                         ("jpeg files", "*.jpeg"),
                                                         ("gif files", "*.gif")))
        self.pic_field.delete(0, END)
        self.pic_field.insert(0, filename)
        self.master.lift()
