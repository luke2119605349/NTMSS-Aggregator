from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException as Stale
from time import sleep
from traceback import print_exc
import pickle
import re

# The INTF uses these different iFrame IDs throughout
list_frame = 'remote_iframe_350290540'
info_frame = 'remote_iframe_903780713'

# Structure containing various forms of book names associated with their number
books = {
    'Mt': 1, 'Matt': 1, 'Matthew': 1,
    'Mc': 2, 'Mk': 2, 'Mark': 2,
    'L': 3, 'Lk': 3, 'Luke': 3,
    'J': 4, 'Jn': 4, 'John': 4,
    'Ac': 5, 'Act': 5, 'Acts': 5,
    'R': 6, 'Rom': 6, 'Romans': 6,
    '1K': 7, '1 K': 7, '1Cor': 7, '1 Cor': 7, '1st Corinthians': 7,
    '2K': 8, '2 K': 8, '2Cor': 8, '2 Cor': 8, '2nd Corinthians': 8,
    'G': 9,	'Gal': 9, 'Galatians': 9,
    'E': 10, 'Eph': 10, 'Ephesians': 10,
    'Ph': 11, 'Phil': 11, 'Philippians': 11,
    'Kol': 12, 'Col': 12, 'Colossians': 12,
    '1Th': 13, '1 Th': 13, '1Thess': 13, '1 Thess': 13, '1st Thessalonians': 13,
    '2Th': 14, '2 Th': 14, '2Thess': 14, '2 Thess': 14, '2nd Thessalonians': 14,
    '1T': 15, '1 T': 15, '1Tim': 15, '1 Tim': 15, '1st Timothy': 15,
    '2T': 16, '2 T': 16, '2Tim': 16, '2 Tim': 16, '2nd Timothy': 16,
    'Tt': 17, 'Titus': 17,
    'Phm': 18, 'Phlm': 18, 'Philemon': 18,
    'H': 19, 'Heb': 19, 'Hebrews': 19,
    'Jc': 20, 'Jas': 20, 'James': 20,
    '1P': 21, '1 P': 21, '1Pet': 21, '1 Pet': 21, '1st Peter': 21,
    '2P': 22, '2 P': 22, '2Pet': 22, '2 Pet': 22, '2nd Peter': 22,
    '1J': 23, '1 J': 23, '1John': 23, '1 John': 23, '1st John': 23,
    '2J': 24, '2 J': 24, '2John': 24, '2 John': 24, '2nd John': 24,
    '3J': 25, '3 J': 25, '3John': 25, '3 John': 25, '3rd John': 25,
    'Jd': 26, 'Jude': 26,
    'Ap': 27, 'Rev': 27, 'Revelation': 27,
}

# Structure containing the number of verses in each chapter
# #NOTE 3 John has 15 here but 14 in the TR, and 2 Cor 13 has 13 here but 14 in the TR
chap_verses = [
    [25,23,17,25,48,34,29,34,38,42,30,50,58,36,39,28,27,35,30,34,46,46,39,51,46,75,66,20],
    [45,28,35,41,43,56,37,38,50,52,33,44,37,72,47,20],
    [80,52,38,44,39,49,50,56,62,42,54,59,35,35,32,31,37,43,48,47,38,71,56,53],
    [51,25,36,54,47,71,53,59,41,42,57,50,38,31,27,33,26,40,42,31,25],
    [26,47,26,37,42,15,60,40,43,48,30,25,52,28,41,40,34,28,41,38,40,30,35,27,27,32,44,31],
    [32,29,31,25,21,23,25,39,33,21,36,21,14,23,33,27],
    [31,16,23,21,13,20,40,13,27,33,34,31,13,40,58,24],
    [24,17,18,18,21,18,16,24,15,18,33,21,13],
    [24,21,29,31,26,18],
    [23,22,21,32,33,24],
    [30,30,21,23],
    [29,23,25,18],
    [10,20,13,18,28],
    [12,17,18],
    [20,15,16,16,25,21],
    [18,26,17,22],
    [16,15,15],
    [25],
    [14,18,19,16,14,20,28,13,28,39,40,29,25],
    [27,26,18,17,20],
    [25,25,22,19,14],
    [21,22,18],
    [10,29,24,21,21],
    [13],
    [15],
    [25],
    [20,29,22,11,14,17,17,13,21,11,19,17,18,20,8,21,18,24,21,15,27,21]
]

