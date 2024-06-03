import re
from pdfquery import PDFQuery
from pdfminer.high_level import extract_pages, extract_text


def extract_information_from_pdf(pdf_path):
    pdf = PDFQuery(pdf_path)
    pdf.load()

    # Use CSS-like selectors to locate the elements
    text_elements = pdf.pq('LTTextLineHorizontal')

    # Extract the text from the elements
    text = [t.text for t in text_elements]

    # Join all text elements into a single string for easier searching
    full_text = " ".join(text)

    # Extract numerical figures
    figures = re.findall(r'\b\d+\.?\d*\b', full_text)

    return {
        "full_text": full_text,
        "figures": figures
    }


def answer_question(extracted_info, question):
    # Convert the question to lowercase to make the search case insensitive
    question = question.lower()

    # Search for the keyword in the full text
    keyword_results = re.findall(r'\b' + re.escape(question) + r'\b', extracted_info["full_text"], re.IGNORECASE)

    # Search for figures if the question indicates numerical data
    if "figure" in question or "number" in question:
        figures = extracted_info["figures"]
    else:
        figures = []

    # Combine results
    if keyword_results or figures:
        return {
            "keyword_results": keyword_results,
            "figures": figures
        }
    else:
        return "The specified keyword or figure was not found in the document."


if __name__ == "__main__":
    pdf_path = 'ART20203995.pdf'  # Replace with your actual PDF path
    extracted_info = extract_information_from_pdf(pdf_path)

    # Print extracted information for debugging
    print("Full Text Extracted:", extracted_info["full_text"][:500])  # Print first 500 characters for brevity
    print("Extracted Figures:", extracted_info["figures"])

    # Get user question and answer it
    user_question = input("Enter your question: ")
    answer = answer_question(extracted_info, user_question)
    print("Answer:", answer)

# def extract_text_from_pdf(pdf_path):
#     pdf = PDFQuery(pdf_path)
#     pdf.load()
#
#     # Use CSS-like selectors to locate the elements
#     text_elements = pdf.pq('LTTextLineHorizontal')
#
#     # Extract the text from the elements
#     text = [t.text for t in text_elements]
#
#     # Join all text elements into a single string for easier searching
#     full_text = " ".join(text)
#
#     return full_text
#
#
# def extract_names_from_text(text):
#     # Define a regular expression pattern to find names
#     pattern = re.compile(r'\b[A-Z][a-z]*\s[A-Z][a-z]*\b')
#
#     # Find all matches in the text
#     matches = pattern.findall(text)
#
#     return matches
#
#
# if __name__ == "__main__":
#     pdf_path = 'Health_and_Safety_Coordinator_Resume.pdf'
#
#     # Extract text from the PDF
#     text = extract_text_from_pdf(pdf_path)
#     print("Extracted Text:", text[:500])  # Print first 500 characters for brevity
#
#     # Extract names from the text
#     names = extract_names_from_text(text)
#     print("Extracted Names:", names)
