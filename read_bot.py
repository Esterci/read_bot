from io import StringIO
from os import read
import argparse


class ProgBar:

    def __init__(self, n_elements,int_str):
        
        import sys

        self.n_elements = n_elements
        self.progress = 0

        print(int_str)

        # initiallizing progress bar

        info = '{:.2f}% - {:d} of {:d}'.format(0,0,n_elements)

        formated_bar = ' '*int(50)

        sys.stdout.write("\r")

        sys.stdout.write('[%s] %s' % (formated_bar,info))

        sys.stdout.flush()

    def update(self,prog_info=None):
        
        import sys

        if prog_info == None:

            self.progress += 1

            percent = (self.progress)/self.n_elements * 100 / 2

            info = '{:.2f}% - {:d} of {:d}'.format(percent*2,self.progress,self.n_elements)

            formated_bar = '-'* int (percent) + ' '*int(50-percent)

            sys.stdout.write("\r")

            sys.stdout.write('[%s] %s' % (formated_bar,info))

            sys.stdout.flush()


        else:

            self.progress += 1

            percent = (self.progress)/self.n_elements * 100 / 2

            info = '{:.2f}% - {:d} of {:d} '.format(percent*2,self.progress,self.n_elements) + prog_info

            formated_bar = '-'* int (percent) + ' '*int(50-percent)

            sys.stdout.write("\r")

            sys.stdout.write('[%s] %s' % (formated_bar,info))

            sys.stdout.flush()


class PDF_miner:

    def __init__(self,file):

        import PyPDF2

        self.file = file

        reader = PyPDF2.PdfFileReader(file)

        self.reader = PyPDF2.PdfFileReader(file)

        self.pdf_n_pages = reader.numPages

        self.pic_ref_list = []

        self.discart_list = []


    def convert_pdf_to_string(self):

        from io import StringIO
        from pdfminer.converter import TextConverter
        from pdfminer.layout import LAParams
        from pdfminer.pdfdocument import PDFDocument
        from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
        from pdfminer.pdfpage import PDFPage
        from pdfminer.pdfparser import PDFParser


        output_string = StringIO()
        with open('transition.pdf', 'rb') as in_file:
            parser = PDFParser(in_file)
            doc = PDFDocument(parser)
            rsrcmgr = PDFResourceManager()
            device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            for page in PDFPage.create_pages(doc):
                interpreter.process_page(page)

        return(output_string.getvalue())


    def add_line(self,line,out):

        # Open the file in append & read mode ('a+')

        with open(out, "a+") as file_object:

            # Move read cursor to the start of file.
            file_object.seek(0)

            # If file is not empty then append '\n'
            data = file_object.read(100)

            if len(data) > 0 :
                file_object.write("\n")
                
            # Append text at the end of file
            file_object.write(line)

    
    def get_text(self,pg):

        import PyPDF2

        writer = PyPDF2.PdfFileWriter()

        output_filename = 'transition.pdf'

        page = self.reader.getPage(pg)

        writer.addPage(page)

        with open(output_filename, 'wb') as output:
            writer.write(output)

        del writer

        text = self.convert_pdf_to_string()

        # formating text
        text = text.replace('\x0c',' ')

        # breaking lines
        text = text.split('\n')

        return text



    def extract_figures(self):

        import fitz
        import glob
        
        # opening pdf file

        self.doc = fitz.open(self.file)

        figures_list = glob.glob(self.file)

        # Initializing progress bar

        bar = ProgBar(self.pdf_n_pages,'\nExtracting Figures...')

        for pg in range(self.pdf_n_pages):

            for img in self.doc.get_page_images(pg):
                
                # get figure refferance
                
                xref = img[0]
                
                # build figure bitmap

                pix = fitz.Pixmap(self.doc, xref)

                # defines the name of the picture

                file_name = "%s.png" % (xref)

                # if the figure does not exists save it

                if not file_name in figures_list:

                    if pix.n < 5:       # this is GRAY or RGB
                        pix.save("figures/"+file_name)
                    else:               # CMYK: convert to RGB first
                        pix1 = fitz.Pixmap(fitz.csRGB, pix)
                        pix1.save("figures/"+file_name)
                        pix1 = None
                    pix = None

            bar.update()

        print("\n")


    def convert(self):

        self.pages_struct = {}

        self.extract_figures()

        # Initializing progress bar

        bar = ProgBar(self.pdf_n_pages,'Converting PDF to LaTex...')

        for pg in range(self.pdf_n_pages):

            self.pages_struct[pg] = {}

            self.pages_struct[pg]['text'] = self.get_text(pg)

            bar.update()


    def save(self):

        ### Saving results in a txt file 

        # initializing progress bar

        bar = ProgBar(len(self.pages_struct),"\n\nSalving conversion...")

        for pg in self.pages_struct:
            
            # appending text

            for txt in self.pages_struct[pg]['text']:
                self.add_line(txt,"conv.txt")

            bar.update()

        print('\n')
  
parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()


parser.add_argument('-f','--file', action='store',
        dest='file', required = True,
            help = "The file to perform the conversion.")


args = parser.parse_args()

file = args.file

print("Starting bot ...")
print("="*80)
        

# initializing class

converter = PDF_miner(file)

# converting information

converter.convert()

# saving results


converter.save()

print("="*80)
print("Bot has finished ;D")