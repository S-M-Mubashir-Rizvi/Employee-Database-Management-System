from tkinter import Tk, Label, Button, Entry, LabelFrame
from tkinter import messagebox
from tkinter import filedialog, simpledialog, Listbox, Scrollbar
import time as t

entered_records = [ ]            #contains all records the user entered after starting application
loaded_records = [ ]              #contains all records which were loaded from a file
list_box =""                             #creating this variable in main code because it was used in different functions
list_of_all_records = [ ]         #combined, modified, final form of all the records

def delt_entry(e):
    """ Clears the text from a entry box """
    e.delete(0,"end")

    
def data_save_Shell():
    """ Fetches information from the interface and saves it in a variable present in main code """
    global entered_records
    flag = 0
    record = [  ]
    name = e1.get()
    age = e2.get()
    DOB = e3.get()
    email = e4.get()
    employment = e5.get()
    contact = e6.get()
    wage_per_day = e8.get()
    total_working_days = e9.get()    
    if int(age) < 60 :                  # Checking age requirements
        pass
    if int(age) >= 60:
        flag +=1
        messagebox.showerror(title = "Wrong input" ,message = "Age requirement is not met")       
    ID = e7.get()
    if len(ID) == 7:                 # Checking length of ID requirements
        pass
    if len(ID) != 7:
        flag +=1
        messagebox.showerror(message = "ID must be of 7 characters")
    if flag ==0:
        record.append(name)
        record.append(age)
        record.append(DOB)
        record.append(email)
        record.append(employment)
        record.append(contact)
        record.append(ID)
        record.append(wage_per_day)
        record.append(total_working_days)
        entered_records.append(record)
    if flag !=0:
       messagebox.showerror(message = "Wrong data was entered, could not be saved!")



def add_new():
    """ Asks to save and remove the previous data """
    confirm = messagebox.askyesno(title = "Confirmation" ,message = "Save previous data?")
    if confirm == True:
        data_save_Shell()
        confirm = messagebox.askyesno(title = "Confirmation" ,message = "Remove previous data?")
        if confirm == True:
            global label_retire
            delt_entry(e1)
            delt_entry(e2)
            delt_entry(e3)
            delt_entry(e4)
            delt_entry(e5)
            delt_entry(e6)
            delt_entry(e7)
            delt_entry(e8)
            delt_entry(e9)
            label_retire.config(text = "")             # Clearing retirement label by simply setting text in it to a empty string

        
def load_file():
    """ Asks for a file from the user to load records from, those records are then saved in a variable present in main code """
    global loaded_records
    file_name = filedialog.askopenfilename(initialdir = "/" , title = "Select A File" , filetypes = (("Text Files","*.txt"),("All Files", "*.*")))   
    f = open(file_name)                    # The two items in filetypes shows that there would be 2 items in dropdown menu when user is selecting file
    content = f.readlines()
    for one_record in content:
        one_record = one_record.split("_")
        record = [ ]
        record.append(one_record[ 0 ])
        record.append(one_record[ 1 ])
        record.append(one_record[ 2 ])
        record.append(one_record[ 3 ])
        record.append(one_record[ 4 ])
        record.append(one_record[ 5 ])
        record.append(one_record[ 6 ])
        record.append(one_record[ 7 ])
        sixth_data = one_record[ 8 ] 
        sixth_data = sixth_data[ 0 : len(sixth_data)-1]         # since the last data will have "\n" in it, i used string slicing to remove it so that it is not displayed when all records are displayed
        record.append(sixth_data)
        loaded_records.append (record)      
    f.close()
    t.sleep(1)
    messagebox.showinfo(message = "File loadad successfully")
            

