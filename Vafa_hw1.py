from concurrent.futures.thread import ThreadPoolExecutor
try:
    import requests                                             
                                                                
except ModuleNotFoundError:
    print("This program uses 'requests' library. Please install it using 'pip'")
import time
import os


#links with lists
links = [
    "http://www.ubicomp.org/ubicomp2003/adjunct_proceedings/proceedings.pdf",
    "https://www.hq.nasa.gov/alsj/a17/A17_FlightPlan.pdf",
    "https://ars.els-cdn.com/content/image/1-s2.0-S0140673617321293-mmc1.pdf",
    "http://www.visitgreece.gr/deployedFiles/StaticFiles/maps/Peloponnese_map.pdf"
    ]

#download function
def download(link, file):
    r = requests.get(link, stream=True)
    if not os.path.exists("./downloads/"):              
        os.mkdir("./downloads/")
    with open(os.path.join("./downloads/", file), "wb") as wf:     
        for chunk in r.iter_content(512):
            if chunk:
                wf.write(chunk)
            else:
                break
    print(file[:-4], "-> done")     


max_threads = os.cpu_count()
workers = 4 if max_threads > 4 else max_threads             

while True:
    thread_mode = int(input("Enter thread mode (0 for single-thread. 1 for multi-thread): "))     

    if thread_mode == 0:      # single thread
        start = time.time()
        for i, link in enumerate(links):                
            file = "file" + str(i + 1) + ".pdf"
            download(link, file)
        print("Time:", round(time.time() - start, 2), "sec")
    
    elif thread_mode == 1:    # multi thread
        start = time.time()
        with ThreadPoolExecutor(max_workers=workers) as executor:       
            for i, link in enumerate(links):                 
                file = "file" + str(i + 1) + ".pdf"
                executor.submit(download, link, file)
        print("Time:", round(time.time() - start, 2), "sec")
    else:
        print("You entered invalid thread mode.")         
        continue
    break

