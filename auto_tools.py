# python3.8
import os
import xml.etree.ElementTree as ET
import time
import re
from functools import cmp_to_key
import platform

import logging 
logging.basicConfig(level=logging.WARN,format = ' %(asctime)s - %(levelname)s- %(message)s')

def file_is_exists(file_name):
    return os.path.exists(file_name)

def read_config(config_file_path,config_item):
    root = ET.parse(config_file_path).getroot()
    include_dir_list = config_item['include_dir']
    for type_tag in root.findall('include_dir/item'):
        value = type_tag.text
        include_dir_list.append(value)
        logging.debug('Include dir is %s%%' % (value))
    platform_system = platform.system()
    if 'Linux' == platform_system:
        config_item['end_of_line_seq'] = '\n'
    elif 'Windows' == platform_system:
        config_item['end_of_line_seq'] = '\n'
    
    logging.debug('config_item[\'end_of_line_seq\']=%s%%'%config_item['end_of_line_seq'])

    img_cfg = root.find('img')
    for cfg in list(img_cfg):
        config_item[cfg.tag]=cfg.text
        logging.debug('config_item[{}] = {}'.format(cfg.tag,config_item[cfg.tag]))

    regex_ele_tag = 'regex'
    regex_cfg = root.find(regex_ele_tag)
    for cfg in list(regex_cfg):
        config_item[cfg.tag]=cfg.text 
        logging.debug("config_item[{}]={}".format(cfg.tag,cfg.text))

def cmp_items(a, b):
    reg = re.compile('^\d+_')
    logging.debug('a - {}'.format(a))
    logging.debug('b - {}'.format(b))
    a_match = reg.match(a)
    b_match = reg.match(b)
    if a_match != None and b_match !=None:
        num1= int(a_match[0][:-1])
        num2 = int(b_match[0][:-1])
        logging.debug('a num - {}'.format(num1))
        logging.debug('b num - {}'.format(num2))
        if num1 > num2:
            return 1
        elif num1 < num2:
            return -1
    elif a_match == None and b_match != None:
        return 1
    elif a_match != None and b_match == None:
        return -1
    else:
        if (a<b):
            return -1
        elif (a>b):
            return 1

def get_dir_file(dir_path):
    files = []
    for folder_name,subfolders,filenames in os.walk(dir_path):
        logging.debug('The Current folders is '+ folder_name)

        if len(folder_name)>2 and folder_name[0] == '.':
            continue
    
        for subfolder in subfolders:
            logging.debug('Subfolders of '+ folder_name + ': ' + subfolder)
        for filename in filenames:
            logging.debug('File inside '+ folder_name + ': '+ filename)
            if filename != 'README.md':
                files.append(filename)
    ret = sorted(files,key= cmp_to_key(cmp_items))  
    logging.debug('files is {}'.format(files))         
    return ret 

def current_data_time():
    current_time = time.strftime("%Y%m%d%H%M")
    logging.debug(current_time)
    return current_time


def regex_match_replace_img(number, current_time, blog_file_name, config_item):
    blog_name = blog_file_name[0:len(blog_file_name)-3]
    blog_file_img_name = ('{}_{}_{}{}'.format(blog_name
                          ,current_time,number,config_item['img_src_suffix']))
    img_src_path = ('{}/{}{}{}'.format(config_item['img_src_dir'] 
                    ,config_item['img_src_prefix']
                    , number ,config_item['img_src_suffix']))
    img_des_path = '../images/' + blog_file_img_name
    os.rename(img_src_path,img_des_path)
    logging.debug('src: {} , des: {}'.format(img_src_path , img_des_path))
    return True

def write_base_markdown(config_file,blog_map,categories):
    out_file = open(config_file,'w',encoding='UTF-8')
    out_file.write('# Categories')
    out_file.write(' ' + categories + config_item['end_of_line_seq'])
    out_file.write('* ## [home](../README.md)'+config_item['end_of_line_seq'])
    for item in blog_map.items():
        out_file.write('* ### ' + '[' + item[1] + ']' + '(' + item[0] + ')'+config_item['end_of_line_seq'])
        logging.debug('blog item {}'.format(item))
    out_file.write('                           step by steop')


