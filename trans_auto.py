from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import re
import pickle
import pprint as pp

list_frame = 'remote_iframe_350290540'
info_frame = 'remote_iframe_903780713'
books = {
	'Matt': 1,
	'Mark': 2,
	'Luke': 3,
	'John': 4,
	'Acts': 5,
	'Rom': 6,
	'1Cor': 7,
	'2Cor': 8,
	'Gal': 9,
	'Eph': 10,
	'Phil': 11,
	'Col': 12,
	'1Thess': 13,
	'2Thess': 14,
	'1Tim': 15,
	'2Tim': 16,
	'Titus': 17,
	'Phlm': 18,
	'Heb': 19,
	'Jas': 20,
	'1Pet': 21,
	'2Pet': 22,
	'1John': 23,
	'2John': 24,
	'3John': 25,
	'Jude': 26,
	'Rev': 27,
    'Matthew': 1,
	'Mark': 2,
	'Luke': 3,
	'John': 4,
	'Acts': 5,
	'Romans': 6,
	'1st Corinthians': 7,
	'2nd Corinthians': 8,
	'Galatians': 9,
	'Ephesians': 10,
	'Philippians': 11,
	'Colossians': 12,
	'1st Thessalonians': 13,
	'2nd Thessalonians': 14,
	'1st Timothy': 15,
	'2nd Timothy': 16,
	'Titus': 17,
	'Philemon': 18,
	'Hebrews': 19,
	'James': 20,
	'1st Peter': 21,
	'2nd Peter': 22,
	'1st John': 23,
	'2nd John': 24,
	'3rd John': 25,
	'Jude': 26,
	'Revelation': 27,
}

def main():
    driver = webdriver.Chrome()
    dup_dict = {'forward': dict(), 'backward': dict()}
    all_mss = dict()
    get_mss(driver, 1, 10001, 10141, dup_dict, all_mss)
    get_mss(driver, 2, 20001, 20324, dup_dict, all_mss)
    get_mss(driver, 3, 30001, 33018, dup_dict, all_mss)
    get_mss(driver, 4, 40001, 42551, dup_dict, all_mss)
    get_mss(driver, 5, 510001, 520030, dup_dict, all_mss)
    '''get_cntr_mss(driver, dup_dict, all_mss, 1, 2)
    # ID 90056 (T789) appears to be a talisman containing John 11
    # Save dictionaries
    with open(f'dup_dict.pkl','wb') as f:
        pickle.dump(dup_dict, f)
    with open('all_mss.pkl','wb') as f:
        pickle.dump(all_mss, f)'''

def get_cntr_mss(driver, dup_dict, all_mss, first_class, last_class):
    driver.get("https://greekcntr.org/manuscripts/index.htm")
    for i in range(first_class, last_class+1):
        cntr_class(i, driver, dup_dict, all_mss)

