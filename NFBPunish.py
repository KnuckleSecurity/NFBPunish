from tkinter import *
import tkinter.font as tkFont
from tkinter import messagebox
import webbrowser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from time import sleep
import os


class InstagramBot:
        def __init__(self, userName, password):
                self.userName=userName
                self.password=password
                try:
                    if os.name=='posix':
                        s=Service('./geckodriver')
                        self.driver=webdriver.Firefox(service=s)
                    if os.name=='nt':
                        s=Service(".\geckodriver.exe")
                        self.driver=webdriver.Firefox(service=s)
                except:
                    os._exit(-1)

        def login(self):
                self.driver.get('https://www.instagram.com/?hl=en')
                sleep(2)
                if self.driver.find_element(By.XPATH,"/html/body/div[4]/div/div/button[1]"):
                    self.driver.find_element(By.XPATH,"/html/body/div[4]/div/div/button[1]").click()
                    sleep(2)
                usernameBox=self.driver.find_element(By.NAME,'username')
                usernameBox.send_keys(self.userName)
                passwordBox=self.driver.find_element(By.NAME,'password')
                passwordBox.send_keys(self.password)
                sleep(0.2)
                loginBtn=self.driver.find_element(By.XPATH,'/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div/div[3]/button/div')
                loginBtn.click()
                sleep(6)
                self.driver.get(f'https://www.instagram.com/{self.userName}/?hl=en')
                
        def scroll_down(self,mode="none"):
                sleep(2)
                js_code=("""
                        scrollBox=document.querySelector('.isgrP');
                        scrollBox.scrollTo(0,scrollBox.scrollHeight);
                        page_end=scrollBox.scrollHeight;
                        return page_end;
                """)
                page_end=self.driver.execute_script(js_code)
                while True:
                        end = page_end
                        sleep(2)
                        page_end=self.driver.execute_script(js_code)
                        if end == page_end:
                            break
                if mode == "none":
                    return
                elif mode == "get_names":
                        elements=self.driver.find_elements(By.CSS_SELECTOR,'.FPmhX.notranslate._0imsa')
                        return elements

        def get_followers(self):
                messagebox.showinfo(title="Info",message="Process will start...\n\nDo not interact neither with the browser nor with the application until you see all the users that follows you in the 'Followers' box.\n\nClick 'OK' to proceed.")
                sleep(2)
                followersBtn=self.driver.find_element(By.XPATH,'/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span')
                followersBtn.click()
                self.follower_elements=self.scroll_down("get_names")
                self.follower_names=[name.text for name in self.follower_elements if name.text != '']
                self.driver.find_element(By.XPATH,"/html/body/div[6]/div/div/div[1]/div/div[2]/button").click()
                messagebox.showinfo(title="Done !",message="Follower usernames successfully retrieved.\n\nClick 'OK' to proceed.")
                return self.follower_names

        def get_following(self):
                messagebox.showinfo(title="Info",message="Process will start...\n\nDo not interact neither with the browser nor with the application until you see all the users that you follow listed in the 'Followings' box.\n\nClick 'OK' to proceed.")
                sleep(2)
                followingBtn=self.driver.find_element(By.XPATH,'/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span')
                followingBtn.click()
                self.following_elements=self.scroll_down("get_names")
                self.following_names=[name.text for name in self.following_elements if name.text != '']
                self.driver.find_element(By.XPATH,"/html/body/div[6]/div/div/div[1]/div/div[2]/button").click() #Close
                messagebox.showinfo(title="Done !",message="Following usernames successfully retrieved.\n\nClick 'OK' to proceed.")
                return self.following_names

        def find_not_following_back(self):
                not_following_back=[user for user in self.following_names if user not in self.follower_names]
                return not_following_back
        def unfollow(self,unfollow_list):
                followingBtn=self.driver.find_element(By.XPATH,'/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span')
                followingBtn.click()
                self.scroll_down()
                unfollow_buttons=self.driver.find_elements_by_xpath("//button[@class='sqdOP  L3NKy    _8A5w5    ']")
                for unfollow in unfollow_list:
                    unfollow_buttons[self.following_names.index(str(unfollow))].click()
                    sleep(0.5)
                    self.driver.find_element(By.XPATH,'/html/body/div[7]/div/div/div/div[3]/button[1]').click()
                    sleep(30)
                self.driver.find_element(By.XPATH,"/html/body/div[6]/div/div/div[1]/div/div[2]/button").click()

