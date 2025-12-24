import json

from lib import g
from lib import io
from lib import llm

'''
from kokoro import KPipeline
import soundfile as sf 

pipeline = KPipeline(lang_code='a')

with open('test.txt') as f: text = f.read()

generator = pipeline(text, voice='af_heart')
for i, (gs, ps, audio) in enumerate(generator):
    print(i, gs, ps)
    sf.write(f'test/{i}.wav', audio, 24000)
'''
def outline_init():
    outline_filepath = f'{g.DATABASE_FOLDERPATH}/shop/videos/lotions/outline.txt'
    with open(outline_filepath) as f: content = f.read().strip()
    lines = [line for line in content.split('\n') if line.strip() != '']
    lines_formatted = []
    for line in lines:
        if line.startswith('            '):
            line = line.strip()
            if line[0].isdigit():
                line = ' '.join(line.split(' ')[1:])
            line = f'[H4] {line.strip()}'
            print(f'            {line.strip()}')
        elif line.startswith('        '):
            line = line.strip()
            if line[0].isdigit():
                line = ' '.join(line.split(' ')[1:])
            line = f'[H3] {line.strip()}'
            print(f'        {line.strip()}')
        elif line.startswith('    '):
            line = line.strip()
            if line[0].isdigit():
                line = ' '.join(line.split(' ')[1:])
            line = f'[H2] {line.strip()}'
            print(f'    {line.strip()}')
        else:
            line = line.strip()
            if line[0].isdigit():
                line = ' '.join(line.split(' ')[1:])
            line = f'[H1] {line.strip()}'
            print(f'{line.strip()}')
        lines_formatted.append(line)
    print()
    print()
    print()

    for line in lines_formatted:
        print(line)

    print()
    print()
    print()

    outline_dict = {}
    outline_dict['chapter_list'] = []
    chapter_cur = None
    section_cur = None
    subsection_cur = None
    for line in lines_formatted:
        line_type = line.split(' ')[0]
        line_content = ' '.join(line.split(' ')[1:])
        if line_type == '[H1]':
            outline_dict['chapter_list'].append({
                'name': line_content,
                'section_list': [],
            })
            chapter_cur = outline_dict['chapter_list'][-1]
        elif line_type == '[H2]':
            chapter_cur['section_list'].append({
                'name': line_content,
                'subsection_list': [],
            })
            section_cur = chapter_cur['section_list'][-1]
        elif line_type == '[H3]':
            section_cur['subsection_list'].append({
                'name': line_content,
                'qa_list': [],
            })
            subsection_cur = section_cur['subsection_list'][-1]
        elif line_type == '[H4]':
            subsection_cur['qa_list'].append({
                'question': line_content,
                'answer_short': '',
                'answer_medium': '',
                'answer_long': '',
            })

    print()
    print()
    print()

    print(json.dumps(
        outline_dict,
        indent=4,
    ))
    json_filepath = f'{g.DATABASE_FOLDERPATH}/shop/videos/lotions/data.json'
    io.json_write(json_filepath, outline_dict)

def answer_gen():
    json_filepath = f'{g.DATABASE_FOLDERPATH}/shop/videos/lotions/data.json'
    json_data = io.json_read(json_filepath)
    chapter_list = json_data['chapter_list']
    for chapter in chapter_list:
        print(f'''CHAPTER: {chapter['name']}''')
        section_list = chapter['section_list']
        for section in section_list:
            print(f'''SECTION: {section['name']}''')
            subsection_list = section['subsection_list']
            for subsection in subsection_list:
                print(f'''SUBSECTION: {subsection['name']}''')
                qa_list = subsection['qa_list']
                for qa in qa_list:
                    print(f'''QUESTION: {qa['question']}''')
                    question = qa['question']
                    ### gen answer short
                    if qa['answer_short'] == '':
                        prompt = f'Answer the following question in one line: {question}'
                        prompt += f'/no_think'
                        reply = llm.reply(prompt, model_filepath='')
                        if '</think>' in reply:
                            reply = reply.split('</think>')[1].strip()
                        qa['answer_short'] = reply
                        io.json_write(json_filepath, json_data)
                    ### gen answer medium
                    if qa['answer_medium'] == '':
                        prompt = f'Answer the following question in one paragraph: {question}'
                        prompt += f'/no_think'
                        reply = llm.reply(prompt, model_filepath='')
                        if '</think>' in reply:
                            reply = reply.split('</think>')[1].strip()
                        qa['answer_medium'] = reply
                        io.json_write(json_filepath, json_data)
                    ### gen answer long
                    if qa['answer_long'] == '':
                        prompt = f'Answer the following question in one page: {question}'
                        prompt += f'/no_think'
                        reply = llm.reply(prompt, model_filepath='')
                        if '</think>' in reply:
                            reply = reply.split('</think>')[1].strip()
                        qa['answer_long'] = reply
                        io.json_write(json_filepath, json_data)
                    if 0:
                        ### gen answer long book
                        if 'answer_long_book' not in qa: qa['answer_long_book'] = ''
                        if qa['answer_long_book'] == '':
                            prompt = f'Answer the following question in one page of a book: {question}. Format it like tipical content you find in books.'
                            prompt += f'/no_think'
                            reply = llm.reply(prompt, model_filepath='')
                            if '</think>' in reply:
                                reply = reply.split('</think>')[1].strip()
                            qa['answer_long_book'] = reply
                            io.json_write(json_filepath, json_data)