def cntr_class(i, driver, dup_dict, all_mss):
    Select(driver.find_element(value='classes')).select_by_value(str(i))
    witnesses = Select(driver.find_element(value='witnesses'))
    for witness in witnesses.options:
        witnesses.select_by_visible_text(witness.accessible_name)
        ms_name = re.sub(r'𝔓', r'P', witness.accessible_name)
        trans_missing = False
        try:
            trans_missing = witness.get_property('style')[0] == 'color'
            print(f'Skipping {ms_name} (no transcription available)')
        except:
            pass
        if not trans_missing:
            driver.switch_to.frame('display')

            # Get name info and see if has a GA number (relevant for things like ostraca)
            aliases = re.sub(r'Aliases: ', '', driver.find_elements(By.CLASS_NAME, 'descr')[0].find_elements(By.TAG_NAME, 'tr')[0].text).split(', ')
            aka = ms_name
            for alias in aliases:
                ga = re.search(r'GA [PO0]\d+', alias)
                if ga is not None:
                    aka = re.search(r'[PO0]\d+', ga.group()).group()
                    break

            # Only get the transcription if we don't have either the transcription or the manuscript
            if all_mss.get(aka) is None:
                # Check to see if it is being referenced by another name (which all_mss will already have)
                possible_parent = dup_dict.get('backward').get(aka)
                if possible_parent is not None:
                    aka = possible_parent
                else:
                    all_mss.update({aka : {'transcription?' : False}})
                    
                    # Get dates when adding new ms
                    years = re.search(r'\d+-\d+', driver.find_elements(By.CLASS_NAME, 'descr')[0].find_elements(By.TAG_NAME, 'tr')[3].text).group().split('-')
                    all_mss.get(aka).update({'yr_start' : int(years[0])})
                    all_mss.get(aka).update({'yr_end' : int(years[1])})

            if all_mss.get(aka).get('transcription?') is False:
                all_mss.get(aka).update({'transcription?' : True})
            
                print(f'Getting {aka}')
                # Format the data
                driver.execute_script('''
                    //replace the verse number with the full title
                    document.querySelectorAll('a').forEach(e => {
                        e.innerText = '~~' + e.title + '~+' //~~ and ~+ are for splitting later
                    })
                                    
                    //add brackets around lacunae
                    document.querySelectorAll('.exp').forEach(e => {
                        e.innerText = '[' + e.innerText + ']'
                    })
                ''')
                
                #get rid of dashes and newlines and extraneous spaces and brackets        
                trans = ''
                for section in driver.find_elements(By.CLASS_NAME, 'trans'):
                    scrub = section.text
                    scrub = re.sub(r'-|—|\n', r'', scrub, flags=re.MULTILINE)
                    scrub = re.sub(r'\[( )*\]', r' ', scrub, flags=re.MULTILINE)
                    scrub = re.sub(r'\]( )*\[', r'', scrub, flags=re.MULTILINE)
                    scrub = re.sub(r' ( +)', r' ', scrub, flags=re.MULTILINE)
                    trans += scrub.lstrip()

                # Split into verses and update dictionary
                vv = trans.split('~~')[1:]
                for v in vv:
                    reftext = v.split('~+')
                    text = reftext[1]
                    ref = reftext[0].split(':')
                    verse = int(ref[-1])
                    bookchap = ref[0].rsplit(' ', 1)
                    chap = int(bookchap[-1])
                    book = books[bookchap[0]]

                    # Somehow add verse to dictionary with its transcription
                    ensure_existence(all_mss.get(aka), book, chap, text, verse, verse+1)
            else:
                print(f'Skipping {aka} (already got transcription)')
            
            driver.switch_to.default_content()

