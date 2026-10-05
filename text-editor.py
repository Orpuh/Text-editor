import tkinter as tk
from turtle import title
import customtkinter
import os
from tkinter import filedialog, messagebox


customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("1000x700")
root.configure(fg_color="#020b08")
root.title("Text Editor")

top_bar = tk.Frame(root, bg="#1f1f1f", height=22)
top_bar.pack(side="top", fill="x")
top_bar.pack_propagate(False)

content_frame = customtkinter.CTkFrame(root, fg_color="transparent")
content_frame.pack(expand=True, fill="both", padx=10, pady=10)

right_panel = customtkinter.CTkFrame(
    content_frame, width=350, fg_color="transparent")

right_panel.pack(side="right", fill="y")
right_panel.pack_propagate(False)

customtkinter.FontManager.load_font(r"D:\FONTS\ModernDOS8x8.ttf")

font = customtkinter.CTkFont(family="Modern DOS 8x8", size=30)

editor_frame = customtkinter.CTkFrame(content_frame, fg_color="transparent")
editor_frame.pack(side="left", expand=True, fill="both")

documents = {}
tab_buttons = {}
tab_frames = {}
close_buttons = {}
tab_number = 0
active_tab = None

def select_tab(tab_title):
    global active_tab

    if tab_title not in documents:
        return
    
    active_tab = tab_title

    for name, document in documents.items():
         document ["textbox"].pack_forget()

         color = "#3a3a3a" if name == tab_title else "#1f1f1f"
         tab_frames[name].configure(bg=color)
         tab_buttons[name].configure(bg=color, activebackground=color)
         close_buttons[name].configure(bg=color, activebackground="#505050")
         
         documents[tab_title]["textbox"].pack(expand=True, fill="both")

def new_tab(title=None, content="", file_path=None):
    global tab_number
    tab_number += 1

    base_title = title or  f"untitled {tab_number}"
    tab_title = base_title
    suffix = 2

    while tab_title in documents:
        tab_title = f"{base_title} ({suffix})"
        suffix += 1

    textbox = customtkinter.CTkTextbox(
        editor_frame,
        fg_color="#020b08",
        text_color="#00ff99",
        border_color="#00ff99",
        corner_radius=0,
        font=font,
        activate_scrollbars=True,
    )
    textbox.insert("1.0", content)

    documents[tab_title] =  {"textbox": textbox, "path": file_path}

    tab_frame = tk.Frame(top_bar, bg="#3a3a3a")
    tab_frame.pack(side="left", fill="y", padx=(2,0))
    tab_frames[tab_title] = tab_frame

    tab_button = tk.Button(
        tab_frame,
        text=tab_title,
        command=lambda title=tab_title: select_tab(title),
        bg = "#3a3a3a",
        fg = "white",
        activebackground="#505050",
        activeforeground="white",
        relief="flat",
        borderwidth=0,
        padx=12,
    )
    tab_button.pack(side="left", fill="y")
    tab_buttons[tab_title] = tab_button

    close_button = tk.Button(
        tab_frame,
        text="x",
        command=lambda title=tab_title: close_tab(title),
        bg="#3a3a3a",
        fg="white",
        activebackground="#505050",
        activeforeground="white",
        relief="flat",
        borderwidth=0,
        padx=7,
    )
    close_button.pack(side="left", fill="y")
    close_buttons[tab_title] = close_button

    select_tab(tab_title)

def close_tab(tab_title):
    global active_tab

    if tab_title not in documents:
        return

    tab_names = list(documents)
    closed_index = tab_names.index(tab_title)

    documents[tab_title]["textbox"].destroy()
    tab_frames[tab_title].destroy()

    del documents [tab_title]
    del tab_frames [tab_title]
    del tab_buttons [tab_title]
    del close_buttons [tab_title]

    remaining_tabs = list(documents)

    if remaining_tabs:
        next_index = min(closed_index, len(remaining_tabs) - 1)
        select_tab(remaining_tabs[next_index])
    else:
        active_tab =None


def open_file():
        path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All files",  "*.*")]
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()
            new_tab(os.path.basename(path), content, path)
        except OSError as error:
            messagebox.showerror("open file error", str(error))

def save_file(save_as=False):
    if active_tab is None:
        return

    document = documents[active_tab]
    path = document["path"]

    if save_as or not path:
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All files",  "*.*")],
        )
        if not path:
            return
        document["path"] = path

    try:
        text = document["textbox"].get("1.0", "end-1c")
        with open(path, "w", encoding="utf-8") as file:
            file.write(text)
    except OSError as error:
        messagebox.showerror("save file error", str(error))

menu_bar = tk.Menu(
    root,
    tearoff=False,
    bg="#333333",
    fg="grey",
    activebackground="#505050",
    activeforeground="white",
    borderwidth=0,
)

file_menu = tk.Menu(
     menu_bar,
     tearoff=False,
     bg="#333333",
     fg="grey",
     activebackground="#505050",
     activeforeground="blue",
)     


