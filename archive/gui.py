import tkinter as tk
import time
import threading

# start_flag = False
# quitting_flag = False

class MainWidget():
    # start_flag = False
    # quitting_flag = False
    # count = 0

    def main(self,var_cur_temp=0):
        self.end_measurement = False
        self.root = tk.Tk()
        self.root.title("Temperature Setting")

        self.root.geometry("300x300")

        self.tar_temp = tk.IntVar()
        self.cur_temp = tk.IntVar()

        self.tar_temp.set(0)
        self.cur_temp.set(var_cur_temp)

        self.var_tar_temp = self.tar_temp.get()

        self.create_widgets()

        self.root.mainloop()
        # i = 0
        # while i < 30:
        #     self.update_cur_temp(i)
        #     i += 1
        #     time.sleep(0.1)

    def create_widgets(self):

        self.label_tar_temp = tk.Label(self.root, text="Target temperature :")
        self.label_var_tar_temp = tk.Label(self.root, textvariable=self.tar_temp)

        self.label_tar_temp.grid(row=0, column=0)
        self.label_var_tar_temp.grid(row=0, column=1)

        self.label_cur_temp = tk.Label(self.root, text = "Current temperature :")
        self.label_var_cur_temp = tk.Label(self.root, textvariable=self.cur_temp)

        self.label_cur_temp.grid(row=1, column=0)
        self.label_var_cur_temp.grid(row=1, column=1)

        self.set_button = tk.Button(self.root, text="Set", command=self.update_tar_temp)
        self.entry = tk.Entry(self.root)

        self.set_button.grid(row=2, column=0)
        self.entry.grid(row=2, column=1)

        self.quit_button = tk.Button(self.root,text = 'Quit',command=self.quit)
        
        self.quit_button.grid(row=3, column=0,columnspan=2)

        self.label_message = tk.Label(self.root)
        self.label_message.grid(row=4, column=0,columnspan=2)

    def update_tar_temp(self):
        try:
            new_value = int(self.entry.get())
            if 0 <= new_value <= 1200:
                self.tar_temp.set(new_value)
                self.var_tar_temp = self.tar_temp.get()
                self.update_message()
            else:
                if new_value > 1200:
                    self.tar_temp.set(1200)
                    self.var_tar_temp = self.tar_temp.get()
                self.update_message(text="Target temperature is limmited within 0 to 1200")

        except ValueError:
            self.update_message(text="Value Error\n Insert Integer")
            pass
        except UnboundLocalError:
            self.update_message(text="Value Error\n Insert Integer")
            pass

    def update_cur_temp(self,var_cur_temp):
        self.cur_temp.set(var_cur_temp)

    # def updates_cur_temp(self):
    #     global start_flag
    #     global quitting_flag
    #     i = 0
    #     while not quitting_flag:
    #         if start_flag:
    #             i += 1
    #             if i > 100:
    #                 start_flag = False                
    #             self.update_cur_temp(i)
    #             time.sleep(0.1)

    def update_message(self,text=""):
        self.label_message["text"] = text
        self.label_message.grid(row=4, column=0,columnspan=2)

    def quit(self):
        self.end_measurement = True





if __name__ == "__main__":
    app = MainWidget()
    app.main()
    # app.mainloop()

    