def display_records():
    """ Displays records in a new window, uses the variables from the main code, combines them,and creates a new window with a listbox and a scrollbar, and displays information """
    global list_box
    global list_of_all_records
    list_of_all_records = loaded_records             # Here i am checking if user has entered the same entry of an employee that was earlier loaded from a file
    for record in entered_records:
        if record not in loaded_records:
            list_of_all_records.append(record)
    display_window = Tk()
    display_window.title("Records Display")
    display_window.geometry("1280x720")
  
    frame = LabelFrame(display_window)
    scroll_bar = Scrollbar(frame , orient = "vertical")          # I want the scrollbar to be vertical

    list_box = Listbox(frame, width =1280 , height = 720, yscrollcommand = scroll_bar.set, font = ("Helvetica",14,"bold"), bg = "#212121")  #The yscrollcommand links scrollbar with listbox
    scroll_bar.config(command = list_box.yview)          #here the command is given to be viewed or moved up and down along y-axis
    
    scroll_bar.pack(side = "right", fill = "y")  # I want the scrollbar to be on the right side
    frame.pack()
    list_box.pack(pady = 20)
    
    for record in range(len(list_of_all_records)):
        monthly_wage = int(list_of_all_records[record][7]) * int(list_of_all_records[record][8])
        age = list_of_all_records[record][1]
        if int(age) < 60:                                           # here retirement age is calculated again since the function I made was to display the result on the main interface
            retiring_age = 60 - int(age)                  # and here I need to display it in a separate window i.e the display_window
            current_time = t.time()
            time_when_retiring = current_time + ((retiring_age * 365)*86400)
            retiring_date = t.localtime(time_when_retiring)
        
            list_box.insert("end","{ Record Number: "+str(record+1) + " }")
            list_box.insert("end","Name: "+list_of_all_records[record][0])
            list_box.insert("end","Age: "+ list_of_all_records[record][1] + ",  " + "DOB: "+list_of_all_records[record][2] + ",  " + "Email Address: " + list_of_all_records[record][3] + ",  " + "Contact: " + list_of_all_records[record][5])
            list_box.insert("end" , "Employment: " + list_of_all_records[record][4] + ",  " + "ID: " + list_of_all_records[record][6] + ",  " + "Monthly Wage: " + str(monthly_wage))
            list_box.insert("end", "Retirement Year: " + str(retiring_date.tm_year) + " (At 60 Years Of Age) ")

        

 
def save_file():
    """ Asks a file to save data in and then the data displayed to the user is saved in the selected file """
    global list_of_all_records
    filename = filedialog.asksaveasfilename(initialdir = "/" ,title = "Select A File" , defaultextension = ".txt", confirmoverwrite = False,filetypes = (("Text Files","*.txt"),("All Files", "*.*")))
    f = open(filename, "r+")
    content = f.read()

    for record in list_of_all_records:
        if record[6] not in content:                           # here i am checking the ID of a record, ID is on the 6th position in the list
            for data in range(len(record)):                # comparing that ID to the contact previously present in the file
                if (data < (len(record) - 1) ):                 # if it matches then the same record would not be written in the file
                    f.write(record[ data ] +"_")
                if (data == (len(record)- 1) ):
                    f.write(record[data] +"\n")
    f.close()
    t.sleep(1)
    messagebox.showinfo(message = "Record saved in file successfully")    


def delete_record():
    """ Asks user to delete records either from the current displayed records or from a file which the user will select """
    global list_box
    global list_of_all_records    
    list_of_all_records = loaded_records         # checkin again if some same record was entered by the user
    for record in entered_records:
        if record not in loaded_records:
            list_of_all_records.append(record)
    option = simpledialog.askinteger("Input","1.)Delete record from display \n2.)Delete record from file?")          # asking user from where he/she wants to delete the record from
    
    if option == 1 :
        record_to_delete = simpledialog.askstring("Input","1.)Enter ID of employee")      #asking user the ID of that employee whose record he/she wants to be removed
        list_box.delete(0,"end")                                # Clearing eveythin in the listbox, so that I can display it again excluding the record wanted to be removed
        for record in list_of_all_records:
            if record_to_delete in record:
                list_of_all_records.remove(record)             # Deleted that record from the list of all records


        for record in range(len(list_of_all_records)):   # here the same code is followed as used in display_records, the listbox is filled again with records, and the specified record is removed 
            monthly_wage = int(list_of_all_records[record][7]) * int(list_of_all_records[record][8])                                                                                                 
            age = list_of_all_records[record][1]
            if int(age) < 60:
                retiring_age = 60 - int(age)
                current_time = t.time()
                time_when_retiring = current_time + ((retiring_age * 365)*86400)
                retiring_date = t.localtime(time_when_retiring)
            
                list_box.insert("end","{ Record Number: "+str(record+1) + " }")
                list_box.insert("end","Name: "+list_of_all_records[record][0])
                list_box.insert("end","Age: "+ list_of_all_records[record][1] + ",  " + "DOB: "+list_of_all_records[record][2] + ",  " + "Email Address: " + list_of_all_records[record][3] + ",  " + "Contact: " + list_of_all_records[record][5])
                list_box.insert("end" , "Employment: " + list_of_all_records[record][4] + ",  " + "ID: " + list_of_all_records[record][6] + ",  " + "Monthly Wage: " + str(monthly_wage))
                list_box.insert("end", "Retirement Year: " + str(retiring_date.tm_year) + " (At 60 Years Of Age) ")

    if option == 2:          # option 2, when user wants to delete record from a file
        file_name = filedialog.askopenfilename(initialdir = "/" , title = "Select A File" , filetypes = (("Text Files","*.txt"),("All Files", "*.*")))
        record_to_delete = simpledialog.askstring("Input","1.)Enter ID of employee")        # asking ID of that employee
        f = open(file_name, "r")
        content = f.readlines()       # readin lines and confirming if he/she wants to remove it
        confirm = messagebox.askyesno(title = "Confirmation" ,message = "Are you sure you want to remove?")
        if confirm == True:
            for record in content:       # here i searched the record the user wanted to remove in the file and removed it used .remove(), since readlines returns a list, .remove() is a list method
                if record_to_delete in record:
                    content.remove(record)                   
            f.close               
            f = open(file_name , "w")      # opened the file again but this time in "w" mode so that previous data is removed
            for record in content:         # the file is filled again but the specified record is removed from the file
                f.write(record)
            f.close()
        t.sleep(1)
        messagebox.showinfo(message = "Record removed from file successfully")
        f.close()