# Get the number of verses in a given chapter in a given book
def get_v_ct(book, chap):
    return chap_verses[book-1][chap-1]

# Get the number of chapters in a given book
def get_chap_ct(book):
    return len(chap_verses[book-1])

# This is the master function that gets all the ms data (mss, date ranges, contents, transcriptions, duplicates, page numbers, duplicate information) from the NTVMR and CNTR
def gather_data():
    driver = webdriver.Chrome()
    dup_dict = {'forward': dict(), 'backward': dict()}
    all_mss = dict()
    ed_mss = dict()
    # get_mss(driver, 1, 10001, 10141, dup_dict, all_mss, ed_mss)
    # get_mss(driver, 2, 20001, 20324, dup_dict, all_mss, ed_mss)
    # get_mss(driver, 3, 30001, 33018, dup_dict, all_mss, ed_mss)
    # get_mss(driver, 4, 40001, 42551, dup_dict, all_mss, ed_mss)
    get_mss(driver, 5, 510001, 520030, dup_dict, all_mss, ed_mss)

    get_cntr_mss(driver, dup_dict, all_mss, 2, 2, ed_mss)
    print()
    
    '''get_cntr_mss(driver, dup_dict, all_mss, 1, 2, ed_mss)
    # ID 90056 (T789) appears to be a talisman containing John 11 and I indexed and transcribed it
    # Save dictionaries
    with open(f'dup_dict.pkl','wb') as f:
        pickle.dump(dup_dict, f)
    with open('all_mss.pkl','wb') as f:
        pickle.dump(all_mss, f)'''

# Get all manuscripts from the Center for New Testament Restoration
def get_cntr_mss(driver, dup_dict, all_mss, first_class, last_class, ed_mss):
    driver.get("https://greekcntr.org/manuscripts/index.htm")
    for i in range(first_class, last_class+1):
        cntr_class(i, driver, dup_dict, all_mss, ed_mss)

# Get a class of manuscripts from the CNTR
def cntr_class(i, driver, dup_dict, all_mss, ed_mss):
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
                
                # This compares edition numbers in here with those found in the NTVMR (relevant for anything in class 2 which is an ostracon/talisman) and links connected mss
                ed = re.sub(r'[^A-Za-z0-9]', '', alias)
                src = ed_mss.get(ed)
                if src is not None:
                    aka = src

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
                    ensure_existence(all_mss.get(aka), book, chap, text, verse, verse)
            else:
                print(f'Skipping {aka} (already got transcription)')
            
            driver.switch_to.default_content()

