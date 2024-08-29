from download_via_link import DownloadSong
import threading

# Function to download a song using DownloadSong class
def download_song(id_number, link):
    downloader = DownloadSong(id_number)
    downloader.main(link)

# Read links from the file
links = []
with open("links.txt", 'r') as file:
    for link in file:
        links.append(link.strip())
        
        
print('the number of songs to be downloaded : {}'.format(len(links)))

# Specify the number of threads you want to use
num_threads = 5  # Change this to the desired number of threads

# Create and start the threads
threads = []
for i in range(num_threads):
    t = threading.Thread(target=download_song, args=(i, links[i]))
    threads.append(t)
    t.start()

# Continue assigning links to threads until all links are processed
next_link_idx = num_threads
while next_link_idx < len(links):
    for i in range(num_threads):
        if not threads[i].is_alive() and next_link_idx < len(links):
            threads[i] = threading.Thread(target=download_song, args=(i, links[next_link_idx]))
            threads[i].start()
            next_link_idx += 1

# Wait for all threads to complete
for t in threads:
    t.join()

print(f'All songs downloaded using {num_threads} threads')
