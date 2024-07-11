import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import pandas as pd
import pytesseract
# import dataparser
import re
import dateparser
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract-ocr-w64-setup-v5.0.0-alpha.20210506.exe"  # Update path as needed


def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def extract_text_from_pdf(pdf_path):
    pages = convert_from_path(pdf_path)
    text = ""
    for page in pages:
        text += pytesseract.image_to_string(page)
    return text

def process_document(file_path):
    if file_path.endswith(('.jpg', '.jpeg', '.png')):
        text = extract_text_from_image(file_path)
    elif file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    else:
        raise ValueError("Unsupported file format")
    return text



def extract_info(resume_text):
    print('========')
    print(resume_text)

    work_exp_regex = r'((\d{2}/\d{4} to \d{2}/\d{4})|Current)\s*(.*?)\s*(Company Name.*?)\s*(City, State)(.*?)\n'
    education_regex = r'Education\s*([\s\S]*?)\s*Skills'
    skills_regex =r'Skills\s*([\w\s,.-]+)'

    work_experiences = re.findall(work_exp_regex, resume_text)
    work_experience_list = []
    
    for experience in work_experiences:
        work_experience_list.append({
            'duration': experience[0],
            'job_title': experience[1],
            'company': experience[2],
            'location': experience[3]
        })

    
    educations = re.findall(education_regex, resume_text)
    
    education_list = []
    for education in educations:
        duration_regex = r'(January|February|March|April|May|June|July|August|September|October|November|December)\s\d{4}.*'
        # print(education)
        duration = re.findall(duration_regex, education)

        education_list.append({
            'date': education[0],
            'description': education[2],
            
        })

    
    skills = re.findall(skills_regex, resume_text)
    skill_list = []
    for skill in skills:
        skill_list.append(skill)

    
    return {
        'work_experience': work_experience_list,
        'education': education_list,
        'skills': skill_list
    }




def extract_work_experience(text):
    

    
    print(text)
  
    # summary_regex = re.search(r"Summary\n([\s\S]*?)\nHighlights", text)
    summary_match = re.search(r"Summary\n([\s\S]*?)\nHighlights", text)
    summary = summary_match.group(1).strip()
    # print('This is summary :', summary)

    # Extract highlights
    highlights_regex = r"Highlights\n(.*?)\nAccomplishments"
    highlights_match = re.search(highlights_regex, text, re.DOTALL)
    highlights = [line.strip() for line in highlights_match.group(1).splitlines()]

    # Extract accomplishments
    accomplishments_regex = r"Accomplishments\n(.*?)\nExperience"
    accomplishments_match = re.search(accomplishments_regex, text, re.DOTALL)
    accomplishments = []
    for line in accomplishments_match.group(1).splitlines():
        if line.strip():
            accomplishments.append(line.strip())

    # Extract experience
    experience_regex = r"Experience\n(.*?)\Z"
    experience_match = re.search(experience_regex, text, re.DOTALL)
    experience = []
    company = 'Company'
    job_title = 'Title'
    # for block in experience_match.group(1).split("\n\n")
    block = experience_match.group(1)
        

    company_regex = r"Company Name (.*?)\n"
    job_title_regex = r"(.*?)\nCity, State\n"
    dates_regex = r"(.*?) to (.*?)\n"
    description_regex = r"(.*)"
    
    company_match = re.search(company_regex, block)
    job_title_match = re.search(job_title_regex, block)
    dates_match = re.search(dates_regex, block)
    description_match = re.search(description_regex, block, re.DOTALL)
    if company_match:
        company = company_match.group(1).strip()
    
    if job_title_match:
        job_title = job_title_match.group(1).strip()
    if dates_match:
        start_date = dates_match.group(1).strip()
        end_date = dates_match.group(2).strip()
    # if description_match:
    #     description = description_match.group(1).strip()
        
    experience.append({
        "company": company,
        "job_title": job_title,
        "start_date": start_date,
        "end_date": end_date,
        "description": "description"
    })

    # Create data model
    data_model = {
        "summary": summary,
        "highlights": highlights,
        "accomplishments": accomplishments,
        "experience": experience
    }

    print(data_model)
    return data_model



def bulk_extraction(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith('.pdf') or file.endswith('.jpg'):
            file_path = os.path.join(folder_path, file)
            main(file_path)


def main(document_path):
    
    extracted_text = process_document(document_path) 
    # print("Extracted Text:")
    # print(type(extracted_text))

    
    info = extract_work_experience(extracted_text)
    
    print('=============================================================================')
    for section, item in info.items():
        print(section, item)
        print('--------------------------------------------------------------------------')

if __name__ == "__main__":
    document_path = r"archive\data\data\ACCOUNTANT\10554236.pdf"  # Giving relative path to document here
    main(document_path)

    """For bulk extraction in a folder"""
    # folder_path = r"archive\data\data\ACCOUNTANT"
    # bulk_extraction(folder_path)
    