def exit_app():
    """ Asks user to confirm if the data is saved in some file, it not, the user is asked if he/she would like to save it, and then exits the application """
    confirm = messagebox.askyesno(title = "Save confirmation", message = "Have you saved data displayed in a file?")   # asking user if data has been saved in a file or not
    if confirm == True:
        exit_confirm = messagebox.askyesno(title = "Exit", message = "Do you wish to exit?") # if yes then, asking confirmation to exit the app
        if exit_confirm == True:
            r.destroy()
        else:
            pass
    if confirm == False:    # if user hasnt saved data in a file then this code runs
        save_confirm = messagebox.askyesno(title = "Save file" , message = "Do you wish to select  file to save data?")   # asking user to select the file to save data in
        if save_confirm == True:      # if he/she wishes to save it in a file, the save_file() function is called which saved data that is displayed to the user 
            save_file()
        else:
            exit_confirm = messagebox.askyesno(title = "Exit", message = "Do you wish to exit?")  # if he/she doesnt want to save it in a file, asking for confirmation to exit
            if exit_confirm == True:
                r.destroy()
            else:
                pass
            
        


def calculate_retirement_button():
    """ Function made to calculate the retirement age ( at 60 years ), this function is restricted for the interface only"""
    age = e2.get()           # fetching age
    if int(age) < 60:         # checking requirement
        retiring_age = 60 - int(age) 
        current_time = t.time()                # t.time()=return number of seconds from the point where time began (based on programming language, python uses Unix Epooc) 
        time_when_retiring = current_time + ((retiring_age * 365)*86400)         
        retiring_date = t.localtime(time_when_retiring)         # t.localtime()=returns the seconds into a format which is in year,day,month,hours,seconds,minutes etc
        
        date = "Year of Retirement: "+ str(retiring_date.tm_year) + "\n(At 60 Years Of Age)"            # fetching only the year  
        label_retire.config(text = date)

    if int(age) > 60:
        label_retire.config(text = "Age should be less than 60")


    
r = Tk()
r.title("DATABASE")
r.geometry("1366x768")
r.config(bg = "#212121")
lab = Label(r,text = "Enter Employee Information ",font = ("Times New Roman",26,"bold"), fg = "#3F51B5", bg = "#B2EBF2")
lab.pack()
f = LabelFrame(r , height = 1360, width = 720)
f.pack(padx = 20 , pady = 40)
f.pack_propagate(False)                                          # Propagate allows to change the default settings(height,width etc)

                  # FRAME 1     # Adding 5 labels with entries of each using label,entry widgets
f1 = LabelFrame(f , height = 500, width = 650, bg = "#00BCD4")
f1.grid(row = 0 , column = 0)
f1.grid_propagate(False)

lab1 = Label(f1 , text="1.) Name: ",font= ("Times New Roman",20,"bold"), fg = "#3F51B5", bg = "#B2EBF2")
lab1.grid(row = 1 , sticky = "NW" ,padx = 20, pady = 30)
e1 = Entry(f1 ,font = ("Times New Roman",14))
e1.grid(row = 1 , column = 1 ,padx = 10)

lab2 = Label(f1 , text="2.) Age: ",font= ("Times New Roman",20,"bold"), fg = "#3F51B5", bg = "#B2EBF2")
lab2.grid(row = 2 , sticky = "NW" ,padx = 20, pady = 30)
e2 = Entry(f1 ,font = ("Times New Roman",14))
e2.grid(row = 2 , column = 1 ,padx = 10)

lab3 = Label(f1 , text="3.) Date of Birth: ",font= ("Times New Roman",20,"bold"), fg = "#3F51B5", bg = "#B2EBF2")
lab3.grid(row = 3 , sticky = "NW",padx = 20 , pady = 30)
e3 = Entry(f1 ,font = ("Times New Roman",14))
e3.grid(row = 3 , column = 1,padx = 10 )

