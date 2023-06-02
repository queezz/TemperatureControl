import tkinter as tk
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class MainWidget():

    def main(self,var_cur_temp=0):
        self.end_measurement = False

        self.sample_rate = 10 # Setting か何かでまとめるとよいかも
        self.scale_range = [5, 10, 30, 60, 300, 600, 1800, 3600]
        self.scale_num = 1
        self.scale = self.scale_range[self.scale_num]
        self.max_data_points = self.sample_rate * self.scale


        self.root = tk.Tk()

        self.costom_font = tk.font.Font(family="Arial",size=24)

        self.root.title("Temperature Setting")

        self.root.geometry("900x900")
        
        self.tar_temp = tk.IntVar()
        self.cur_temp = tk.DoubleVar()
        self.text_scale = tk.StringVar()
        self.text_scale.set(f'{self.scale} s')

        self.tar_temp.set(20)
        self.cur_temp.set(var_cur_temp)

        self.var_tar_temp = self.tar_temp.get()

        self.create_widgets()

        graph_thread = threading.Thread(target=self.update_graph,daemon=True)
        graph_thread.start()

        self.root.mainloop()


    def create_widgets(self):

        self.label_tar_temp = tk.Label(self.root, text="Target temperature :",font=self.costom_font)
        self.label_var_tar_temp = tk.Label(self.root, textvariable=self.tar_temp,font=self.costom_font)

        self.label_tar_temp.grid(row=0, column=0)
        self.label_var_tar_temp.grid(row=0, column=1,columnspan=2)

        self.label_cur_temp = tk.Label(self.root, text = "Current temperature :",font=self.costom_font)
        self.label_var_cur_temp = tk.Label(self.root, textvariable=self.cur_temp,font=self.costom_font)

        self.label_cur_temp.grid(row=1, column=0)
        self.label_var_cur_temp.grid(row=1, column=1,columnspan=2)

        self.set_button = tk.Button(self.root, text="Set", command=self.update_tar_temp,font=self.costom_font)
        self.entry = tk.Entry(self.root,font=self.costom_font)

        self.set_button.grid(row=2, column=0)
        self.entry.grid(row=2, column=1,columnspan=2)

        self.quit_button = tk.Button(self.root,text = 'Quit',command=self.quit,font=self.costom_font)
        
        self.quit_button.grid(row=3, column=0,columnspan=3)

        self.label_message = tk.Label(self.root,font=self.costom_font)
        self.label_message.grid(row=4, column=0,columnspan=3)

        self.fig = plt.figure(figsize=(9,4))
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.get_tk_widget().grid(row=5, columnspan=3)

        self.x_data = [0]
        self.y_data = [self.cur_temp.get()]

        self.down_scale_button = tk.Button(self.root,text = '▽',command=self.down_scale,font=self.costom_font)
        self.label_scale = tk.Label(self.root, textvariable=self.text_scale,font=self.costom_font)
        self.up_scale_button = tk.Button(self.root,text = '△',command=self.up_scale,font=self.costom_font)

        self.down_scale_button.place(x=125,y=700)
        self.label_scale.place(x=425,y=700)
        self.up_scale_button.place(x=725,y=700)

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
            self.update_message(text="Value Error! Insert Integer!")
            pass
        except UnboundLocalError:
            self.update_message(text="Value Error! Insert Integer!")
            pass

    def update_cur_temp(self,var_cur_temp):

        self.cur_temp.set(var_cur_temp)


    def update_graph(self):
        i = 0
        while True:
            if i % ((self.scale+self.sample_rate-1)//self.sample_rate) == 0:
                self.x_data += [self.x_data[-1] + 1/self.sample_rate]
                self.y_data += [self.cur_temp.get()]
            if self.y_data[0] == 0:
                self.x_data.pop(0)
                self.y_data.pop(0)
            self.x = self.x_data[:-self.max_data_points:-1]
            self.y = self.y_data[:-self.max_data_points:-1]
            if i % 5 == 0:
                self.ax.clear()
                self.ax.plot(self.x,self.y,c='k')
                self.canvas.draw()
            i += 1
            time.sleep(1/self.sample_rate)

    def up_scale(self):
        if self.scale_num + 1 != len(self.scale_range):
            self.scale_num += 1
            self.scale = self.scale_range[self.scale_num]
            self.max_data_points = self.sample_rate * self.scale
            if self.scale // 3600 != 0:
                self.text_scale.set(f'{self.scale//3600} h')
            elif self.scale // 60 != 0:
                self.text_scale.set(f'{self.scale//60} min')
            else:
                self.text_scale.set(f'{self.scale} s')
            self.update_message()
        else:
            self.update_message(text="Already max scale")


    def down_scale(self):
        if self.scale_num != 0:
            self.scale_num -= 1
            self.scale = self.scale_range[self.scale_num]
            self.max_data_points = self.sample_rate * self.scale
            if self.scale // 3600 != 0:
                self.text_scale.set(f'{self.scale//3600} h')
            elif self.scale // 60 != 0:
                self.text_scale.set(f'{self.scale//60} min')
            else:
                self.text_scale.set(f'{self.scale} s')
            self.update_message()
        else:
            self.update_message(text="Already min scale")



    def update_message(self,text=""):
        self.label_message["text"] = text
        self.label_message.grid(row=4, column=0,columnspan=3)

    def quit(self):
        self.end_measurement = True
        if __name__ == "__main__":
            self.root.destroy()





if __name__ == "__main__":
    app = MainWidget()
    app.main()
    # app.mainloop()

    



