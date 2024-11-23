import os
from typing import List, Dict
from pdfsrc.authorcell import *
from pdfsrc.styles import *
from pdfsrc.latexfile import *
from pdfsrc.latexchapter import *

# get a list of chapters as defined in settings json file
def get_chapter_list(config : Settings, style : Styles) -> Dict[str, LatexChapter]:
    chapters = {}
    chapter_files = []
    for chapter_data in config['pdf.chapters']:
        chapter_name = get_insensitive_str(config[f'pdf.chapters/{chapter_data}/name'])
        chapter_file = config[f'pdf.chapters/{chapter_data}/file']
        chapter_base = config.getKeyIfExists(f'pdf.chapters/{chapter_data}/base')

        # if chapter has already been added, raise error
        if chapter_name in chapters.keys():
            raise Exception(f'Fatal Error: Duplicate Chapter {chapter_name} found in {config.file}')

        chapters[chapter_name] = LatexChapter(config, chapter_base, style, chapter_file)
        chapter_files.append(chapter_file)
    return chapters

# add file to it's chapter, 
# if the chapter does not exist raise an exception
# returns chapters dictionary with the file
def register_latex_file(filename : str, fileroot : str, chapters : Dict[str, LatexChapter], style : Styles, config : Settings) -> Dict[str, LatexChapter]:
    for chapter in chapters.values():
        if chapter.compiledfile == filename:
            return chapters
    if config.isSkippedFile(filename) and (config.skiplist != None):
        config.log(f'Skipped processing file {filename}\n\tReason: in skiplist {config["pdf.skipfile"]}')
        return chapters
    file : LatexFile = LatexFile(filename, fileroot, style, config)
    if not file.isMainFile:
        config.log(f'Skipped processing file {filename}\n\tReason: Did not match conditions given in key "pdf.conditions.validlatex" in json file {config.file}')
        return chapters
    chapter_list = []
    for chapter_dicts in config['pdf.chapters']:
        chapter_list.append(config[f'pdf.chapters/{chapter_dicts}/name'])
    try:
        chapters[file.chapter.lower()].add_file(file)
    except KeyError:
        print(f'Fatal Error: Chapter {file.chapter} is not defined in json file {config.file}')
        print(f'file {filename} to one the following folders:\n\t', '\t'.join(chapter_list))
    return chapters



# registers all latex file in 'latex.root' json key
def get_latex_files(chapters, style : Styles, config : Settings) -> Dict[str, LatexChapter]:
    for root, dirs, files in os.walk(config['latex.root']):
        for f in files:
            filename, file_ext = os.path.splitext(f)

            #if the file is latex, then register it
            if file_ext == '.tex':
                # print(filename)
                chapters = register_latex_file('{}/{}'.format(root, f), root, chapters, style, config)
    return chapters


def main():
    settings : Settings = Settings('pdfc.json')
    style : Styles = Styles(settings)

    chapters = get_chapter_list(settings, style)
    # years = get_years_list(settings, style)
    try:
        chapters = get_latex_files(chapters, style, settings)
        # print(chapters)
        # years = get_latex_years_files(years, style, settings)
        for chapter in chapters:
            chapters[chapter].compile()
        
    # for year in years:
    #     years[year].compile()
    except Exception as exception:
       print(exception)
       print('The final pdf will not be compiled.')
       if settings.logfile != None:
           print(f'Output written to {settings["pdf.log"]}')

if __name__ == '__main__':
    main()
