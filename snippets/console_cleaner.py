#!/usr/bin/env python3

from tkinter import *
from tkinter import ttk

import re

RE_CALLOUT = re.compile(r'<\d+>')

class ConsoleCleaner(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        self.after(1, lambda:self.text.focus())

    def create_widgets(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        btn = ttk.Button(self, text='Clean', command=self.clean)
        btn.grid(row=0, column=0, sticky='ew')

        self.text = Text(self)
        self.text.grid(row=1, column=0, sticky='nesw')

        vertical_scroller = Scrollbar(self, orient='vertical')
        vertical_scroller.grid(row=1, column=1, sticky='ns')
        horizontal_scroller = Scrollbar(self, orient='horizontal')
        horizontal_scroller.grid(row=2, column=0, sticky='ew')

    def clean(self):
        clean_text = []
        for line in self.text.get('1.0', 'end').split('\n'):
            line = line.strip()
            if line.startswith('>>> ') or line.startswith('... '):
                line = line[4:]
            else:
                continue
            line = re.sub(RE_CALLOUT, '', line)
            line = line.rstrip()
            line = line.rstrip('#')
            line = line.rstrip()
            clean_text.append(line)

        self.text.delete('1.0', 'end')
        self.text.insert('1.0', '\n'.join(clean_text))
        self.text.focus()
        self.text.tag_add(SEL, "1.0", END)
        self.text.mark_set(INSERT, "1.0")
        self.text.see(INSERT)


app = ConsoleCleaner()
app.mainloop()
