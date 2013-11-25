#!/usr/bin/python
'''
A python script for generating my personal static blogging site
author: rootuser
e-mail: jujaezen@gmail.com
'''
import os, argparse,subprocess,string,re
from datetime import date

def get_dir():
    home=os.path.expanduser('~')
    site_folder='blogtest'
    markdown=os.path.join(home,site_folder,'blog','markdown')
    html=os.path.join(home,site_folder,'blog','html')
    page=os.path.join(home,site_folder,'page')
    return {'markdown':markdown,'html':html,'page':page}
    
class NewPost(argparse.Action):
    def __call__(self,parser,namespace,values,option_string=None):
        new_post(values,get_dir()['markdown'])

class GenerateSites(argparse.Action):
    def __call__(self,parser,namespace,values,option_string=None):
        generate(get_dir()['markdown'],
                 get_dir()['html'],
                 get_dir()['page'])

class UpdateSites(argparse.Action):
    def __call__(self,parser,namespace,values,option_string=None):
        update(get_dir()['html'],get_dir()['page'])

def new_post(post_title, markdown_dir):
    '''
    read the title of the post from the argument and the markdown directory
    create new markdown file using choosing editor (default is vim).
    the name of the new file will be the date plus the post title.
    '''
    author='Rootuser'
    post_date=date.today().isoformat()
    post_name=re.sub('[^\w\s-]','',string.join(post_title.split(),'-'))
    fpathname=os.path.join(markdown_dir,post_name)+'.markdown'
    with open(fpathname,'w') as post:
        post.write('<!-- begin metadata\n')
        post.write('title: %s\n'%post_title)
        post.write('author: %s\n'%author)
        post.write('date: %s\n'%post_date)
        post.write('end metadata -->\n')

def generate(markdown_dir,html_dir,page_dir):
    '''
    read the markdown directory, html directory and page directory.
    convert all the markdown file to html
    '''
    highlight_style='pygments'
    css_style=page_dir+'/style.css'
    html_head=page_dir+'/header.html'
    html_before=page_dir+'/before.html'
    html_after=page_dir+'/after.html'
    html_poster=page_dir+'/post.html'
    author='Rootuser'
   
    md_list=os.listdir(markdown_dir)
    for md_file in md_list:
        file_name=os.path.splitext(md_file)[0]
        html_file=os.path.join(html_dir,file_name)+'.html'
        post_markdown=os.path.join(markdown_dir,md_file)
        
        with open(post_markdown) as metafile:
            meta_data=[metafile.next() for x in xrange(4)]

        post_title=meta_data[1].split(':')[1].strip()
        post_date=meta_data[3].split(':')[1].strip()

        with open(html_poster,'w') as post:
            post.write('\n')
            post.write('<a class="return_to_index" href="../index.html">Back to index</a>\n')
            post.write('<h1 class="post_title">%s</h1>\n'%post_title)
            post.write('<p class="date">%s</p>\n'%post_date)
            post.write('\n')


        pandoc_cmd=('pandoc -s -S --mathjax'\
                    ' --highlight-style %s'\
                    ' -c %s'
                    ' -H %s -B %s -B %s -A %s'\
                    ' -V pagetitle="%s" -V author-meta="%s"'\
                    ' -f markdown -t html5 -o %s %s'\
                   %(highlight_style,
                     css_style,
                     html_head,html_before,html_poster,html_after,
                     file_name,author,
                     html_file,post_markdown))

        subprocess.call(pandoc_cmd,shell=True)


def update(html_dir,page_dir):
    '''
    read the html directory and the page directory
    update the post list
    update the whole site (e.g. if css has been changed)
    '''
    print(page_dir)
    pass

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-n','--new',action=NewPost,
                        metavar="'new_post_title'")
    group.add_argument('-g','--generate',action=GenerateSites,nargs=0)
    group.add_argument('-u','--update',action=UpdateSites,nargs=0)
    parser.parse_args() 
