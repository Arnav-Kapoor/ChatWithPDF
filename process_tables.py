import pdfplumber
import pandas as pd
import numpy as np
import camelot
import tabula
from collections import defaultdict
import re


def number_of_valid_cells(table):
    values=table.values.reshape(1,-1)[0]

    return table.shape[0]*table.shape[1]-pd.isna(values).sum() #total cells-invalid cells


def process_columns(table,plumber_table):
    cols=table.columns.tolist()
    # check if columns from plumber are present or not, if plumber did not generate any table then pick the first row 
    is_valid=False
    tries=-1
    pattern = re.compile(r'^(?![\d,.\s]+$).+')
    plumber_cols=plumber_table.columns.tolist()

    is_plumber_valid=False
    for plumber_col in plumber_cols:
        if bool(pattern.match(plumber_col)):
            is_plumber_valid=True
            break
    
    # print(is_plumber_valid)

    if not plumber_table.empty and is_plumber_valid:
        for plumber_col in plumber_table.columns.tolist():
            if tries<=3 and plumber_col in cols:
                is_valid=True
                break
            else:
                if tries+1<len(table):
                    cols=list(table.iloc[tries+1].values)
                    tries+=1
        
        if is_valid:
            if tries>=0:
                table.columns=list(table.iloc[tries].values)
                table.drop(index=tries,inplace=True)

        else:
            nums=0
            for col in cols:
                if type(col)==str and "Unnamed" not in col:
                    nums+=1
            # print(nums)
            if nums==0:
                table.columns=list(table.iloc[0].values)
                table.drop(index=0,inplace=True)
    else:
        table.columns=list(table.iloc[0].values)
        table.drop(index=0,inplace=True)
    
    return table

def preprocessing(pdfplumber_tables,camelot_tables,tabula_tables):
    all_pages=list(set(list(pdfplumber_tables.keys())+list(tabula_tables.keys())+list(camelot_tables.keys())))
    all_pages.sort()

    final_tables=defaultdict(list)
    for page in all_pages:
        # print(page)
        pdfplumber_pages=pdfplumber_tables.get(page,[])
        camelot_pages=camelot_tables.get(page,[])
        tabula_pages=tabula_tables.get(page,[])

        max_tables=max(len(pdfplumber_pages),len(camelot_pages),len(tabula_pages))

        for i in range(max_tables):
            try:
                pdfplumber_page=pdfplumber_pages[i]
            except:
                pdfplumber_page=pd.DataFrame()
            
            try:
                camelot_page=camelot_pages[i]
            except:
                camelot_page=pd.DataFrame()
            
            try:
                tabula_page=tabula_pages[i]
            except:
                tabula_page=pd.DataFrame()


            plumber_valids,camelot_valids,tabula_valids=0,0,0
            final_table=pd.DataFrame()

            # print("plumber",pdfplumber_page,"\n","camelot",camelot_page,"\n","tabula",tabula_page)

            if not pdfplumber_page.empty:
                plumber_valids=number_of_valid_cells(pdfplumber_page)
                
            
            if not camelot_page.empty:
                camelot_valids=number_of_valid_cells(camelot_page)
                

            if not tabula_page.empty:
                tabula_valids=number_of_valid_cells(tabula_page)
            

            ## Process columns 
            if tabula_valids>camelot_valids:
                if tabula_valids>plumber_valids:
                    #process columns for tabula
                    final_table=process_columns(tabula_page.copy(),pdfplumber_page.copy())
                    
                elif tabula_valids<plumber_valids:
                    #process columns for plumber
                    final_table=process_columns(pdfplumber_page.copy(),pdfplumber_page.copy())
                    
                else:
                    #equal case prefer tabula
                    final_table=process_columns(tabula_page.copy(),pdfplumber_page.copy())

            elif tabula_valids<camelot_valids:
                if camelot_valids>plumber_valids:
                    #process columns for camelot
                    # print(camelot_page)
                    final_table=process_columns(camelot_page.copy(),pdfplumber_page.copy())
                    
                elif camelot_valids<plumber_valids:
                    #process columns for plumber
                    final_table=process_columns(pdfplumber_page.copy(),pdfplumber_page.copy())
            
                else:
                    #equal case prefer camelot
                    final_table=process_columns(camelot_page.copy(),pdfplumber_page.copy())
                
            else:
                #equal case
                if tabula_valids<plumber_valids:
                    #process columns for plumber
                    final_table=process_columns(pdfplumber_page.copy(),pdfplumber_page.copy())
                
                else:
                    #process columns for tabula
                    final_table=process_columns(tabula_page.copy(),pdfplumber_page.copy())
                    
            final_tables[page].append(final_table)
    
    return final_tables