# Get all manuscripts from the NTVMR (specified by type and upper and lower bounds)
def get_mss(driver, type, lower_bound, upper_bound, dup_dict, all_mss, ed_mss):
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
            print(ms_name)
            sleep(1)
            
            # For linking duplicates or combined mss:
            # The format is either "Removed; Combined; See: MSNUM"
            #                   or "Removed; Duplicate; See: MSNUM"
            #                   or "Removed; See: CURRMSNUM"
            # Exception cases that are fine: 2560, 2892, L242, L652, L1353, L1398 but they still follow enough of the pattern to regex them consistently
            # NOTE even for duplicates, this still does normal page parsing and such. The correct ms is linked to it later
            if re.search('Removed', entry) is not None:
                if re.search('Combined', entry) is not None:
                    source_ms = re.search(r'(L|P)?\d+', re.search(r'See: (L|P)?\d+', entry).group()).group()
                    dup_type = 'Combined'
                elif re.search('Duplicate', entry) is not None:
                    source_ms = re.search(r'(L|P|T|O)?(s1-)?\d+', re.search(r'See: (L|P|T|O)?(s1-)?\d+', entry).group()).group()
                    dup_type = 'Duplicate'
                else:
                    pass # for the few extraneous ones that are self-referential

                # Other exception cases to manually handle: L355, L1353 (the INTF has weird things here)
                if re.match('L355', entry):
                    source_ms = '0303'
                if re.match('L1353', entry):
                    source_ms = 'L962'
                
                if dup_dict.get('forward').get(source_ms) is None:
                    dup_dict.get('forward').update({source_ms : []})
                curr_dups_at_ms = dup_dict.get('forward').get(source_ms)
                curr_dups_at_ms.extend([(ms_name, dup_type)])
                dup_dict.get('forward').update({source_ms : curr_dups_at_ms})
                dup_dict.get('backward').update({ms_name : source_ms})

            # Click ms to get its contents, get contents, get pages, get transcript (drill down)
            info[1].click()
            sleep(1)
            driver.switch_to.default_content()
            driver.switch_to.frame(info_frame)
            info = driver.find_element(value="content")
            contents = info.find_elements(By.TAG_NAME, "tr")
            while len(contents) < 10:
                contents = info.find_elements(By.TAG_NAME, "tr")
            sleep(0.2)
            stale = True
            while stale:
                try:
                    toprow = contents[0]
                    ths = toprow.find_elements(By.CLASS_NAME, "fieldValue")
                    linkspot = ths[0]
                    link = linkspot.find_elements(By.TAG_NAME, "a")[0]
                    
                    important_rows = {'Content' : dict(), 'GMO' : dict(), 'BC' : dict()}
                    gmo = 0
                    c = 0
                    bc = 0
                    for row in contents:
                        # Get biblical content info
                        if row.text[:7] == "Content":
                            important_rows.get('Content').update({c : row.find_elements(By.TAG_NAME, 'td')[0].accessible_name})
                            c += 1
                        elif row.text[:30] == "General Manuscript Observation":
                            important_rows.get('GMO').update({gmo : row.find_elements(By.TAG_NAME, 'td')[0].accessible_name})
                            gmo += 1
                        elif row.text.__contains__('Biblical Content'):
                            important_rows.get('BC').update({bc : re.sub('Biblical Content ?', '', row.text)})
                            bc += 1

                        # Get year info
                        if row.text.__contains__('Origin Year Early'):
                            ms_dict.update({'yr_start' : max(0, int(row.find_elements(By.TAG_NAME, 'td')[0].accessible_name))})
                        if row.text.__contains__('Origin Year Late'):
                            ms_dict.update({'yr_end' : max(0, int(row.find_elements(By.TAG_NAME, 'td')[0].accessible_name))})

                        # Get Edition info to compare Talismans and Ostraca with CNTR things:
                        if row.text.__contains__('Edition'):
                            ed_mss.update({re.sub('(Edition ?)|([^A-Za-z0-9])', '', row.text) : ms_name})

                    # Annoying spaghetti solution to a problem caused by inconsistencies in the format of GMO in 070
                    if ms_name == '070':
                        # Just reset GMO to be the correct contents manually
                        important_rows.update({'GMO' : {0 : 'L 3,19-30; 8,13-19.55-9,9; 9,9-17; 10,21-30; 10,30-39; 10,40-11,6; 11,24-42; 12,5-14; 12,15-13,32; 16,4-12; 21,30-22,2; 22,54-65; 23,4-24,26; J 3,23-32; 5,22-42; 7,3-12; 8,13-22; 8,33-42; 8,42-9,39; 11,48-56; 12,27-36.46-13,4'}})
                    
                    master_range = []

                    # Get range from GMO (catch errors)
                    try:
                        regex_gmo_range(important_rows, master_range, already_formatted=ms_name.__contains__('Os'))
                        # If it fails, clear it out and continue on (address later if needed)
                    except Exception as e:
                        with open('errlog.txt','a') as f:
                            f.write(f'Regex GMO failed in {ms_name} with {e} in: \n\t{important_rows.get("GMO")}\n\n\n')
                            print_exc(file=f)
                        master_range = []

                    # For ones that return nothing, try going through 'Content' or 'Content Overview' or 'Biblical Content'
                    if len(master_range) == 0:

                        # Lectionary contents getting ('Biblical Content')
                        if ms_name[0] == 'L':
                            # Spaghetti to handle a few early edge cases
                            # NOTE, because of how confusing it is to record what lectionaries contain, this part will be inherently dubious
                            if ms_name == 'L1604' or ms_name == 'L1043' or ms_name == 'L2210':
                                # Do this to not mess up the contents on the few early lectionaries.
                                pass
                            elif ms_name == 'L1354':
                                # The INTF does not contain pages for L1354, so the contents will be hardcoded here
                                important_rows.update({'GMO' : {0: 'Mt 3; Mc 1'}})
                                regex_gmo_range(important_rows, master_range)
                            else:
                                # Normal lectionary contents getting
                                regex_bc(important_rows.get('BC'), master_range)

                        # Special case for 0212
                        elif ms_name == '0212':
                            # Just skip now because it will be gotten later in get_cntr_class
                            pass
                        
                        # Non-lectionary contents getting
                        else:
                            regex_co_range(important_rows, master_range)

                    # Update dictionary for the manuscript with the range of contents
                    add_range(master_range, ms_dict)

                    # Click link, get page contents and transcription, and return control
                    link.click()
                    stale = False

                    # Get pages and return control to here
                    try:
                        get_pages(driver, ms_dict)
                    except Exception as e:
                        with open('errlog.txt','a') as f:
                            f.write(f'Error during get_pages in {ms_name}: {e}\n')
                            print_exc(file=f)
                    driver.switch_to.default_content()
                    driver.switch_to.frame(list_frame)
                
                # Try reloading if there is a stale element
                except Stale as e:
                    contents = info.find_elements(By.TAG_NAME, "tr")

                # Log other errors and move on
                except Exception as e:
                    print(f'Error in {ms_name} (logged)')
                    with open('errlog.txt','a') as f:
                        f.write(f'An error occurred at {ms_name}: {e}\n')
                        print_exc(file=f)
                    stale = False
                    for window in driver.window_handles:
                        if window != driver.window_handles[0]:
                            driver.switch_to.window(window)
                            driver.close()
                    driver.switch_to.default_content()
                    driver.switch_to.frame(list_frame)

            # Save each dictionary so that progress is saved
            '''with open(f'mss/{ms_name}.pkl','wb') as f:
                pickle.dump(ms_dict, f)'''
            # Update master dictionary
            all_mss.update({ms_name : ms_dict})
            sleep(1)

    print(f'Finished getting all manuscripts of type {type}')