def login():
        if len(entry_username.get())==0 or len(entry_password.get())==0:
                messagebox.showerror(title="Error",message="'Username' and 'Password' fields are empty.")
                return
        global browser
        messagebox.showinfo(title="Info",message="Logging in...\n\nDo not interact neither with the browser nor with the application until the browser at the account's profile page.\n\nClick 'OK' to proceed.")
        browser=InstagramBot(entry_username.get(),entry_password.get())
        browser.login()

def get_followers():
        try:
                followers=browser.get_followers()
                followers_c.set(str(len(followers)))
                for user in followers:
                        listbox_followers.insert(END,user)
        except:
                messagebox.showerror(title="Error",message="In order to dump a follower users list, you need to login and summon a web browserfirst.\nOr you have 0 followers.")

def get_followings():
        try:
                followings=browser.get_following()
                following_c.set(str(len(followings)))
                for user in followings:
                        listbox_following.insert(END,user)
        except:
                messagebox.showerror(title="Error",message="In order to dump a following users list, you need to login and summon a web browserfirst.\nOr you are following 0 accounts.")

def get_not_following_back():
        try:
                not_following_back=browser.find_not_following_back()
                nfb_c.set(str(len(not_following_back)))
                for user in not_following_back:
                        listbox_not_following_back.insert(END,user)
        except:
                messagebox.showerror(title="Error",message="In order to comb out the users that are not following you back, you need to dump a following and followers a list.")
def clear_boxes():
        listbox_followers.delete(0,END)
        listbox_following.delete(0,END)
        listbox_not_following_back.delete(0,END)
        listbox_unfollow.delete(0,END)
        followers_c.set("0")
        following_c.set("0")
        nfb_c.set("0")
        unf_c.set("0")
def select_lb(lb):
        lb.select_set(0,END)

def add_to_unf(lb):
        unf_list=[lb.get(user) for user in lb.curselection()]
        for user in unf_list:
                if user not in listbox_unfollow.get(0,END):
                        listbox_unfollow.insert(END,user)
        unf_c.set(str(len(listbox_unfollow.get(0,END))))
def remove_box(lb):
        for user in lb.curselection()[::-1]:
                lb.delete(user)
        unf_c.set(str(len(lb.get(0,END))))
def unfollow(lb):
        try:
                lb.select_set(0,END)
                unf_list=[lb.get(user) for user in lb.curselection()]
                time_calculated=30*len(unf_list)
                messagebox.showinfo(title="Info",message=f"Starting unfollow process...\n\nDo not interact neither with the browser nor with the application until the program finishes to unfollow all the users that you selected.\n\nDue to Instagram's policies and regulations to prevent bots, each user must be unfollowed with an interval of 30 seconds to bypass bot detection.\n\nWith the total of {len(unf_list)} users selected,\nall unfollowing process will take approximately {time_calculated} seconds.\n\nClick 'OK' to proceed.")
                browser.unfollow(unf_list)
        except:
                messagebox.showerror(title="Error",message="In order to start unfollowing process, you have to login, to dump profiles.")
def redirect_website(url):
        webbrowser.open(url)


root=Tk()
root.geometry("865x650")
root.resizable(0, 0)
root.configure(bg='black')
icon= PhotoImage(file = "misc/icon.png")
root.iconphoto(False, icon)
root.title("NFBPunish v1.0 - Powered by Burak Baris")

fontStyle = tkFont.Font(size=13,family='Serif')
fontStyle2 = tkFont.Font(size=17,family='Courier',weight='bold')
fontStyle3 = tkFont.Font(size=14,family='Courier',weight='bold')

label_username=Label(root,text="Username",font=fontStyle3,bg="black",fg="white")
label_password=Label(root,text="Password",font=fontStyle3,bg="black",fg="white")
label_username.place(x=15,y=185)
label_password.place(x=15,y=225)

button_login=Button(root,text="Login",font=fontStyle,command=login,width=20,bg="black",fg="white",activebackground="green")
button_login.place(x=15,y=275)

entry_username=Entry(root,bg="black",fg="white",insertbackground='white',width=17)
entry_password=Entry(root,bg="black",fg="white",insertbackground='white',show="*",width=17)
entry_password.place(x=110,y=228)
entry_username.place(x=110,y=188)

button_get_followers=Button(root,text="Dump followers",font=fontStyle,width=20,command=get_followers,bg="black",fg="white",activebackground="green")
button_get_followings=Button(root,text="Dump followings",font=fontStyle,width=20,command=get_followings,bg="black",fg="white",activebackground="green")
button_not_following_back=Button(root,text="Extract non-followers",font=fontStyle,width=20,command=get_not_following_back,bg="black",fg="white",activebackground="green")
button_get_followers.place(x=15,y=325)
button_get_followings.place(x=15,y=375)
button_not_following_back.place(x=15,y=430)

