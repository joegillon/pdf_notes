import os
from tkinter import *
import fitz


def get_pdf_files(folder):
    pdfs = []
    for entry in os.listdir(folder):
        if os.path.isfile(entry):
            parts = entry.split('.')
            if parts[1].lower() == 'pdf':
                pdfs.append(entry)

    return pdfs


def do_file(pdf):
    parts = pdf.split('.')
    rpt_name = '%s_notes.txt' % parts[0]
    with open(rpt_name, 'w') as rpt:
        abs_path = '%s\n\n' % os.path.abspath(pdf)
        rpt.write(abs_path)

        try:
            # Pycharm can't see fitz.open
            # noinspection PyUnresolvedReferences
            doc = fitz.open(pdf)
        except:
            msg = '%s is not a PDF!' % abs_path
            rpt_box.insert(END, msg)
            return

        for page in doc:
            notes = []
            if not page.first_annot:
                continue
            annot = page.first_annot
            while annot:
                if annot.type[1] == 'Highlight':
                    words = page.get_text('words')
                    mywords = [w for w in words if fitz.Rect(w[:4]).intersect(annot.rect)]
                    notes.append(' '.join([w[4] for w in mywords]))
                elif annot.type[1] == 'Text':
                    notes.append(annot.info['content'])
                annot = annot.next

            rpt.write('\nPage %d\n' % page.number)
            for note in notes:
                rpt.write('\n%s\n' % note)

        msg = '%s -> %s' % (abs_path, rpt_name)
        rpt_box.insert(END, msg)


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master


def define_window():
    window = Tk()
    window.title('PDF Notes')
    window.geometry('500x600+50+50')

    toolbar = Frame(window)
    toolbar.pack(side=TOP, fill=X)

    dir_button = Button(
        toolbar,
        relief=FLAT,
        compound=LEFT,
        text="Folder",
        command=do_folder,
        image=None
    )
    dir_button.pack(side=LEFT, padx=0, pady=0)

    file_button = Button(
        toolbar,
        text="File(s)",
        compound=LEFT,
        command=do_files,
        relief=FLAT,
        image=None
    )
    file_button.pack(side=LEFT, padx=0, pady=0)

    return window


def show_done():
    import tkinter.messagebox

    tkinter.messagebox.showinfo('Woohoo!', 'Done!')


def do_folder():
    from tkinter.filedialog import askdirectory

    pdf_dir = askdirectory()
    if pdf_dir:
        pdf_files = get_pdf_files(pdf_dir)
        if pdf_files:
            for f in pdf_files:
                do_file('%s/%s' % (pdf_dir, f))

            show_done()


def do_files():
    from tkinter.filedialog import askopenfilenames

    pdf_files = askopenfilenames()
    if pdf_files:
        for f in pdf_files:
            do_file(f)

        show_done()


if __name__ == '__main__':

    root = define_window()

    rpt_box = Listbox(root, height=500, width=600)
    rpt_box.pack(side=LEFT, fill=BOTH)

    app = Window(root)
    root.mainloop()