# Get all the indexed pages for a given manuscript in the NTVMR
def get_pages(driver, ms_dict):
    driver.switch_to.window(driver.window_handles[1])
    sleep(1)
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
        ms_id = re.search('doc(\d{5,6})page', id).groups()[0]
        page_num = re.search('page(\d+)img', id).groups()[0]
        if id[-1] == '0':
            print(f'\t{page_num}')
            contains = page.find_elements(By.CLASS_NAME, "bibContDisp")[0]
            # Remove things like "inscriptio/subscription" or "commentary" from the thing
            contents = re.sub(r'\d? ?[A-Za-z]+ ?(inscriptio|subscriptio)[^;]*;?', '', contains.text)
            contents = re.sub(r'( |\n|\t)*\+?( |\n|\t)*Commentary[^;]*;?', '', contents)
            if contents != "No Index Content" and contents != '':
                try:
                    get_trans(driver, ms_id, page_num, contents, ms_dict)
                except Exception as e:
                    with open('errlog.txt','a') as f:
                        f.write(f'Error during get_trans in {ms_id} at page {page_num} ({contents}): {e}\n')
                        print_exc(file=f)

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.switch_to.frame(list_frame)

# Get the transcription for a given manuscript in the NTVMR
def get_trans(driver, ms_id, page_num, contents, ms_dict):
    # Ensure that each verse of the contents is in this manuscript's dictionary
    contents = re.sub(r'([^\d]):([^\d])', r'\1;\2', contents)
    chunks = re.split(r'[^A-Za-z 0-9\-:]', contents)
    for chunk in chunks:
        if not chunk.__contains__('inscriptio') and not chunk.__contains__('subscriptio'):
            s = chunk.strip().split(' ')
            try:
                book = books[s[0]]
                cv = s[1].split(':')
                chap = int(cv[0])
                v_bounds = cv[1].split('-')
                v_st = int(v_bounds[0])
                try:
                    v_end = int(v_bounds[1])
                except IndexError:
                    v_end = v_st

                # Somehow add the content range to the dictionary and initialize the transcription with blanks
                ensure_existence(ms_dict, book, chap, "", v_st, v_end)
                for v in range(v_st, v_end+1):
                    add_verse(book, chap, v, '', page_num, ms_id, ms_dict, contents)
            except KeyError as e:
                print(f'{s[0]} {s[1]} is not a valid NT verse (ignoring)')

    if contents.__contains__("Rev") is False:
        apoc_flag = ""
    else:
        apoc_flag = "&userName=Apokalypse%20Edition"
    # TODO IGNTP flag??
    # TODO if a flag has nothing, try the main page

    page = f'https://ntvmr.uni-muenster.de/community/vmr/api/transcript/get/?docID={ms_id}&pageID={page_num}&format=html{apoc_flag}'
    driver.execute_script(f'window.open("{page}")')
    driver.switch_to.window(driver.window_handles[2])
    sleep(1)
    
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
            try {
                osisid = e.dataset.osisid.replace(/,/g, '.');
            }
            catch {
                lectid = e.dataset.lectid.replace(/,/g, '.');
                lectid = lectid.replace(/ /g, '');
            }
            padChk = e.dataset.lectid === undefined ? osisid.match(/\./g) : lectid.match(/\./g);
            zeroPad = padChk === null ? ".0.0" : padChk.length === 1 ? ".0" : "";
            e.innerText = e.dataset.lectid === undefined ? osisid + zeroPad : lectid + zeroPad;
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
                    ef.write(f'Issues on page {page_num} of {ms_id} (blank element in list: {vv})\n')
                    print_exc(file=ef)
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
                    try:
                        add_verse(books[bcv[0]], int(bcv[1]), int(bcv[2]), text, page_num, ms_id, ms_dict, contents)
                    except KeyError:
                        print(f'{bcv[0]} {bcv[1]}:{bcv[2]} is not a valid NT verse (ignoring)')

    driver.close()
    driver.switch_to.window(driver.window_handles[1])
    driver.switch_to.frame(list_frame)

