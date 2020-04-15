from tkinter import *
import search


def searchstuff():
    global min_year_inpt
    global max_year_inpt
    global min_usescore_inpt
    global min_metascore_inpt
    global descend
    global inc_tbd
    for child in scrollable_frame.winfo_children():
        child.destroy()
    try:
        min_year = int(min_year_inpt.get())
    except:
        return
    try:
        max_year = int(max_year_inpt.get())
    except:
        return
    try:
        min_usescore = float(min_usescore_inpt.get())
    except:
        return
    try:
        min_metascore = float(min_metascore_inpt.get())
    except:
        return
    descend_fr = descend.get()
    inc_tbd_fr = inc_tbd.get()
    try:
        esskeetit = search.search(min_year, max_year, min_usescore,
                                  min_metascore, inc_tbd, 'title', descend_fr)
    except:
        return
    if len(esskeetit) == 0:
        error_msg = Label(scrollable_frame,
                          text='No games meet the criteria', anchor='w')
        error_msg.grid(row=0, column=0)
    for i, obj in enumerate(esskeetit):
        dispresult(obj, i)


def dispresult(obj, ro):
    global WIDTH
    global scrollable_frame
    ro *= 4
    # global window
    obj_title = Label(scrollable_frame, text=obj['title'], font=(
        "TkDefaultFont", 20), anchor='w')
    obj_date = Label(scrollable_frame, text=obj['date'],  font=(
        'TkDefaultFont', 10), anchor='w')
    summ = obj['summary'].replace('\n', '')
    obj_sum = Label(scrollable_frame, text=summ, font=(
        'TkDefaultFont', 15), justify='left', wraplength=WIDTH - 10)
    obj_scores = Frame(scrollable_frame)
    obj_meta = Label(obj_scores, text=f"Metascore: {obj['scores']['metascore']}", font=(
        'TkDefaultFont', 12), anchor='w')
    obj_user = Label(obj_scores, text=f"Userscore: {obj['scores']['userscore']}", font=(
        'TkDefaultFont', 12), anchor='w')
    obj_title.grid(row=ro+1, sticky=W)
    obj_date.grid(row=ro+2, sticky=W)
    obj_sum.grid(row=ro+3, sticky=W)
    obj_scores.grid(row=ro+4, sticky=W)
    obj_meta.pack(side='left')
    obj_user.pack(side='right')


window = Tk()
window.title('Find Games')
descend = IntVar()
inc_tbd = IntVar()
INPUT_WIDTH = 5
WIDTH = 480

params_frame = Frame(window)
search_button = Button(params_frame, text='Search!', command=searchstuff)

check_frame = Frame(params_frame)
descending = Checkbutton(check_frame, text='Descending?',
                         variable=descend, onvalue=True, offvalue=False)
include_tbd = Checkbutton(check_frame, text='Include TBD scores?',
                          variable=inc_tbd, onvalue=True, offvalue=False)


years_frame = Frame(params_frame)

min_year_frame = Frame(years_frame)
min_year_lbl = Label(min_year_frame, text='Min Year: ')
min_year_inpt = Entry(min_year_frame, width=INPUT_WIDTH)

max_year_frame = Frame(years_frame)
max_year_lbl = Label(max_year_frame, text='Max Year:')
max_year_inpt = Entry(max_year_frame, width=INPUT_WIDTH)

scores_frame = Frame(params_frame)

min_usescore_frame = Frame(scores_frame)
min_usescore_lbl = Label(min_usescore_frame, text='Min usescore:  ')
min_usescore_inpt = Entry(min_usescore_frame, width=INPUT_WIDTH)

min_metascore_frame = Frame(scores_frame)
min_metascore_lbl = Label(min_metascore_frame, text='Min metascore:')
min_metascore_inpt = Entry(min_metascore_frame, width=INPUT_WIDTH)

container = Frame(window, width=WIDTH, height=457)
canvas = Canvas(container, width=WIDTH, height=457)
scrollbar = Scrollbar(container, orient='vertical', command=canvas.yview)
scrollable_frame = Frame(canvas, width=WIDTH, height=457)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
canvas.configure(yscrollcommand=scrollbar.set)


params_frame.grid(row=0, sticky=W)
years_frame.grid(row=0, column=1)
scores_frame.grid(row=0, column=2)
check_frame.grid(row=0, column=3)

min_year_frame.grid(row=0, sticky=W)
max_year_frame.grid(row=1, sticky=W)

min_usescore_frame.grid(row=0, sticky=W)
min_metascore_frame.grid(row=1, sticky=W)

descending.grid(row=0, sticky=W)
include_tbd.grid(row=1, sticky=W)

min_year_lbl.grid(row=0, column=0)
min_year_inpt.grid(row=0, column=1)

max_year_lbl.grid(row=0, column=0)
max_year_inpt.grid(row=0, column=1)

min_usescore_lbl.grid(row=0, column=0)
min_usescore_inpt.grid(row=0, column=1)

min_metascore_lbl.grid(row=0, column=0)
min_metascore_inpt.grid(row=0, column=1)

search_button.grid(row=0, column=4)
window.geometry('513x513')
window.resizable(False, False)
container.grid(row=1)
canvas.pack(side='left', fill='both', expand=True)
scrollbar.pack(side='right', fill='y')
mainloop()