listbox_followers=Listbox(root,width=17,height=30,bg="black",fg="white")
listbox_following=Listbox(root,width=17,height=30,selectmode="multiple",bg="black",fg="white")
listbox_not_following_back=Listbox(root,width=17,height=30,selectmode="multiple",bg="black",fg="white")
listbox_unfollow=Listbox(root,width=17,height=30,selectmode="multiple",bg="black",fg="white")
listbox_followers.place(x=270,y=35)
listbox_following.place(x=420,y=35)
listbox_not_following_back.place(x=570,y=35)
listbox_unfollow.place(x=720,y=35)

label_box1=Label(root,text="Followers:",bg="black",fg="white")
label_box2=Label(root,text="Followings",bg="black",fg="white")
label_box3=Label(root,text="Not Following Back:",bg="black",fg="white")
label_box4=Label(root,text="People to Unfollow:",bg="black",fg="white")
label_box1.place(x=270,y=10)
label_box2.place(x=420,y=10)
label_box3.place(x=570,y=10)
label_box4.place(x=720,y=10)

button_clear=Button(text="Clear boxes",font=fontStyle,width=20,command=clear_boxes,bg="black",fg="white",activebackground="green")
button_clear.place(x=15,y=485)

followers_c=StringVar()
following_c=StringVar()
nfb_c=StringVar()
unf_c=StringVar()

followers_c.set("0")
following_c.set("0")
nfb_c.set("0")
unf_c.set("0")

label_count_followers=Label(root,textvariable=followers_c,bg="black",fg="white")
label_count_following=Label(root,textvariable=following_c,bg="black",fg="white")
label_count_nfb=Label(root,textvariable=nfb_c,bg="black",fg="white")
label_count_unf=Label(root,textvariable=unf_c,bg="black",fg="white")
label_count_followers.place(x=332,y=10)
label_count_following.place(x=480,y=10)
label_count_nfb.place(x=690,y=10)
label_count_unf.place(x=838,y=10)


button_add=Button(root,text="===>",width=14,command=lambda:add_to_unf(listbox_not_following_back),bg="black",fg="white",activebackground="green")
button_add.place(x=570,y=520)
button_add2=Button(root,text="===>",width=14,command=lambda:add_to_unf(listbox_following),bg="black",fg="white",activebackground="green")
button_add2.place(x=420,y=520)

button_select=Button(root,text="Select All",width=14,command=lambda:select_lb(listbox_not_following_back),bg="black",fg="white",activebackground="green")
button_select.place(x=570,y=550)
button_select2=Button(root,text="Select All",width=14,command=lambda:select_lb(listbox_following),bg="black",fg="white",activebackground="green")
button_select2.place(x=420,y=550)
button_select3=Button(root,text="Select All",width=14,command=lambda:select_lb(listbox_unfollow),bg="black",fg="white",activebackground="green")
button_select3.place(x=720,y=550)
button_remove=Button(text="Remove",width=14,command=lambda:remove_box(listbox_unfollow),bg="black",fg="white",activebackground="green")
button_remove.place(x=720,y=520)


button_unfollow=Button(font=fontStyle2,text="START",width=29,height=1,bg="green",fg="white",activebackground="green",command=lambda:unfollow(listbox_unfollow))
button_unfollow.place(x=422,y=585)

canvas=Canvas(root,width=250,height=83,borderwidth=0, highlightthickness=0)
canvas.place(x=5,y=530)
img=PhotoImage(file="misc/other.png")
canvas.create_image(0,0,anchor=NW,image=img)

canvas=Canvas(root,width=245,height=176,borderwidth=0, highlightthickness=0)
canvas.place(x=0,y=0)
img2=PhotoImage(file="misc/logo1.png",)
canvas.create_image(0,0,anchor=NW,image=img2)


label_copyright=Label(text="@2021 Barrier Security. All rights reserved.",bg="black",fg="white")
label_copyright.place(x=5,y=620)

button_blog=Button(text="Blog",width=9,bg="yellow",fg="black",activebackground="green",font=fontStyle,command=lambda:redirect_website("https://krygennn.github.io"))
button_linkedin=Button(text="LinkedIn",width=9,bg="blue",fg="black",activebackground="green",font=fontStyle,command=lambda:redirect_website("https://www.linkedin.com/in/burak-baris/"))
button_instagram=Button(text="Instagram",width=9,bg="purple",fg="black",activebackground="green",font=fontStyle,command=lambda:redirect_website("https://www.instagram.com/burak_baris_"))
button_blog.place(x=275,y=530)
button_linkedin.place(x=275,y=565)
button_instagram.place(x=275,y=600)

root.mainloop()


