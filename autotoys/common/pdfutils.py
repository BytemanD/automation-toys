
def merge(pdf_list, output=None):
    from PyPDF2 import PdfFileReader, PdfFileWriter         # noqa

    output = output or 'merged.pdf'
    pdf_writer = PdfFileWriter()
    for pdf_file in pdf_list:
        pdf_reader = PdfFileReader(pdf_file)
        for num in range(pdf_reader.getNumPages()):
            # page = pdf_reader.getPage(num)
            pdf_writer.addPage(pdf_reader.getPage(num))
    with open('merged.pdf', 'wb') as merged_file:
        pdf_writer.write(merged_file)
