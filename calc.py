'''
app

first-order poker calculator.

calculates the % chance of hitting 1 of N outs.
calculates the minimum Implied Odds needed to call a bet of different sizes.

inputs:
N = number of outs
P = number of players

controlled with arrow keys rather than keyboard entry.
'''

import tkinter as tk

import eq


WINDOW = tk.Tk()
WINDOW.title("Odds Calculator")
#WINDOW.geometry("540x480")
WINDOW.columnconfigure(0,weight=1)

FRM_PAD = 10

def PASS(*args):
    pass

class Data:
    def __init__(self, sources=[], callback=PASS, strfmt="{}", frame=WINDOW, row=0, column=0, dtype=float):
        self.value = None
        self.callback = callback
        self.strfmt = strfmt
        self.dtype = dtype
        self.children = []
        self.ent_output = tk.Entry(
            master=frame,
        )
        self.ent_output.grid(row=row, column=column, sticky='e', padx=5)
        self.sources = sources
        for source in self.sources:
            source.register(self)

    def update(self):
        args = [source.get() for source in self.sources]
        val = self.callback(*args)
        self.set(val)
        for child in self.children:
            child.update()

    def register(self, child):
        self.children.append(child)

    def get(self):
        return self.value
    
    def set(self, val):
        if val == None:
            return
        try:
            self.value = self.dtype(val)
            self.ent_output.delete(0, tk.END)
            self.ent_output.insert(0, self.strfmt.format(val))
        except ValueError as e:
            print("Could not cast inputs {} to {}".format(val, str(self.dtype)))

class Table:
    def __init__(self, ):
        self.frame = tk.Frame(
            master=WINDOW,
            relief=tk.FLAT,
            borderwidth=FRM_PAD
        )
        self.frame.grid(row=1, column=0)
        self.frame.columnconfigure(0, weight=1)
        self._nrows = 0
        self._ncols = 0
        self._row_lbls = []
        self._col_lbls = []
        self._cells = []

    def size(self):
        return (self._nrows, self._cols)
    
    def add_row(self, name):
        self._nrows += 1
        self._cells.append([])
        lbl_row = tk.Label(
            master=self.frame,
            text=name
        )
        lbl_row.grid(row=self._nrows, column=0, sticky='w')
        self._row_lbls.append(lbl_row)
    
    def add_column(self, name, sources=[], callback=PASS, strfmt="{}", dtype=float):
        self._ncols += 1
        lbl_col = tk.Label(
            master=self.frame,
            text=name
        )
        lbl_col.grid(row=0, column=self._ncols)
        self._col_lbls.append(lbl_col)
        self.frame.columnconfigure(self._ncols, weight=1)
        if sources == []:
            # empty column
            for i in range(self._nrows):
                self._cells[i].append(0)
        else:
            for i in range(self._nrows):
                def convert(src):
                    return self._cells[i][src] if type(src) == int else src
                tmp_sources = [convert(source) for source in sources]
                cell = Data(
                    sources=tmp_sources,
                    callback=callback,
                    strfmt=strfmt,
                    frame=self.frame,
                    row=i+1,
                    column=self._ncols,
                    dtype=dtype
                )
                self._cells[i].append(cell)
    
    def set_cell(self, row, column, sources=[], callback=PASS, strfmt="{}", dtype=float):
        cell = Data(
            sources=sources,
            callback=callback,
            strfmt=strfmt,
            frame=self.frame,
            row=row+1,
            column=column+1,
            dtype=dtype
        )
        self._cells[row][column] = cell


# input frame
frm_input = tk.Frame(
    master=WINDOW,
    relief=tk.FLAT,
    borderwidth=FRM_PAD
)
frm_input.grid(row=0, column=0, sticky='w')
frm_input.columnconfigure(0, weight=1)
frm_input.columnconfigure(1, weight=1)
# source
lbl_nouts = tk.Label(
    master=frm_input,
    text=u"Num. Outs \u2191\u2193"
)
lbl_nouts.grid(row=0, column=0)
src_nouts = Data(
    frame=frm_input,
    row=0,
    column=1,
    dtype=int
)
lbl_nplayers = tk.Label(
    master=frm_input,
    text=u"Num. Players \u2190\u2192"
)
lbl_nplayers.grid(row=1, column=0, sticky='w')
src_nplayers = Data(
    frame=frm_input,
    row=1,
    column=1,
    dtype=int
)

def pct_odds_nouts(ndraws, nrem):
    return lambda nouts: eq.pct_odds(nouts, ndraws, nrem)

def req_pot_odds(raise_pct):
    def _req_pot_odds(pct, nplayers):
        equity = pct / 100
        raise_frac = raise_pct / 100
        req_pot_frac = (raise_frac / equity) - (1 + nplayers * raise_frac)
        return max(0, req_pot_frac)
    return _req_pot_odds



tbl_output = Table()
tbl_output.add_row("Preflop")
tbl_output.add_row("Flop")
tbl_output.add_row("By River")
tbl_output.add_row("Turn")
tbl_output.add_row("River")
tbl_output.add_column("Out %")
tbl_output.set_cell(
    0, 0,
    sources=[ src_nouts ],
    callback=pct_odds_nouts(5, 50),
    strfmt="{:2.2f}%",
)
tbl_output.set_cell(
    1, 0,
    sources=[ src_nouts ],
    callback=pct_odds_nouts(3, 50),
    strfmt="{:2.2f}%",
)
tbl_output.set_cell(
    2, 0,
    sources=[ src_nouts ],
    callback=pct_odds_nouts(2, 47),
    strfmt="{:2.2f}%",
)
tbl_output.set_cell(
    3, 0, 
    sources=[ src_nouts ],
    callback=pct_odds_nouts(1, 47),
    strfmt="{:2.2f}%",
)
tbl_output.set_cell(
    4, 0,
    sources={ src_nouts },
    callback=pct_odds_nouts(1, 46),
    strfmt="{:2.2f}%",
)

# implied odds columns
def add_implied_odds_req(raise_pct):
    tbl_output.add_column(
        "{}% Raise".format(raise_pct),
        sources=[0, src_nplayers],
        callback=req_pot_odds(raise_pct),
        strfmt="{:.2f} x Pot",
    )
add_implied_odds_req(30)
add_implied_odds_req(50)
add_implied_odds_req(75)
add_implied_odds_req(100)


# refresh
def enter(*args):
    global src_nouts
    src_nouts.update()
WINDOW.bind('<Return>', enter)

# increment nouts
def incr_nouts(*args):
    global src_nouts
    val = src_nouts.get()
    src_nouts.set(val + 1)
    src_nouts.update()
WINDOW.bind('<Up>', incr_nouts)

# decrement nouts
def decr_nouts(*args):
    global src_nouts
    val = src_nouts.get()
    if val == 1:
        val = 2
    src_nouts.set(val - 1)
    src_nouts.update()
WINDOW.bind('<Down>', decr_nouts)

# increment nouts
def incr_nplayers(*args):
    global src_nplayers
    val = src_nplayers.get()
    if val == 9:
        val = 8
    src_nplayers.set(val + 1)
    src_nplayers.update()
WINDOW.bind('<Right>', incr_nplayers)

# decrement nplayers
def decr_nplayers(*args):
    global src_nplayers
    val = src_nplayers.get()
    if val == 2:
        val = 3
    src_nplayers.set(val - 1)
    src_nplayers.update()
WINDOW.bind('<Left>', decr_nplayers)

WINDOW.bind('<Escape>', lambda e: WINDOW.destroy())

src_nouts.set(1)
src_nplayers.set(2)
src_nouts.update()
WINDOW.mainloop()