def open_blog_clear_tail_links(blog_file,blog_map):
    reg1=('(.*#.*)')
    reg2=('[^# ].+')
    reg3=('.*addimage.*\\d+')
    reg4=('\\d+')

    in_file = open(blog_file,'r',encoding='UTF-8')
    out_file_name = 'tmp.md'
    out_file = open(out_file_name,'w',encoding='UTF-8')
    found = False
    only_get_one_blog_name = 0

    for tmp_line in in_file:
        found = re.match(reg1,tmp_line)
        only_get_one_blog_name += 1
        if found and (1 == only_get_one_blog_name):
            search_ret = re.search(reg2,tmp_line)
            tmp = search_ret.group()
            blog_map[blog_file]=tmp 
            out_file.write(tmp_line)
            continue
        found = re.match(reg3,tmp_line)
        if found:
            current_time = current_data_time() 
            search_ret = re.search(reg4,tmp_line)
            number = search_ret.group()
            if regex_match_replace_img(number,current_time,blog_file,config_item):
                out_file.write('![](../images/{}_{}_{}.png){}'.format(
                    blog_file[0:len(blog_file)-3],current_time,number,
                    config_item['end_of_line_seq']))
                continue
        if '[上一级]' in str(tmp_line):
            break
        out_file.write(tmp_line)
    out_file.close()
    in_file.close()
    tmp = blog_file
    os.remove(blog_file)
    os.rename(out_file_name,tmp)

def blog_add_pre_next_links(blog_file,blog_map):
    if file_is_exists(blog_file):
        out_file=open(blog_file,'a',encoding='UTF-8')
        out_file.write('[上一级](README.md)'+config_item['end_of_line_seq'])

        endPos = len(blog_map.keys())
        blog_key_list = list(blog_map.keys())
        pos = blog_key_list.index(blog_file)
        if pos >= endPos:
            logging.error('not found blog_file{}'.format(blog_file))
            return False
        
        if 0 == pos :
            tmp = pos
            tmp += 1
            if (tmp != endPos):
                out_file.write('[下一篇]({}){}'.format(blog_key_list[tmp]
                ,config_item['end_of_line_seq']))
        else :
            tmp = pos 
            if tmp+1 == endPos:
                out_file.write('[上一篇]({}){}'.format(blog_key_list[tmp-1]
                ,config_item['end_of_line_seq']))
            else:
                out_file.write('[上一篇]({}){}'.format(blog_key_list[tmp-1]
                ,config_item['end_of_line_seq']))
                out_file.write('[下一篇]({}){}'.format(blog_key_list[tmp+1]
                ,config_item['end_of_line_seq']))
    return True 


if __name__ == "__main__":
    global config_item
    config_item = {'include_dir':[]}
    read_config('config.xml',config_item)
    blog_map = {}
    root_path = os.getcwd()
    logging.debug('current work directory {}'.format(root_path))

    for dir in config_item['include_dir']:
        os.chdir('{}/{}'.format(root_path,dir))
        logging.debug('change directory to {}'.format(dir))

        files = get_dir_file('.')
        for file_name in files:
            open_blog_clear_tail_links(file_name,blog_map)
        for file_name in files:
            if not blog_add_pre_next_links(file_name,blog_map):
                logging.error('Error !!!!!!!')

            
        write_base_markdown("README.md",blog_map,dir)
        os.chdir(root_path)
        blog_map.clear()

    # Delete the original path of the picture 
    images = get_dir_file(config_item['img_src_dir'])
    for image in images:
        if(re.match(config_item['delete_ori_img_regex'],image)):
            img_full_path = config_item['img_src_dir'] + '/' + image
            os.remove(img_full_path)

