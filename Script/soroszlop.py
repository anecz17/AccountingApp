import openpyxl

# Load the Excel workbook
wb = openpyxl.load_workbook('D:\ApaLusta\ExcelSorbólOszlop\elista_20240926_1419.xlsx')

# Select the active worksheet (or specify the sheet name)
source_ws = wb["Munka1"]  # or wb['SheetName']
target_ws = wb['Munka2']  # Replace with your target sheet name

# Step 1: Copy data from a specific cell (or range) in the source worksheet
#source_value = source_ws['A1'].value  # Example: Copy from cell A1 in source sheet

# Step 2: Write the data to a specific cell in the target worksheet
#target_ws['B2'].value = source_value  # Example: Write to cell B2 in target sheet

# Optional: You can copy entire ranges or loops through multiple cells if needed

alap = 5
sor = 0
for sor in range(1805):
    
    # Ennyi oszlop van/kell
    for oszlop, jelen in zip([chr(i) for i in range(ord('A'), ord('G'))], range(6)):
        target_ws[oszlop + str(sor + 1)].value = source_ws['B' + str(alap+sor*6+jelen)].value
        
    for oszlop, jelen in zip([chr(i) for i in range(ord('G'), ord('M'))], range(6)):
        target_ws[oszlop + str(sor + 1)].value = source_ws['D' + str(alap+sor*6+jelen)].value

    jelen = 0
    for oszlop in [chr(i) for i in range(ord('M'), ord('R'))]:
        target_ws[oszlop + str(sor + 1)].value = source_ws['F' + str(alap+sor*6+jelen)].value
        jelen += 1

    oszlop = 'R'        
    jelen -= 1
    target_ws[oszlop + str(sor + 1)].value = source_ws['G' + str(alap+sor*6+jelen)].value
    oszlop = 'S'
    jelen += 1
    target_ws[oszlop + str(sor + 1)].value = source_ws['F' + str(alap+sor*6+jelen)].value
    oszlop = 'T'
    target_ws[oszlop + str(sor + 1)].value = source_ws['G' + str(alap+sor*6+jelen)].value
    
    oszlop = 'U'
    target_ws[oszlop + str(sor + 1)].value = source_ws['I' + str(alap+sor*6+jelen)].value
    oszlop = 'V'
    target_ws[oszlop + str(sor + 1)].value = source_ws['J' + str(alap+sor*6+jelen)].value
    
    oszlop = 'W'
    target_ws[oszlop + str(sor + 1)].value = source_ws['L' + str(alap+sor*6+jelen)].value
    oszlop = 'X'
    target_ws[oszlop + str(sor + 1)].value = source_ws['M' + str(alap+sor*6+jelen)].value
    oszlop = 'Y'
    target_ws[oszlop + str(sor + 1)].value = source_ws['N' + str(alap+sor*6+jelen)].value
    

"""     for oszlop, jelen in zip([chr(i) for i in range(ord('W'), ord('Z'))], range(3)):
        target_ws[oszlop + str(sor + 1)].value = source_ws['B' + str(alap+sor*6+jelen)].value """

#formátum: éééé.hh.nn

# Step 3: Save the workbook after copying
wb.save('ExcelSorbólOszlop/teszt.xlsx')