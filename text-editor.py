import tkinter as tk
import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("1000x700")
root.configure(fg_color="#020b08")
root.title("Text Editor")

customtkinter.FontManager.load_font("D:\FONTS\ModernDOS8x8.ttf")

font = customtkinter.CTkFont(family="Modern DOS 8x8", size=30)

text_edit = customtkinter.CTkTextbox(
    root,
    fg_color="#020b08",
    text_color="#00ff99",
    border_color="#00ff99",
    corner_radius=0,
    font=font,
    activate_scrollbars=True,
)
text_edit.pack(expand=True, fill="both", padx=10, pady=10)



root.mainloop()




