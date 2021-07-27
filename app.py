import tkinter as tk
import requests
from bs4 import BeautifulSoup
import shutil
from pathlib import Path
from os import path


window = tk.Tk()
label = tk.Label(window, text="LINK").grid(row=0)
entry = tk.Entry(window)
entry.grid(row=0, column=1)

def download_images():
    try:
        page_url = entry.get().strip()
        if not page_url or 'https://www.bobaedream.co.kr/cyber/CyberCar_view.php?no=' not in page_url:
            return
        page = requests.get(page_url)
        soup = BeautifulSoup(page.text, 'html.parser')
        bb = [b.text for b in soup.select('b')]
        plate_num = 'new_data'
        for b in bb:
            if '차량번호' in b:
                plate_num = b.replace('차량번호', '').strip()
                break
        Path(f'./bobae_dream_images/{plate_num}').mkdir(parents=True, exist_ok=True)
        imgs = soup.select('img')
        imgs = [img['src'] for img in imgs if 'CyberCar' in img['src'] and '.jpg' in img['src'] and 'img_' in img['src']]
        for img in imgs:
            img_url = f'https:{img}'
            img_data = requests.get(img_url)
            img_data = requests.get(img_url, stream=True)
            with open(path.join('bobae_dream_images', plate_num, img_url.split('/').pop()), 'wb') as out_file:
                shutil.copyfileobj(img_data.raw, out_file)
            del img_data
    except Exception as e:
        print(e)



button = tk.Button(
    window,
    text='Download',
    command=download_images,
    highlightbackground='#3E4149'
)
button.grid(row=0, column=2)

window.mainloop()
