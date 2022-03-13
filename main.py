import os

def grab_text_from_image(file):
    import pytesseract as pt
    '''grab the text from the image'''
    pt.pytesseract.tesseract_cmd = r'ignore-tesseract\tesseract.exe'
    # Grab the text from the image
    text = pt.image_to_string(file)
    return text


def grab_all_files(path):
    """
    This function will grab all the files in the directory
    """
    import glob
    # Grab all the files in the directory
    files = glob.glob(path + '*')
    return files

def return_nhs_num(files):
    '''search the file for the NHS number'''
    '''if named directory is not found create it'''
    if not os.path.exists('named'):
        os.makedirs('named')
    if not os.path.exists('unnamed'):
        os.makedirs('unnamed')
    if not os.path.exists('failed'):
        os.makedirs('failed')
    import re
    # Loop through the files
    for file in files:
        # Open the file
        text = grab_text_from_image(file)
        # Read the file
        # Search for the NHS number
        #use re to find the NHS number in form NHS {letters} 1111111111 with or without dots
        #regex = re.compile(r'NHS\s\w{2}\s\d{10}')
        nhs_num = re.search(r'NHS No.\s\d{10}', text)

        if not nhs_num:
            nhs_num = re.search(r'NHS No.\s\d{3} \d{3} \d{4}', text)
            if not nhs_num:
                nhs_num = re.search(r'NHS\s\w{2}\s\d{10}', text)
                if not nhs_num:
                    nhs_num = re.search(r'\s\d{3} \d{3} \d{4}\s', text)
                    if not nhs_num:
                        nhs_num = re.search(r'NHS No\s\d{3} \d{3} \d{4}', text)
                        if not nhs_num:
                            nhs_num = re.search(r'NHS No\s\d{10}', text)
                            if not nhs_num:
                                #use re to find nhs num in form NHS Number: 1111111111
                                nhs_num = re.search(r'NHS Number:\s\d{10}', text)
                #if not nhs_num:
                    #nhs_num = re.search(r'\d{10}', text)
                    #if '01296' in str(nhs_num.group()):
                    #    nhs_num = None
        # If the NHS number is found, add it to the list
        if nhs_num:
            nhs_num = nhs_num.group().strip('\n').strip('NHS No.').strip('NHS').strip('NHS No').strip('NHS No').strip('NHS Number:').strip('no').strip('NHSno')
            print(nhs_num)
            #move the file into new directory and rename it to the NHS number using
            os.rename(file, f'named/{nhs_num.replace(" ","")}---FILE={file.replace("unnamed","")[1:]}')
        else:
            # If the NHS number is not found, move the file into the failed directory
            print('NHS number not found',file)
            os.rename(file, f'failed/{file.replace("unnamed","")[1:]}')



if __name__ == '__main__':
    try:
        files = grab_all_files('unnamed/')
        return_nhs_num(files)
    except Exception as e:
        print(e)
        input('Press enter to exit')
