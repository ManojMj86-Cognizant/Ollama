'''
-- This does not work for pdfs having multiple columns and images.-----------
from pypdf import PdfReader  # pip install pypdf4
# def extract_text_from_pdf(pdf_path):
#     reader = PdfReader(pdf_path)
#     text = ""
#     for page in reader.pages:
#         text += page.extract_text() or "" # handle pages with no text
#     return text
# print(extract_text_from_pdf(pdf_path))
'''
from pdfminer.high_level import extract_text # pip install pdfminer.six
pdf_path = "./documents/2630782_coventry-building-society-achieves-operational-resiliency-with-aws-migration_singlepage.pdf"
def extract_text_from_pdf_pdfminer(pdf_path):
    try:
        text = extract_text(pdf_path)
        return text
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None
    
# Count the number of lines in the extracted text
print(f"Number of lines: {extract_text_from_pdf_pdfminer(pdf_path).count("\n")} lines") 
# Count the number of words in the extracted text
print(f"Word count in the file: {extract_text_from_pdf_pdfminer(pdf_path).count(" ")} words") 
# Print the extracted text
print(f"\n {extract_text_from_pdf_pdfminer(pdf_path)}")