file_menu.add_command(label= "New Tab", command=new_tab, accelerator="Ctrl+N")
file_menu.add_command(label="Open File", command=open_file, accelerator="Ctrl+O")
file_menu.add_separator()
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_command(
        label="Save As", command=lambda: save_file(save_as=True)
)

def show_file_menu():
     file_menu.tk_popup(
          file_button.winfo_rootx(),
            file_button.winfo_rooty() + file_button.winfo_height(),
     )

file_button = tk.Button(
    top_bar,
    text="File",
    command=show_file_menu,
    bg="#1f1f1f",
    fg="white",
    activebackground="#505050",
    activeforeground="white",
    relief="flat",
    borderwidth=0,
    padx=20,
)
file_button.pack(side="left", fill="y")

plus_button = tk.Button(
    top_bar,
    text="+",
    command=new_tab,
    bg="#1f1f1f",
    fg="white",
    activebackground="#505050",
    activeforeground="white",
    relief="flat",
    borderwidth=0,
    padx=12,
)
plus_button.pack(side="left", fill="y")




root.bind("<Control-n>", lambda event: new_tab())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save_file())

new_tab()

                            

ascii_eyes = r"""
          _..~~*****~~.._
        _~",&*.`.`.*.`.`.y"~_
      .y ,;``.` `.`._..~%;*.``.
    .'; q`       .;%%b`*`.`.`.``.
   /) '         .*`  y   `..&%#$y\
  /  _~****~_     .~*    ;$'.`=*.*L
 . ,*    .._ *,        ;`    `.`.`'.
 '/     (   `. \         _  `.`.`*='
y/   ..  `.   ; L    _,;;" ,~~.._..&L
d  .####.  )  ;  b ~*"`     .==y**'`:
|  ###### (   y  |       .~`  ('`.,*:
q  ######  `='   |             )`/`.y
 . '####'  .=.   *            '`.`..
 '   ``    ; y  y     ;._   `.`.`.&'
  \ .=.  .' .` /       `*;.    .`./
   \`~`  `"`_.*    (      `*~.~.~/
    `.~....~   .  \ )   `.`.`.`;`
      `.  .    `.  Y `.`.~..*.`
        `~.\`.`~.)`.`~._`..~`
            ``~~.L...~~``

            








           _..~~*****~~.._
        _~"  ~.   .~``.~~.*~_
      .`_`.`.   .`   (.~~.)  *.
    .&p**`*~.  /       _..._   *.
   /=~.`      d .**. ,######b    \
  /`.`.`      | d  F #########    b
 .`.)`        q q  L `########    |.
 '`/           \ q  `.`q####p     p'
d`(.~**~        \ :   ) ````     /  b
:)F`.            `.`~`   (`*)  .*  ~:
:&`..&;'           `.._   ``_.*    `:
q&`d;'      /          `````      7 p
 .,p`.`. _.`                  ._`(~.
 'F`.`_~**"`                   `*~)'
  \`dy`.`.`    ,*      (      .`.`/
   \q`.`.`.`.`/    (   ,) `.`.L`./
    `.==&"`.`(`_.'`.`. F`.`/`.))`
      `.~=_  _)&p`.`..)'_.*`..`
        `~%&&*`.`_,,&p=*`_.~`
            ``~~q%F..~~``

            







            
           _..~~*****~~.._
        _~"_~*  _..._ `*~_"~_
      .` .`  .#########.  `. `.
    .`  /   .###########.   \  `.
   /~* d    :###########: .. b  ,\
  /`.  |  _ '###########'(  )|    \
 . %   q ( `.`#########'  `` p   `=.
 '`.`   \ `. `.`"***"`_.~.  /    .`'
d`.*     `. `~'   (```_.' .`      \`b
:F`._,     `~_     ``` _~*    *. `.i:
:`.%*   /     ``*****``         L`.i:
q`&`.  (                        (`.`p
 i`.`.` ,            (      _  `.)`.
 '`.`.`d    y         )     *b`.`.`'
  \`y`.q.`."     ,       . `.`L`.`/
   \i`.`\(`.`.` y`.`.;`.` b`.`%`./
    `L`.`qb`.`.`*`.`.)`.. *`.,&.`
      `.`.`*=._`.L`.(=*`.`&`.y`
        `~._ *;L..`Jp`.`.y.~`
            `*~~*q;;.~~*`    
"""            

watermark = customtkinter.CTkLabel(
    right_panel,
    text=ascii_eyes,
    font=customtkinter.CTkFont(family="Modern DOS 8x8", size=15),
    text_color="#dae2e1",
    fg_color="transparent",
    justify="left",
    anchor="nw",
)   

watermark.pack(anchor="ne", padx=10, pady=70)
watermark.bind(
    "<Button-1>",
    lambda _event: documents[active_tab]["textbox"].focus_set()
    if active_tab else None
)


                
                    

root.mainloop()