# Associate an INTF page number and/or transcription with a verse in a manuscript (it is assumed that the verse is already in its contents, but if not it adds it)
def add_verse(book, chap, verse, text, page_num, ms_id, ms_dict, contents):
    try:
        concat = ms_dict.get(book).get(chap).get(verse).get('t')
        ms_dict.get(book).get(chap).get(verse).update({'t' : concat + text})
        ms_dict.get(book).get(chap).get(verse).update({'intf_page' : page_num})
        ms_dict.update({'transcription?' : True})
    except Exception as e:
        with open('errlog.txt','a') as ef:
            ef.write(f'Potential issues on page {page_num} of {ms_id} (found {book} {chap}:{verse} in a page purporting to contain {contents}): {e}\n')
            print_exc(file=ef)
        
        # Correct an error in P41 where Acts 20:28-30 is marked as Acts 28:28-30
        if ms_id == 'P41' and book == 5 and chap == 28:
            add_verse(book, 20, verse, text, page_num, ms_id, ms_dict, contents)
        
        # Add verse if we find a transcription of it when we previously didn't know about it
        else:
            ensure_existence(ms_dict, book, chap, '', verse, verse)
            add_verse(book, chap, verse, text, page_num, ms_id, ms_dict, contents)

# Make sure that a verse exists in a manuscript (with or without a transcription)
def ensure_existence(ms_dict, book, chap, text, v_st, v_end):
    # Ensure book exists
    if ms_dict.get(book) is None:
        ms_dict.update({book : dict()})
    # Ensure chapter exists
    if ms_dict.get(book).get(chap) is None:
        ms_dict.get(book).update({chap : dict()})
    # Add verses
    for v in range(v_st, v_end+1):
        ms_dict.get(book).get(chap).update({v : {'t': text}})