lab4 = Label(f1 , text="4.) Email Address: ",font= ("Times New Roman",20,"bold"), fg = "#3F51B5", bg = "#B2EBF2")
lab4.grid(row = 4 , sticky = "NW",padx = 20 , pady = 30)
e4 = Entry(f1 ,font = ("Times New Roman",14))
e4.grid(row = 4 , column = 1 ,padx = 10)

lab5 = Label(f1 , text="5.) First Day of Employment: ",font= ("Times New Roman",20,"bold"), fg = "#3F51B5", bg = "#B2EBF2")
lab5.grid(row = 5 , sticky = "NW" ,padx = 20 , pady = 30)
e5 = Entry(f1 ,font = ("Times New Roman",14))
e5.grid(row = 5 , column = 1 ,padx = 10)


                    # FRAME 2    # Adding 4 labels with entries of each, and one button (retirement) with its label using label,entry,button widgets
f2 = LabelFrame(f , height = 500, width = 650, bg = "#00BCD4")
f2.grid(row=0 , column= 1)
f2.grid_propagate(False)

lab6 = Label(f2 , text="6.) Contact Number: ",font= ("Times New Roman",20,"bold"), fg = "#3F51B5", bg = "#B2EBF2")
lab6.grid(row = 1 , sticky = "NW",padx = 20 , pady = 30)
e6 = Entry(f2 ,font = ("Times New Roman",14))
e6.grid(row = 1 , column = 1 ,padx = 70)

lab7 = Label(f2 , text="7.) ID (7 Characters): ",font= ("Times New Roman",20,"bold"), fg = "#3F51B5", bg = "#B2EBF2")
lab7.grid(row = 2 , sticky = "NW" ,padx = 20, pady = 30)
e7 = Entry(f2 ,font = ("Times New Roman",14))
e7.grid(row = 2 , column = 1 ,padx = 70)

lab8 = Label(f2 , text="8.) Wage Per Day: ",font= ("Times New Roman",20,"bold"), fg = "#3F51B5", bg = "#B2EBF2")
lab8.grid(row = 3 , sticky = "NW" ,padx = 20, pady = 30)
e8 = Entry(f2 ,font = ("Times New Roman",14))
e8.grid(row = 3 , column = 1 ,padx = 70)

lab9 = Label(f2 , text="9.) Total Working Days: ",font= ("Times New Roman",20,"bold"), fg = "#3F51B5", bg = "#B2EBF2")
lab9.grid(row = 4 , sticky = "NW" ,padx = 20 , pady = 30)
e9 = Entry(f2 ,font = ("Times New Roman",14))
e9.grid(row = 4 , column = 1 ,padx = 70)

b = Button(f2 , text="10.) Calculate \nRetirement: ",font= ("Times New Roman",20,"bold"), fg = "#3F51B5" , bg = "#B2EBF2", command =calculate_retirement_button)
b.grid(row = 5 , sticky = "NW",padx = 20  , pady = 15)
label_retire = Label(f2,font = ("Times New Roman",14))
label_retire.grid(row = 5 , column = 1 ,padx = 70)

      
                   # FRAME 3          # Adding functions used in the code in this frame using button widget
f3 = LabelFrame(r , height = 90, width = 850, bg = "#00BCD4")
f3.pack()
f3.pack_propagate(False)

b1 = Button(f3, text = "ADD\nNEW",font= ("Times New Roman",18), fg = "#3F51B5", bg = "#B2EBF2",command = add_new)
b1.grid(row = 0, column = 0,padx = 50, pady = 10)

b2 = Button(f3, text = "LOAD\nFILE" ,font= ("Times New Roman",18), fg = "#3F51B5", bg = "#B2EBF2",command = load_file)
b2.grid(row = 0,column = 1,padx = 50, pady = 10)

b3 = Button(f3, text = "DISPLAY\nRECORDS" ,font= ("Times New Roman",18), fg = "#3F51B5", bg = "#B2EBF2",command = display_records)
b3.grid(row = 0,column = 2,padx = 50, pady = 10)

b4 = Button(f3, text = "FILE\nSAVE",font= ("Times New Roman",18), fg = "#3F51B5", bg = "#B2EBF2",command = save_file)
b4.grid(row = 0,column = 3,padx = 50, pady = 10)

b5 = Button(f3, text = "DELETE\nRECORD",font= ("Times New Roman",18), fg = "#3F51B5", bg = "#B2EBF2",command = delete_record)
b5.grid(row = 0,column = 4,padx = 50, pady = 10)

b6 = Button(f3, text = "EXIT\nAPP",font= ("Times New Roman",18), fg = "#3F51B5", bg = "#B2EBF2",command = exit_app)
b6.grid(row = 0,column = 5,padx = 50, pady = 10)

r.mainloop()
