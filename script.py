import tkinter as tk
from model.process_model import Process
from tkinter.messagebox import showinfo

class Application(tk.Frame):
    processes = []
    start_time = 5
    start_x = 0
    start_y = 25
    size = 25
    margin = 25

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.wm_title("Lamport")
        self.pack()
        self.create_process()
        self.create_parameters()
        self.create_buttons()
        self.create_canvas()

    def create_process(self):
        self.label = tk.Label(self, text="Numero de processos")
        self.label.grid(row=1, column=1)

        self.entry = tk.Entry(self)
        self.entry.grid(row=1, column=2, columnspan=2)
    
    def create_parameters(self):
        self.emiter_label = tk.Label(self, text="Processo Emissor", fg="blue")
        self.emiter_label.grid(row=2, column=1)

        self.emiter_entry = tk.Entry(self)
        self.emiter_entry.grid(row=2, column=2)

        self.emiter_time_label = tk.Label(self, text="Tempo")
        self.emiter_time_label.grid(row=2, column=3)

        self.emiter_time_entry = tk.Entry(self)
        self.emiter_time_entry.grid(row=2, column=4)

        self.receiver_label = tk.Label(self, text="Processo Receptor", fg="red")
        self.receiver_label.grid(row=3, column=1)

        self.receiver_entry = tk.Entry(self)
        self.receiver_entry.grid(row=3, column=2)

        self.receiver_time_label = tk.Label(self, text="Tempo")
        self.receiver_time_label.grid(row=3, column=3)

        self.receiver_time_entry = tk.Entry(self)
        self.receiver_time_entry.grid(row=3, column=4)

    def create_buttons(self):
        self.send_button = tk.Button(self, text="Enviar", command=self.calculate)
        self.send_button.grid(row=4, column=2)

        self.sync_button = tk.Button(self, text="Sincronizar", command=self.sync)
        self.sync_button.grid(row=4, column=3)
    
    def create_canvas(self):
        self.canvas = tk.Canvas(self, width=500, height=250, background="white") 
        self.canvas.grid(row=5, column=1, columnspan=5)

    def create_processes_grid(self):
        self.canvas.delete("all")

        if len(self.processes) == 1:
            self.start_x = 500 / 2 - 12
        elif len(self.processes) == 10:
            self.start_x = 12
        elif len(self.processes) > 1:
            self.start_x = 500 / len(self.processes) - 12

        start_x = self.start_x
        start_y = self.start_y
        size = self.size
        margin = self.margin

        for i in range(len(self.processes)):
            self.canvas.create_text(start_x + (i * size) + (margin * i) + 12, 10, text="P" + str(i), fill="#F00")
            for j in range(len(self.processes[i])):
                x1 = start_x + (i * size) + (margin * i)
                x2 = x1 + size
                y1 = (j * size) + start_y
                y2 = y1 + size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#fff")
                self.canvas.create_text(x1 + 12, y1 + 10, text=str(self.processes[i][j].value), fill=self.processes[i][j].color)
    
    def create_lines(self, p1, t1, p2, t2):
        self.processes[p1][t1]
        self.processes[p2][t2]

        start_x = self.start_x
        start_y = self.start_y
        size = self.size
        margin = self.margin

        x1 = start_x + (p1 * size) + (margin * p1) + 12
        y1 = (t1 * size) + start_y + 12
        x2 = start_x + (p2 * size) + (margin * p2) + 12
        y2 = (t2 * size) + start_y + 12
        
        self.canvas.create_line(x1, y1, x2, y2, fill="#0f0")

        pass

    def calculate(self):
        try:
            self.processes = []
            self.start_time = 5
            number_of_process = self.entry.get()
            for i in range(int(number_of_process)):
                new_process = []
                value = 0
                for j in range(10):
                    value = self.start_time * j
                    process = Process(value, color="black")
                    new_process.append(process)
                self.processes.append(new_process)
                value = 0
                self.start_time += 3
            

            self.create_processes_grid()
        except:
            showinfo('Erro', 'Erro ao mostrar processos')

    def sync(self):
        try:
            emiter = int(self.emiter_entry.get())
            emiter_time = int(self.emiter_time_entry.get())

            receiver = int(self.receiver_entry.get())
            receiver_time = int(self.receiver_time_entry.get())

            self.processes[receiver][receiver_time].value = 1 + self.processes[emiter][emiter_time].value

            self.processes[emiter][emiter_time].color = "blue"
            self.processes[receiver][receiver_time].color = "red"

            razao = self.processes[receiver][1].value
            for i in range(receiver_time+1,len(self.processes[receiver])):
                self.processes[receiver][i].value = self.processes[receiver][i-1].value + razao
                self.processes[receiver][i].color = "red"

            self.create_processes_grid()
            self.create_lines(emiter, emiter_time, receiver, receiver_time)
        except:
            if (len(self.processes) == 0):
                showinfo("Erro", "Primeiro crie os processos")
            else:
                showinfo("Erro", "Erro ao sincronizar os processos")

root = tk.Tk()
app = Application(master=root)
app.mainloop()