# This takes GMO from the important_rows dictionary and does regex and range creation on it
def regex_gmo_range(important_rows, master_range, already_formatted=False):
    for things in important_rows.get('GMO'):
        thing = important_rows.get('GMO').get(things)
        thing = re.sub(r'\( ?\? ?\)', '', thing)                 # Remove '(?)' marks
        thing = re.sub(r'/', ';', thing)                         # Replace slashes with semicolons
        thing = re.sub(r'([,\.:;])? ?\([^)]*\) ?;?', ';', thing) # Remove parenthesized parts (with potential surrounding spaces and leading punctuation)
        thing = re.sub(r'([\.,:;])*$|^([\.,:;])*', '', thing)    # Remove punctation at the beginning or end of lines
        thing = re.sub(r'\+[, ]', ';', thing)                    # Replace '+,' (or '+ ') with a semicolon because this indicates an entire chapter
        thing = re.sub(r'([,;])+([,;])', r'\1', thing)           # I have no idea if this is needed at all
        if not already_formatted:
            thing = re.sub(r',', r':', thing)                        # Replace commas with colons
        thing = re.sub(r'\.', r',', thing)                       # Replace periods with commas
        thing = re.sub(r'fin,?', '0000', thing)                  # Replace 'fin' with 000 to handle later (leaving it as fin breaks the chapter division regex)
        thing = re.sub(r'\?|\+', '', thing)                      # Remove extra + and ?
        thing = re.sub(r'\/\d+', '', thing)                      # Replace things like 17/18 to just 17 (I don't care if it could be a little better)
        thing = re.sub(r'\[[^]]*\]', '', thing)                  # Remove anything in brackets 
        thing = re.sub(r'(\d)(a|b)', r'\1', thing)               # Replace things like 1-4a with 1-4, or 4b-5 with 4-5

        # If the start of the entry is in the format of a reference, keep, else discard (the __contains__ is an edge case that breaks this at 30319)
        if re.match(r'\d? ?[A-Za-z]+ \d', thing) is not None and not thing.__contains__('miniscule'):
            # Replace potential 'f' with the next verse
            fs = re.search(r'\d+f', thing)
            if fs is not None:
                fs = re.findall(r'\d+f', thing)
                while len(fs) != 0:
                    split_point = thing.rfind(fs.pop())
                    begin = thing[:split_point]
                    end = thing[split_point:]
                    num = int(re.match('\d+', end).group())
                    new_end = re.sub('f', '-' + str(num + 1), end)
                    thing = begin + new_end

            # Split on new book
            book_units = re.split(r'(\d? ?[A-Za-z]+( [\d:;\-\– ,\+\?]+)?($|[:;,]))', thing)[1::4]
            for bookss in book_units:
                book = re.sub(r'([\.,:;])*$', '', bookss.strip())               # Replace trailing whitespace or punctuation
                book_name = re.search(r'\d? ?[A-Za-z]+', book).group()
                book_contents = book[len(book_name):].strip()
                try:
                    bk = books[book_name]
                    # When there is nothing but the book name (as in P46)
                    if book_contents == '':
                        range = get_bible_range(book_name, 1, 1, get_chap_ct(bk), get_v_ct(bk, get_chap_ct(bk)))
                        master_range.extend(range)
                    # When we have more fine grained information
                    else:
                        start_chap = 0
                        sections = re.split(' ?; ?', book_contents)
                        for section in sections:
                            got_chap = False
                            parts = re.split(' ?, ?', section)

                            # This is a really stupid thing to prevent an error in 20311
                            skip = False
                            for part in parts:
                                try:
                                    n = int(part)
                                    if n > 80:
                                        skip = True
                                except:
                                    pass
                            if skip:
                                break
                            # I absolutely hate it (above) but it works

                            for part in parts:
                                # For single chapter books, mark the implicit single chapter
                                if bk == 18 or bk == 24 or bk == 25 or bk == 26:
                                    start_chap = 1
                                    got_chap = True
                                
                                end_chap = start_chap   # The last hit chapter must always be updated
                                # When there is a range
                                if part.__contains__('-') or part.__contains__('–'):
                                    limits = re.split(' ?[\-\–] ?', part)
                                    start = limits[0]
                                    end = limits[1]
                                    if start.__contains__(':'):
                                        ref = start.split(':')
                                        start_chap = int(ref[0])
                                        got_chap = True
                                        start_verse = int(ref[1])
                                    else:
                                        if got_chap:
                                            start_verse = int(start)
                                        else:
                                            start_chap = int(start)
                                            start_verse = 1

                                    if end.__contains__(':'):
                                        ref = end.split(':')
                                        end_chap = int(ref[0])
                                        end_verse = int(ref[1])
                                    else:
                                        # Handle the case where 'fin' is present instead of a number
                                        if end == '0000':
                                            end_chap = get_chap_ct(bk)
                                            end_verse = get_v_ct(bk, end_chap)
                                        else:
                                            if got_chap:
                                                end_chap = start_chap
                                                end_verse = int(end)
                                            else:
                                                end_chap = int(end)
                                                end_verse = get_v_ct(bk, end_chap)
                                    range = get_bible_range(book_name, start_chap, start_verse, end_chap, end_verse)
                                    start_chap = end_chap   # Move start chap forward if end_chap has crossed a chapter barrier
                                # When there is not a range
                                else:
                                    # Just get one verse
                                    if part.__contains__(':'):
                                        # With a chapter indicator
                                        cv = part.split(':')
                                        start_chap = int(cv[0])
                                        start_verse = int(cv[1])
                                        got_chap = True
                                        range = [(books[book_name], start_chap, start_verse)]
                                    # A single number
                                    else:
                                        # A verse (without a chapter indicator)
                                        if got_chap:
                                            start_verse = int(part)
                                            range = [(books[book_name], start_chap, start_verse)]
                                        # A chapter
                                        else:
                                            start_chap = int(part)
                                            end_chap = start_chap
                                            start_verse = 1
                                            end_verse = get_v_ct(bk, end_chap)
                                            range = get_bible_range(book_name, start_chap, start_verse, end_chap, end_verse)

                                master_range.extend(range)
                
                # Handle random words in the entry
                except KeyError:
                    pass
                    # print(f'{book_name} is not a valid NT book')

