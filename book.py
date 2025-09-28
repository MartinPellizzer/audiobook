import os
import shutil

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

from kokoro import KPipeline
import soundfile as sf 

from pydub import AudioSegment

from lib import g
from lib import polish

pipeline = KPipeline(lang_code='a')

def clips():
    book = epub.read_epub('/home/ubuntu/books/the-green-witch.epub')

    pipeline = KPipeline(lang_code='a')

    i = 0
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            '''
            print('========================================')
            name = item.get_name()
            print(f'NAME: {name}')
            print('----------------------------------------')
            if name == 'xhtml/copy.xhtml':
                print(item.get_content())
            print('========================================')
            '''
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text = soup.get_text()
            print(text)
            generator = pipeline(text, voice='af_heart')
            for (gs, ps, audio) in generator:
                print(i, gs, ps)
                i_str = ''
                if i >= 10000: i_str = f'{i}'
                elif i >= 1000: i_str = f'0{i}'
                elif i >= 100: i_str = f'00{i}'
                elif i >= 10: i_str = f'000{i}'
                else: i_str = f'0000{i}'
                sf.write(f'output/{i_str}.wav', audio, 24000)
                i += 1
            # break
        '''
        if item.get_type() == ebooklib.epub.EpubHtml:
            print(item)
        '''

def book_pdf(book_filename):
    from pypdf import PdfReader
    reader = PdfReader(book_filename)
    i = 0
    for page in reader.pages:
        # page = reader.pages[0]
        # print(page.extract_text())
        # for text in page.extract_text():
        text = page.extract_text() 
        generator = pipeline(text, voice='af_heart')
        for (gs, ps, audio) in generator:
            print(i, gs, ps)
            i_str = ''
            if i >= 10000: i_str = f'{i}'
            elif i >= 1000: i_str = f'0{i}'
            elif i >= 100: i_str = f'00{i}'
            elif i >= 10: i_str = f'000{i}'
            else: i_str = f'0000{i}'
            sf.write(f'output/{i_str}.wav', audio, 24000)
            i += 1
    quit()

book_filename = 'socratic-logic.pdf'
book_filename = '48-laws-of-power.pdf'
book_pdf(book_filename)