def get_mss(driver, type, lower_bound, upper_bound, dup_dict, all_mss):
    driver.get("https://ntvmr.uni-muenster.de/catalog?docID="+str(type))
    driver.switch_to.frame(list_frame)

    # Wait for mss to load
    table = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "listeTable")))
    table = driver.find_element(value="listeTable")
    mss = table.find_elements(By.TAG_NAME, "tr")
    while len(mss) < 10:
        sleep(0.5)
        mss = table.find_elements(By.CLASS_NAME, "docrow")
    print(f'Found {len(mss)} documents...')

    # For each ms, get its info, and then click on the link and do stuff there
    for ms in mss:
        ms_dict = {'transcription?' : False}
        info = ms.find_elements(By.TAG_NAME, "td")
        id = int(info[0].text)
        if id >= lower_bound and id <= upper_bound:
            # The regex is to handle Weird things in these names: L969DEL, L970DEL, l 2523, l 2525, l 2526, l 2527, l 2528, l 2529, l 2530, l 2531
            entry = re.sub('l ', 'L', re.sub('DEL', '', info[1].accessible_name.strip()))
            ms_name = entry.split(' ')[0]
            
            # For linking duplicates or combined mss:
            # The format is either "Removed; Combined; See: MSNUM"
            #                   or "Removed; Duplicate; See: MSNUM"
            #                   or "Removed; See: CURRMSNUM"
            # Exception cases that are fine: 2560, 2892, L242, L652, L1353, L1398 but they still follow enough of the pattern to regex them consistently
            # !!!!! TODO Other exception cases to manually handle: L355, L1353 !!!!! TODO
            if re.search('Removed', entry) is not None:
                if re.search('Combined', entry) is not None:
                    source_ms = re.search(r'(L|P)?\d+', re.search(r'See: (L|P)?\d+', entry).group()).group()
                    dup_type = 'Combined'
                elif re.search('Duplicate', entry) is not None:
                    source_ms = re.search(r'(L|P|T|O)?(s1-)?\d+', re.search(r'See: (L|P|T|O)?(s1-)?\d+', entry).group()).group()
                    dup_type = 'Duplicate'
                else:
                    pass # for the few extraneous ones that are self-referential
                
                if dup_dict.get('forward').get(source_ms) is None:
                    dup_dict.get('forward').update({source_ms : []})
                curr_dups_at_ms = dup_dict.get('forward').get(source_ms)
                curr_dups_at_ms.extend([(ms_name, dup_type)])
                dup_dict.get('forward').update({source_ms : curr_dups_at_ms})
                dup_dict.get('backward').update({ms_name : source_ms})

            print(ms_name)
            
            # Click ms to get its contents
            info[1].click()
            driver.switch_to.default_content()
            driver.switch_to.frame(info_frame)
            info = driver.find_element(value="content")
            contents = info.find_elements(By.TAG_NAME, "tr")
            while len(contents) < 10:
                contents = info.find_elements(By.TAG_NAME, "tr")
            sleep(0.2)
            p=pp.PrettyPrinter()
            stale = True
            while stale:
                try:
                    toprow = contents[0]
                    ths = toprow.find_elements(By.CLASS_NAME, "fieldValue")
                    linkspot = ths[0]
                    link = linkspot.find_elements(By.TAG_NAME, "a")[0]
                    
                    important_rows = {'Content Overview' : dict(), 'Content' : dict(), 'GMO' : dict()}
                    gmo = 0
                    co = 0
                    c = 0
                    for row in contents:
                        if row.text[:16] == "Content Overview":
                            important_rows.get('Content Overview').update({co : row.find_elements(By.TAG_NAME, 'td')[0].accessible_name})
                            co += 1
                        elif row.text[:7] == "Content":
                            important_rows.get('Content').update({c : row.find_elements(By.TAG_NAME, 'td')[0].accessible_name})
                            c += 1
                        elif row.text[:30] == "General Manuscript Observation":
                            important_rows.get('GMO').update({gmo : row.find_elements(By.TAG_NAME, 'td')[0].accessible_name})
                            gmo += 1

                        # Get year info
                        if row.text.__contains__('Origin Year Early'):
                            ms_dict.update({'yr_start' : max(0, int(row.find_elements(By.TAG_NAME, 'td')[0].accessible_name))})
                        if row.text.__contains__('Origin Year Late'):
                            ms_dict.update({'yr_end' : max(0, int(row.find_elements(By.TAG_NAME, 'td')[0].accessible_name))})


                    contents=pp.pformat(important_rows)
                    with open('contents.txt','a') as f:
                        f.write(contents + '\n')

                    ###It really might be easier to just use NTMSS.sql to get the contents...###

                    
                    # REGEXS to apply to GMO
                    #re.sub(r'( ?\(.*\) ?)|($\.)', '', gmo)             # Remove parenthesized parts and periods at the end of lines
                    #re.match(r'\d?[A-Z] \d', gmo)                      # If true, keep, else discard
                    #book_units = re.split(r'(\d? ?[A-Z])', gmo)        # Split on new book
                    # for book in book_units:
                        #book_name = re.search(r'\d? ?[A-Za-z]+', book)
                        #book_contents = re.sub(r'[A-Za-z ]', '', book, re.M)
                        #chaps = book_contents.split(';')
                        #for chap in chaps:
                            #first

                    # REGEXS to apply to CO

                    # REGEXS to apply to C


                    # TODO Get things like name, data, and contents.
                    

                    # TODO Update dictionary for the manuscript with the range of contents

                    # Click link, get page contents and transcription, and return control
                    '''link.click()'''
                    stale = False
                except Exception as e:
                    contents = info.find_elements(By.TAG_NAME, "tr")
            
            # Get pages and return control to here
            '''get_pages(driver, ms_dict)'''
            driver.switch_to.default_content()
            driver.switch_to.frame(list_frame)

            # Save each dictionary so that progress is saved
            '''with open(f'mss/{ms_name}.pkl','wb') as f:
                pickle.dump(ms_dict, f)'''
            # Update master dictionary
            all_mss.update({ms_name : ms_dict})
    
    print(f'Finished getting all manuscripts of type {type}')

