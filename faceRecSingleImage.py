import os
import sys
import cv2
import csv
import logging
import tkinter as tk
from datetime import datetime
from faceRecFiler import Dlib_Face_Unlock
from logging.handlers import RotatingFileHandler
from tkinter import messagebox, PhotoImage, font, Canvas

# DIRECTORIES,FILE PATHS AND GLOBAL VARS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = BASE_DIR + '/images'
DT_STRING = datetime.now().strftime("%d/%m/%Y %H:%M:%S")


# LOGGING
LOG_FORMAT = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
logFile = 'faceRec.log'
handler = RotatingFileHandler(logFile, mode='a', maxBytes=4000,
                                 backupCount=3, encoding=None, delay=0)
handler.setFormatter(LOG_FORMAT)
handler.setLevel(logging.INFO)
app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)
app_log.addHandler(handler)

def main():
	root = tk.Tk()
	window = Window(root, "APPLECORE - INDUSTRIES", "1300x772",
                        font.Font(family="spaceranger",size=25),
                        PhotoImage(file="mr_potato_head_lg.png"))


class Window:
	def __init__(self, root, title, geometry, customfont, wallpaper):
		self.root = root
		self.root.title(title)
		self.root.geometry(geometry)
		self.root.cfont = customfont
		self.root.wp = wallpaper
		self.regFrame = tk.Frame()
		self.loginFrame = tk.Frame()
		self.userMenuFrame = tk.Frame()
		self.name = tk.StringVar()
		self.loggedInUser = tk.StringVar()
		self.logged_in_members = {}

		# BACKGROUND IMAGE
		my_label = tk.Label(self.root,image=self.root.wp)
		my_label.place(x=0,y=0,relwidth=1,relheight=1)

		# LOGIN FRAME
		tk.Label(self.loginFrame,text="Face",font=("spaceranger", 40),fg="white",bg="#001737").grid(row=1,column=1,pady=(40, 0))
		tk.Label(self.loginFrame,text="Recognition",font=("spaceranger", 40),fg="white",bg="#001737").grid(row=2,column=1,pady=(0,40),ipadx=20)
		regButton = tk.Button(self.loginFrame,text="Register",font=self.root.cfont,fg="white",bg="#fc355e",command=self.regFrameRaiseFrame)
		regButton.grid(row=3,column=1,ipadx=30,sticky="nswe")
		logoutBtn = tk.Button(self.loginFrame,text="Logout",font=self.root.cfont,fg="white",bg="#fc355e",command=self.user_logout)
		logoutBtn.grid(row=4,column=1,ipadx=30,columnspan=2,sticky="nswe")
		loginButton = tk.Button(self.loginFrame,text="Login",font=self.root.cfont,fg="white",bg="#fc355e",command=self.login)
		loginButton.grid(row=5,column=1,ipadx=30, sticky="nswe")

		# REGISTER-SUBMIT FRAME
		tk.Label(self.regFrame,text=" Hit spacebar when image shows ",font=self.root.cfont,bg="white").grid(row=1,column=1,columnspan=2)
		tk.Label(self.regFrame,text="Name:",font=self.root.cfont,bg="white").grid(row=2,column=1,ipadx=28)
		nameEntry = tk.Entry(self.regFrame,textvariable=self.name,font=self.root.cfont)
		nameEntry.focus_set()
		nameEntry.grid(row=2,column=2)
		registerButton = tk.Button(self.regFrame,text="Submit",font=self.root.cfont,fg="white",bg="#fc355e",command=self.register)
		registerButton.grid(row=3,column=1,ipadx=30,sticky="nswe", columnspan=2)

		# USER MENU FRAME
		tk.Label(self.userMenuFrame,text=" Hello ",font=self.root.cfont,fg="white",bg="#001737").grid(row=1,column=1,pady=(30, 30))
		tk.Label(self.userMenuFrame,textvariable=self.loggedInUser,font=("spaceranger", 35),fg="red",bg="#001737").grid(row=1,column=2,pady=(30, 30),sticky="w")
		tk.Label(self.userMenuFrame,text="  Welcome back!  ",font=self.root.cfont,fg="white",bg="#001737").grid(row=2,column=1,pady=(0, 10),columnspan=2)
		tk.Label(self.userMenuFrame,text='{}'.format(DT_STRING),font=("Helvetica", 15),fg="white",bg="#001737").grid(row=3,column=1,pady=(0, 40),columnspan=2)
		infoBtn = tk.Button(self.userMenuFrame,text="Members",font=self.root.cfont,fg="white",bg="#fc355e",command=self.user_info)
		infoBtn.grid(row=4,column=1,ipadx=30,columnspan=2,sticky="nswe")
		backBtn = tk.Button(self.userMenuFrame,text="Back",font=self.root.cfont,fg="white",bg="#fc355e",command=self.logFrameRaiseFrame)
		backBtn.grid(row=5,column=1,ipadx=30,columnspan=2,sticky="nswe")

		self.raiseFrame(self.loginFrame)
		self.root.bind('<Escape>', self.close)
		self.root.mainloop()


	def register(self):
		person = "-".join(self.name.get().split())
		# CHECK IF ENTRY TEXT BOX IS NOT EMPTY
		if not person:
			messagebox.showinfo("Alert", "Please enter your username    ")
			return
		if person + '.png' in [f for f in os.listdir(IMAGES_DIR)]:
			messagebox.showinfo("Alert", "Username taken    ")
			return

		cam = cv2.VideoCapture(0)

		while True:
			ret, frame = cam.read()
			cv2.imshow("Say cheese", frame)
			if not ret:
				break
			k = cv2.waitKey(1)

			# Q KEY PRESSED -> CLOSES THE WEBCAM WINDOW
			if k % 256 == 99 or k % 256 == 67:
				print("Closing Webcam")
				cam.release()
				cv2.destroyAllWindows()
				break

			# PRESS SPACE KEY TO TAKE PHOTO
			if k % 256 == 32:
				img_name = person + ".png"
				cv2.imwrite(os.path.join(IMAGES_DIR, img_name), frame)
				cam.release()
				cv2.destroyAllWindows()
				break

		# WEBCAM IMAGE PROMPT
		result = messagebox.askquestion("Notice", "Do you wish to keep this photo? ")
		if result == 'no':
			os.remove(os.path.join(IMAGES_DIR, img_name))
		else:
			# WRITE TO LOGFILE AND CSV FILE
			app_log.info(f"{person} REGISTERED")
			with open(BASE_DIR + '/registered.csv', 'a') as f:
				writer = csv.writer(f)
				writer.writerow([person, DT_STRING])

		self.raiseFrame(self.loginFrame)
		self.hideFrame(self.regFrame)


	def login(self):
		dfu = Dlib_Face_Unlock()
		user = dfu.ID()
		if not user:
			messagebox.showerror("Call Security", "Face Not Recognised    ")
			return
		person = str(user[0])
		self.loggedInUser.set(user[0])
		self.logged_in_members[person] = DT_STRING
		app_log.info(f"{person} LOGGED-IN")
		self.raiseFrame(self.userMenuFrame)
		self.hideFrame(self.loginFrame)


	def user_logout(self):
		dfu = Dlib_Face_Unlock()
		user = dfu.ID()
		if not user:
			messagebox.showerror("Call Security", "Face Not Recognised    ")
			return
		leaver = str(user[0])
		if leaver in self.logged_in_members:
			del self.logged_in_members[leaver]
			messagebox.showinfo("Confirmation", "{} logged out    ".format(leaver))
			app_log.info(f"{leaver} LOGGED-OUT")
		else:
			messagebox.showerror("Error", "User not logged in    ")


	# READ CSV FILE
	def user_info(self):
		# NEW MEMBERS INFORMATION WINDOW
		top = tk.Toplevel()
		top.title = 'MEMBERS INFORMATION'
		top.geometry("550x300")
		listbox = tk.Listbox(top)
		listbox.pack(side=tk.LEFT,fill=tk.BOTH,expand=True)
		scrollbar = tk.Scrollbar(top)
		scrollbar.pack(side=tk.RIGHT,fill=tk.BOTH)
		listbox.config(fg="white",bg="#1c1c1b",yscrollcommand=scrollbar.set)
		scrollbar.config(command=listbox.yview)
		exitBtn = tk.Button(listbox,text="Close",fg="black",bg="white",command=top.destroy)
		exitBtn.pack(fill=tk.BOTH,side=tk.BOTTOM)
		# HACKY FORMATING INSTEAD OF USING PANDAS
		with open(BASE_DIR + '/registered.csv', 'r') as f:
			listbox.insert(tk.END, 'REGISTERED                TIME-IN                        IN      NAME')
			csr = csv.reader(f)
			# USING IF ROW BECAUSE: YOU MIGHT HAVE HIDDEN
			# UNWANTED CHARS AT THE END OF YOUR CSV FILE
			# IF NOT CLEANED UP PROPERLY. EG '/n' OR EMPTY STRING?
			for row in csr:
				if row:
					fname = row[0]
					timein = self.logged_in_members.get(fname, '')
					if fname in self.logged_in_members:
						yorn = "   Yes    "
					else:
						yorn = "N/A    -------------------   no     "
					nline ='{}    {}{}{}'.format(row[1], timein, yorn, fname).lstrip()
					listbox.insert(tk.END, nline)
					listbox.itemconfig(0, {'fg': 'red'})


	def hideFrame(self, frame):
		frame.grid_forget()

	def raiseFrame(self, frame):
		frame.grid(row=0,column=0, padx=20, sticky='nw')
		frame.configure(bg='#001737')
		frame.tkraise()

	def regFrameRaiseFrame(self):
		self.raiseFrame(self.regFrame)
		self.hideFrame(self.loginFrame)

	def logFrameRaiseFrame(self):
		self.raiseFrame(self.loginFrame)
		self.hideFrame(self.userMenuFrame)

	# ESCAPE KEY - QUIT PROGRAM
	def close(self, event):
		print("Escape hit, closing...")
		cv2.destroyAllWindows()
		sys.exit()

	# LOAD FACES
	dfu = Dlib_Face_Unlock()


main()
