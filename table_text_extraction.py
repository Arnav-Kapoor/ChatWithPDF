import pdfplumber
import pandas as pd
import os
import logging
import torch
from PIL import ImageDraw
import matplotlib.pyplot as plt
import camelot
import tabula
from collections import defaultdict


logging.propagate = False 
logging.getLogger().setLevel(logging.ERROR)


def find_tables(model,image_processor,page_img):
    inputs = image_processor(images=page_img, return_tensors="pt")
    outputs = model(**inputs)
    target_sizes = torch.tensor([page_img.size[::-1]])
    results = image_processor.post_process_object_detection(outputs, threshold=0.9, target_sizes=target_sizes)[0]
    
    return results



def read_tables_text(pdf_path,model,image_processor,pdf,adjustment_factor=5):
    pdfplumber_tables=defaultdict(list)
    camelot_tables=defaultdict(list)
    tabula_tables=defaultdict(list)
    adjustment_factor=adjustment_factor
    extracted_texts=defaultdict(str)

    for j,page in enumerate(pdf.pages):
    # print(j+1)
        page_number=page.page_number
        # print(page_number)
        page_height = float(page.height)
        page_width=float(page.width)
        page_img=page.to_image().original


        results=find_tables(model,image_processor,page_img)
        

        no_table_page=page

        #iterating over all the tables detected
        for i, box in enumerate(results["boxes"]):
            # print(box)
            x0, y0, x1, y1 = box.tolist()

            #pdfplumber
            bbox_pdf = (max(0,x0-adjustment_factor),   max(0,y0-adjustment_factor), min(page_width,x1+adjustment_factor),  min(page_height,y1+adjustment_factor))

            # Crop region
            cropped_page = page.within_bbox(bbox_pdf)
            no_table_page=no_table_page.outside_bbox(bbox_pdf)


            # Extract the table using pdfplumber
            table = cropped_page.extract_table()
            # print(table)
            columns=[]
            empty_col=1
            if table:
                for column in table[0]:
                    if column!=None and len(column)>0:
                        columns.append(column)
                    else:
                        columns.append(f'{empty_col}')
                        empty_col+=1
                # print(columns)
                if len(columns)>0:
                    # print(pd.DataFrame(columns=columns,data=table[1:]))
                    pdfplumber_tables[page_number].append(pd.DataFrame(columns=columns,data=table[1:]))
            # print("pdfplumber done")

            #camelot
            # print(f"{x0-10},{page_height-y0-10},{x1+10},{page_height-y1+10}")
            # print(f"{max(0,x0-adjustment_factor)},{page_height-y0-adjustment_factor},{min(page_width,x1+adjustment_factor)},{page_height-y1+adjustment_factor}")
            try:
                camelot_table = camelot.read_pdf(pdf_path, pages=f"{page_number}",flavor='stream',row_tol=8,table_areas=[f"{max(0,x0-adjustment_factor)},{page_height-y0-adjustment_factor},{min(page_width,x1+adjustment_factor)},{page_height-y1+adjustment_factor}"])
                if len(camelot_table) > 0:
                    camelot_tables[page_number].append(camelot_table[0].df)
            except:
                print("camelot error")
            
            # print("camelot done")

            #tabula
            tabula_table = tabula.read_pdf(
                pdf_path,
                pages=page_number,
                area=[max(0,y0-adjustment_factor),max(0,x0-adjustment_factor),min(page_height,y1+adjustment_factor),min(page_width,x1+adjustment_factor)],       #coordinates in points
                encoding="cp1252",
                stream=True
            )
            tabula_tables[page_number].extend(tabula_table)
            # print("tabula done")

        bbox_footer = (0,   no_table_page.height*0.90 , no_table_page.width ,  no_table_page.height)
        no_table_page=no_table_page.outside_bbox(bbox_footer)
        extracted_text=no_table_page.extract_text()

        # print(extracted_text)  
        extracted_texts[page_number]=extracted_text


    return pdfplumber_tables,camelot_tables,tabula_tables,extracted_texts