def get_pages(driver, ms_dict):
    driver.switch_to.window(driver.window_handles[1])
    driver.switch_to.frame(list_frame)
    page_table = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.ID, "pagesTable")))
    pages = page_table.find_elements(By.TAG_NAME, "tr")
    while len(pages) == 1:
        try:
            quit = pages[0].text
            if quit == "No results found.\nWe are digitizing manuscripts and registering these in the VMR daily. Community members are indexing, transcribing, and marking features of manuscript pages. You can help. Become an active member of the VMR community and help us build a more complete manuscript repository for biblical studies.":
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                driver.switch_to.frame(list_frame)
                return
            elif re.search('\d', quit):
                break
        except:
            pass
        pages = page_table.find_elements(By.TAG_NAME, "tr")
    pages = page_table.find_elements(By.CLASS_NAME, "pageRow")
    for page in pages:
        id = page.get_attribute("id")
        ms_id = id[3:8]
        page_num = id[12:-4]
        if id[-1] == '0':
            contains = page.find_elements(By.CLASS_NAME, "bibContDisp")[0]
            if contains.text != "No Index Content" and contains.text != '':
                get_trans(driver, ms_id, page_num, contains.text, ms_dict)
    
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.frame(list_frame)

def get_trans(driver, ms_id, page_num, contents, ms_dict):
    # Ensure that each verse of the contents is in this manuscript's dictionary
    contents = re.sub(r'([^\d]):([^\d])', r'\1;\2', contents)
    chunks = re.split(r'[^A-Za-z 0-9\-:]', contents)
    for chunk in chunks:
        if not chunk.__contains__('inscriptio') and not chunk.__contains__('subscriptio'):
            s = chunk.strip().split(' ')
            book = books[s[0]]
            cv = s[1].split(':')
            chap = int(cv[0])
            v_bounds = cv[1].split('-')
            v_st = int(v_bounds[0])
            try:
                v_end = int(v_bounds[1])+1
            except IndexError:
                v_end = v_st

            # Somehow add the content range to the dictionary and initialize the transcription with blanks
            ensure_existence(ms_dict, book, chap, "", v_st, v_end)

    if contents.__contains__("Rev") is False:
        apoc_flag = ""
    else:
        apoc_flag = "&userName=Apokalypse%20Edition"
    # IGNTP flag??

    page = f'https://ntvmr.uni-muenster.de/community/vmr/api/transcript/get/?docID={ms_id}&pageID={page_num}&format=html{apoc_flag}'
    driver.execute_script(f'window.open("{page}")')
    driver.switch_to.window(driver.window_handles[2])

    #Remove unwanted extraneous parts with Javascript
    driver.execute_script('''
        //remove the line numbers, column numbers, folio numbers, and lacuna indicators that contain numbers
        document.querySelectorAll(".linenumber").forEach(e => e.remove());
        document.querySelectorAll(".lac").forEach(e => e.remove());
        document.querySelectorAll(".columnBreak").forEach(e => e.remove());
        document.querySelectorAll(".folioBreak").forEach(e => e.remove());

        //put supplied text in brackets and solve the issue of line breaks in the middle of words
        document.querySelectorAll(".supplied").forEach(e => {e.innerText = "[" + e.innerText + "]"});
        document.querySelectorAll(".nobreak").forEach(e => e.innerText = "~~");

        //remove corrections (ideally put in parens, but not yet)
        document.querySelectorAll(".readings").forEach(e => {
            e.remove()
            //correctors = e.innerText.match(/corrector\d?/g);
            //let corrections = e.innerText.replace(/^\*/,'').split(/corrector\d?/);
            //corrections.reverse();
            //let correctionstr = 'Firsthand: ' + corrections.pop();
            //corrections.reverse();
            //let idx = 0;
            //for (let correction of corrections) {
            //	correctionstr += ", " + correctors[idx][0] + ": " + correction
            //}
            //e.innerText = " (" + correctionstr + ") "
        });

        //remove notes and random other things that clutter up the original page and mess this up otherwise
        document.querySelectorAll(".note").forEach(e => e.remove());
        document.querySelectorAll(".note-marker").forEach(e => e.remove());
        document.querySelectorAll(".app").forEach(e => e.remove());
        document.querySelectorAll(".app-rdgs").forEach(e => e.remove());
        document.querySelectorAll(".verse_number").forEach(e => e.remove());
        
        //Put the full verse reference before each verse using the DOM
        document.querySelectorAll(".verse_marker").forEach(e => {
            padChk = e.dataset.osisid.match(/\./g)
            zeroPad = padChk === null ? ".0.0" : padChk.length === 1 ? ".0" : ""
            e.innerText = e.dataset.osisid + zeroPad;
            e.style.display = 'Block';
        });
    ''')
    
    sections = driver.find_elements(By.CLASS_NAME, "msstrans")
    #parse the verses and format them for insertion into database
    for e in sections:
        regexed = e.get_attribute("innerText")

        #quit here if there isn't a transcription for the desired page
        if re.search('No Transcription Available', regexed, re.IGNORECASE) is not None:
            break

        #if there is a line break in the middle of the word, I previously notated it with ~~, so remove it now
        regexed = re.sub('~~\n', '', regexed, flags=re.MULTILINE)

        # Get all verses and isolate them from each other using my DOM trick from earlier
        vv = re.findall(r'\n\d?\w+\.\d+\.\d+\n', regexed)
        idxx = [regexed.find(v) for v in vv]
        idxx.append(len(regexed))
        vv = [regexed[idxx[i]:idxx[i+1]] for i in range(len(idxx)-1)]

        for v in vv:

            if v == '':
                # This happens on page 1750 of 20001 (INTF's fault)
                with open('errlog.txt','a') as ef:
                    ef.write(f'Issues on page {page_num} of {ms_id} (blank element in list)\n')
                break

            #remove all other line breaks (will be reinserted later)
            v = re.sub('\n', ' ', v, flags=re.MULTILINE)

            #remove any characters that are not Alphanumeric, brackets, parens, spaces, newlines, periods, or Greek
            v = re.sub('[^ςερτυθιοπασδφγηξκλζχψωβνμ\n\[\]\(\) .\w]', '', v, flags=re.MULTILINE)

            #remove duplicate spaces
            v = re.sub('  +', ' ', v, flags=re.MULTILINE)
    
            # Split into reference and text and only keep meaningful references
            ref = re.search(r'\d?\w+\.\d+\.\d+', v).group()
            if re.search('\.0', ref) is None:
                text = re.split(r'\d?\w+\.\d+\.\d+', v)[1].lstrip()

                #remove redundant brackets that used to stop and start around (now removed) newlines
                text = re.sub('\]\[', '', text, flags=re.MULTILINE)

                #Remove indications of commentary
                text = re.sub('\[?comm\]?', '', text, flags=re.MULTILINE)
                text = re.sub(' +', ' ', text, flags=re.MULTILINE)

                # Only keep if there is any text remaining after removing the commentary
                if re.search(r', *$', text) is None:
                    # Get book, chapter, and verse
                    bcv = ref.split('.')
                    
                    # Update the manuscript's dictionary (concatenate always, because it either is blank or has stuff already there)
                    add_verse(books[bcv[0]], int(bcv[1]), int(bcv[2]), text, page_num, ms_dict, contents)

    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    driver.switch_to.frame(list_frame)

def add_verse(book, chap, verse, text, page_num, ms_id, ms_dict, contents):
    try:
        concat = ms_dict.get(book).get(chap).get(verse)
        ms_dict.get(book).get(chap).update({verse : concat + text})
        ms_dict.update({'transcription?' : True})
    except Exception as e:
        # Hits this at page 141 of 10041
        with open('errlog.txt','a') as ef:
            ef.write(f'Issues on page {page_num} of {ms_id} (found {book} {chap}:{verse} in a page purporting to contain {contents}): {e}\n')

def ensure_existence(ms_dict, book, chap, text, v_st, v_end):
    # Ensure book exists
    if ms_dict.get(book) is None:
        ms_dict.update({book : dict()})
    # Ensure chapter exists
    if ms_dict.get(book).get(chap) is None:
        ms_dict.get(book).update({chap : dict()})
    # Add verses
    for v in range(v_st, v_end):
        ms_dict.get(book).get(chap).update({v : text})

if __name__ == "__main__":
    main()