def text_format(text):
    text_formatted = text
    text_formatted = text_formatted.replace('’', "'")
    text_formatted = text_formatted.replace('–', "-")
    text_formatted = text_formatted.replace('—', "-")
    import string
    printable = set(string.printable)
    # printable = filter(lambda x: x in printable, text_formatted)
    printable = ''.join(filter(lambda x: x in printable, text_formatted))
    return printable

px_in = 20
px_out = 20

def h1(pdf, text):
    pdf.add_page()
    pdf.set_font('Helvetica', size=36, style='B')
    pdf.x = px_out
    pdf.multi_cell(210 - px_in - px_out, 12, text=f'{text}')
    pdf.ln()

def h2(pdf, text):
    pdf.add_page()
    pdf.set_font('Helvetica', size=24, style='B')
    pdf.x = px_out
    pdf.multi_cell(210 - px_in - px_out, 10, text=f'{text}')
    pdf.ln()

def h3(pdf, text):
    # pdf.add_page()
    pdf.set_font('Helvetica', size=16, style='B')
    pdf.x = px_out
    pdf.multi_cell(210 - px_in - px_out, 8, text=f'{text}')
    pdf.ln()

def h4(pdf, text):
    pdf.set_font('Helvetica', size=12, style='B')
    pdf.x = px_out
    pdf.multi_cell(210 - px_in - px_out, 6, text=f'{text}')
    pdf.ln()

def pdf_gen(qa_len):
    from fpdf import FPDF
    pdf = FPDF()
    json_filepath = f'{g.DATABASE_FOLDERPATH}/shop/videos/lotions/data.json'
    json_data = io.json_read(json_filepath)
    chapter_list = json_data['chapter_list']
    for chapter_i, chapter in enumerate(chapter_list):
        print(f'''CHAPTER: {chapter['name']}''')
        chapter_name = chapter['name']
        chapter_name = text_format(chapter_name)
        text = f'{chapter_i+1}. {chapter_name}'
        h1(pdf, text)
        ### section
        section_list = chapter['section_list']
        for section_i, section in enumerate(section_list):
            print(f'''SECTION: {section['name']}''')
            section_name = section['name']
            section_name = text_format(section_name)
            text = f'{chapter_i+1}.{section_i+1} {section_name}'
            h2(pdf, text)
            ### subsection
            subsection_list = section['subsection_list']
            for subsection_i, subsection in enumerate(subsection_list):
                print(f'''SUBSECTION: {subsection['name']}''')
                subsection_name = subsection['name']
                subsection_name = text_format(subsection_name)
                text = f'{chapter_i+1}.{section_i+1}.{subsection_i+1} {subsection_name}'
                h3(pdf, text)
                ### qa
                qa_list = subsection['qa_list']
                for qa_i, qa in enumerate(qa_list):
                    print(f'''QUESTION: {qa}''')
                    question = qa['question']
                    question = text_format(question)
                    text = f'{chapter_i+1}.{section_i+1}.{subsection_i+1}.{qa_i+1} {question}'
                    h4(pdf, text)
                    if qa_len == 'short':
                        answer = qa['answer_short']
                        answer = text_format(answer)
                    elif qa_len == 'medium':
                        answer = qa['answer_medium']
                        answer = text_format(answer)
                    elif qa_len == 'long':
                        answer = qa['answer_long']
                        answer = text_format(answer)
                    pdf.set_font('Helvetica', size=11)
                    pdf.x = px_out
                    pdf.multi_cell(210 - px_in - px_out, 6, text=f'{answer}')
                    pdf.ln()
    pdf.output(f'{g.DATABASE_FOLDERPATH}/shop/videos/pdfs/{qa_len}.pdf')

def narration_gen(qa_len):
    output_text = ''
    json_filepath = f'{g.DATABASE_FOLDERPATH}/shop/videos/lotions/data.json'
    json_data = io.json_read(json_filepath)
    chapter_list = json_data['chapter_list']
    for chapter_i, chapter in enumerate(chapter_list):
        print(f'''CHAPTER: {chapter['name']}''')
        chapter_name = chapter['name']
        chapter_name = text_format(chapter_name)
        ### section
        section_list = chapter['section_list']
        for section_i, section in enumerate(section_list):
            print(f'''SECTION: {section['name']}''')
            section_name = section['name']
            section_name = text_format(section_name)
            ### subsection
            subsection_list = section['subsection_list']
            for subsection_i, subsection in enumerate(subsection_list):
                print(f'''SUBSECTION: {subsection['name']}''')
                subsection_name = subsection['name']
                subsection_name = text_format(subsection_name)
                ### qa
                qa_list = subsection['qa_list']
                for qa_i, qa in enumerate(qa_list):
                    print(f'''QUESTION: {qa}''')
                    question = qa['question']
                    question = text_format(question)
                    # print(question)
                    # continue
                    if qa_len == 'short':
                        answer = qa['answer_short']
                        answer = text_format(answer)
                    elif qa_len == 'medium':
                        answer = qa['answer_medium']
                        answer = text_format(answer)
                    elif qa_len == 'long':
                        answer = qa['answer_long']
                        answer = text_format(answer)
                    output_text += answer
                    output_text += '\n'
    with open(f'{g.DATABASE_FOLDERPATH}/shop/videos/narrations/{qa_len}.txt', 'w') as f: f.write(output_text)


def main():
    # outline_init()
    # answer_gen()
    # pdf_gen('short')
    # pdf_gen('medium')
    # pdf_gen('long')
    narration_gen('medium')

main()