# This takes Content/Content Overview from important_rows and does regex and range creation on it
def regex_co_range(important_rows, master_range):
    content_list = []
    add_these = []
    gmo_like = False
    for item in important_rows.get('Content'):
        reg = important_rows.get('Content')[item]
        # Check first to see if the format is like GMO (more specific)
        if re.match(r'\d? ?[A-Za-z]+ \d', reg) is not None:
            gmo_like = True
            important_rows.update({'GMO' : {0: reg}})
            try:
                regex_gmo_range(important_rows, master_range, already_formatted=True)
            except Exception as e:
                pass
        
        # Scan through all and apply a regex that removes things like ePK: (anything to the left of a colon)
        else:
            contents = re.sub(' |†', '', reg)                           # Remove all spaces and † characters
            contents = re.sub(r'\([^)]*\)', '', contents)               # Remove anything between parens
            contents = re.sub(r'(e|a|p|r)(P|K)', '\1', contents)        # Remove info about how a category (eapr) is contained (PK)
            contents = re.sub(r':\?', '', contents)                     # Remove ':?' so that the next one isn't messed up
            must_do = True if contents.__contains__(':') else False     # Despite potentially longer strings being present for each range item,
                                                                            # do this no matter what is there is more specific info (denoted by colon)
            contents = re.sub(r'(e|a|p|r)+:', '', contents)             # Remove anything to the left of a colon as well as the colon
            contents = re.sub(r'1-3J', r'1J2J3J', contents)             # Replace 1-3J with 1J2J3J
            contents = re.sub(r'R-Tt', r'R1K2KGEPhK1Th2Th1T2TTt', contents) # A manual fix of a thing in 30309
            if contents != '':                                          # Append values to one of the lists
                if must_do:
                    add_these.append(contents)                          # These must be done unconditionally
                else:
                    content_list.append(contents)                       # These should be compared for length below

    # Return if there was a GMO like range in here, otherwise search through the remaining
    if gmo_like:
        return

    # Take the longest of these (if several are the same length, just do all of them (as well as all must_dos))
    longest = (0, None)
    for contents in content_list:
        if len(contents) > longest[0]:
            longest = (len(contents), contents)
        elif len(contents) == longest[0]:
            temp = longest + tuple(contents)
            longest = temp

    # Add the longest to the list of things to add
    for long in longest[1:]:
        add_these.append(long)

    # Go through the list of things to add and actually create a Bible range
    for add in add_these:
        # Split at book or split at category (eapr)
        ranges = re.split(r'(e|a|p|r)|(\d?[A-Z][a-z]*)', add)[1::4]
        for b_range in ranges:
            # Categories
            if b_range == 'a':
                master_range.extend(add_several_books(5, 5))
                master_range.extend(add_several_books(20, 26))
            elif b_range == 'e':
                master_range.extend(add_several_books(1, 4))
            elif b_range == 'p':
                # Includes Hebrews
                master_range.extend(add_several_books(6, 19))
            elif b_range == 'r':
                master_range.extend(add_several_books(27, 27))
            
            # Individual books
            elif b_range != '':
                bk = books[b_range]
                master_range.extend(add_several_books(bk, bk))

