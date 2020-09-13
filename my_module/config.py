#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
'''
    FileName : get_config.py
    Date : 2020/09/13 16:47:02
    Author : HuangJianYi
    Copyright : © 2020 HuangJianYi <vahx@foxmail.com>
    License : MIT, see LICENSE for more details.
'''

import configparser #引入模块

class ConfigFile:
    # 生成ConfigParser对象
    config = configparser.ConfigParser()
    def __init__(self, path=None):
        # 配置文件的路径
        if path is not None:
            self.filename = path
        else:
            self.filename = r'C:\JianYi-Huang\config.ini'
            
    def read(self):
        self.config = configparser.ConfigParser()
        # 读取配置文件
        self.config.read(self.filename, encoding='utf-8')

    def get(self, item=None):
        self.read()

        local_config = dict()
        # 获取指定节点的options信息

        if item is not None:
            items = self.config.items(item)
        else:
            raise RuntimeError('请输入需要获取的节点名称')

        for i in items:
            local_config[i[0]] = i[1]
        
        return local_config
if __name__ == "__main__":
    config = ConfigFile()
    config = config.get('pushover')
    print(config)