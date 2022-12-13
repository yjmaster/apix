# -*- coding: utf-8 -*-
import configparser
from time import strftime

def config_generator():
    # 설정파일 만들기
    config = configparser.ConfigParser()

    # 설정파일 오브젝트 만들기
    config['beflydb'] = {}
    config['beflydb']['host'] = '118.67.152.74'
    config['beflydb']['user'] = 'yjuser'
    config['beflydb']['password'] = 'Yjuser(1124#$)'
    config['beflydb']['db'] = 'spell_check'

    config['kpfdb'] = {}
    config['kpfdb']['host'] = 'localhost'
    config['kpfdb']['user'] = 'kpf'
    config['kpfdb']['password'] = 'kpf123'
    config['kpfdb']['db'] = 'newsai'
    
    config['kpf'] = {}
    config['kpf']['host'] = '0.0.0.0'
    config['kpf']['port'] = '10001'

    # 설정파일 저장
    with open('config.ini', 'w', encoding='utf-8') as configfile:
        config.write(configfile)        
        
def config_read():
    
    # 설정파일 읽기
    config = configparser.ConfigParser()    
    config.read('config.ini', encoding='utf-8') 

    # 설정파일의 색션 확인
    # print(config.sections())
    version_read(config)

def version_read(config):

    kpfdb = config['kpf']
    print(kpfdb['host'])

# config_generator()
config_read()