# This is for creating a range for lectionaries (pretty simple)
def regex_bc(bc, master_range):
    for b in bc:
        bb = bc.get(b)
        if re.search(r'Gosp', bb, re.IGNORECASE) is not None:
            regex_co_range({'Content' : {0 : 'e'}}, master_range)
        if re.search(r'Apost', bb, re.IGNORECASE) is not None:
            regex_co_range({'Content' : {0 : 'ap'}}, master_range)

# This will return a list of triples of (book, chap, verse) in ascending order
def get_bible_range(bn, sc, sv, ec, ev, is_num=False):
    book = bn if is_num else books[bn]
    b_range = []

    # Get verses within the current chapter
    if ec == sc:
        for v in range(sv, ev+1):
            b_range.append((book, sc, v))
    else:
        # Add verses in starting chapter
        for v in range(sv, get_v_ct(book, sc)+1):
            b_range.append((book, sc, v))
        # Add all verses in the middle
        for chap in range(sc+1, ec):
            for v in range(1, get_v_ct(book, chap)+1):
                b_range.append((book, chap, v))
        # Add verses in end chapter
        for v in range(1, ev+1):
            b_range.append((book, ec, v))

    return b_range

# This adds a range of contents to a manuscript's dictionary
def add_range(master_range, ms_dict):
    for b, c, v in master_range:
        ensure_existence(ms_dict, b, c, '', v, v)

# This adds several books at once (intended to be used for an entire category eapr)
def add_several_books(start_book, stop_book):
    b_range = []
    for bk in range(start_book, stop_book+1):
        b_range.extend(get_bible_range(bk, 1, 1, get_chap_ct(bk), get_v_ct(bk, get_chap_ct(bk)), is_num=True))
    return b_range

if __name__ == "__main__":
    gather_data()