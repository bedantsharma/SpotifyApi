from download_via_link import DownloadSong
import threading

D1 = DownloadSong()
D2 = DownloadSong()

links = []

with open("links.txt",'r') as file:
    for link in file:
        links.append(link.strip())
        
t1 = threading.Thread(target=D1.main, args=(links[0],))
t2 = threading.Thread(target=D2.main, args=(links[1],))

t1.start()
t2.start()
t1.join()
t2.join()

print('two songs downloaded at once')