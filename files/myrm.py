#!/usr/bin/env python
import sys
import logging
import argparse
import errno
import os
import json
import shutil
import datetime
import glob
import logging
from setuptools import setup, find_packages
from Load_config import Load_config
#from files.log import _setup_log


def del_file(path_basket, path_information, name, dry_run=False, confirm=False, silent=False):
    path_str = os.path.abspath(name)
    result = path_str
    result += " size:" + str(os.path.getsize(result)) + "  Deleting successfully"
    try:
        check_confirm(confirm)
        path_str = os.path.abspath(name)
        (dir_name, file_name) = os.path.split(path_str)
        (file_Base_Name, file_Extension) = os.path.splitext(file_name)
        if dry_run is True and silent is False:
            return os.path.abspath(name)
        else:
            count = 0
            logging.info(path_str + "  file removed")
            new_path = path_basket + file_name
            if os.path.exists(new_path):
                count += 1
                while True:
                    if os.path.exists("{0}.{1}".format(new_path, count)):
                        count += 1
                    else:
                        break
                new_path += ".{0}".format(count)
            os.rename(path_str, new_path)
            safe_file_information(path_information, dir_name, file_name, count)
            return result
    except Exception as error:
        logging.error("file not removed -- {0} ".format(error))
        return error


def safe_file_information(path_information, old_path, file_name, conflict_count=1):
    info = {}
    info['oldPath'] = old_path
    info['fileName'] = file_name
    if conflict_count > 0:
        info['conflict'] = conflict_count
    else:
        info['conflict'] = 0
    with open(path_information, 'a') as files:
        json.dump(info, files)
        files.write('\n')


def del_by_regex(regex, path_basket, path_information, dry_run=False, confirm=False):
    files = glob.glob(regex)
    for f in files:
        result = del_file(path_basket, path_information, f, dry_run, confirm)
        return result


def update_basket(path_basket, path_information):
    try:
        listdir = os.listdir(path_basket)
        files = open(path_information, "r")
        lines = files.readlines()
        files.close()
        with open(path_information, "w") as fp:
            for line in lines:
                info = json.loads(line)
                for file_name_dir in listdir:
                    if info['conflict'] < 1:
                        if file_name_dir == info['fileName']:
                            json.dump(info, fp)
                            fp.write('\n')
                    else:
                        if file_name_dir == "{0}.{1}".format(info['fileName'], info['conflict']):
                            json.dump(info, fp)
                            fp.write('\n')
        return "basket is updated"
    except Exception as error:
        return error


def restore_file(path_basket, path_information, name, dry_run=False, confirm=False):
    # log.set_logger_level(log.INFO)
    # log.debug("Restoring file '{}'...".format(name))
    # import setuptools
    # import
    try:
        check_confirm(confirm)
        my_file = open(path_information, "r")
        lines = my_file.readlines()
        target = 0
        count = 0
        for line in lines:
            info = json.loads(line)
            count += 1
            if info['fileName'] == name:
                target = count
                if dry_run is True:
                    return path_basket + name + "  Was recovered"
        if target < 1:
            return "File not found"
        my_file.close()
        result = ""
        with open(path_information, 'w') as fp:
            count = 0
            for line in lines:
                count += 1
                info = json.loads(line)
                if count == target:
                    print info['fileName']
                    old_name = info['oldPath'] + '/' + name
                    if info['conflict'] > 0:
                        os.rename("{0}.{1}".format(path_basket + name, info['conflict']), old_name)
                    else:
                        os.rename(path_basket + name, old_name)
                    logging.info("{0} file recovered".format(old_name))
                    result = old_name + " size:" + str(os.path.getsize(old_name)) + " recovered successfully"
                else:
                    json.dump(info, fp)
                    fp.write('\n')
        return result
    except Exception as error:
        logging.error(error)
        return error


def get_size_basket(path_basket):
    size = 0
    for d, dirs, files in os.walk(path_basket):
        for file in files:
            file_path = os.path.join(d, file)
            size += os.path.getsize(file_path)
    return size


def clean_basket(path_basket, path_information, dry_run=False, confirm=False):
    check_confirm(confirm)
    try:
        for file in os.listdir(path_basket):
            file_removed = os.path.join(path_basket, file)
            if os.path.isdir(file_removed):
                if dry_run is True:
                    print (shutil.rmtree, "was deleting")
                else:
                    shutil.rmtree(file_removed)
            else:
                if dry_run is True:
                    print (shutil.rmtree, "was deleting")
                else:
                    os.remove(file_removed)
        info_removed = open(path_information, "w")
        info_removed.close()
        logging.info("basket is clean")
        return "basket is clean"
    except Exception as error:
        logging.error(error)
        return error


def automatic_clean(path_trash, path_information, day, size):
    if datetime.datetime.today().isoweekday() == day:
        clean_basket(path_trash, path_information, False)
    if get_size_basket(path_trash) > size:
        clean_basket(path_trash, path_information, False)


def check_confirm(confirm):
    if confirm is True:
        answer = raw_input("Are you sure? y/n \n")
        if answer == "n":
            sys.exit("canceled")
        else:
            if answer != "y":
                check_confirm(confirm)


def show_basket(path_basket):
    count = 0
    for root, dirs, files in os.walk(path_basket, topdown=False):
        for name in files:
            count += 1
            print(os.path.join(root, name))
        for name in dirs:
            count += 1
            print(os.path.join(root, name))
    if count > 2:
        answer = raw_input("the basket is too large, open folder? y/n  ")
        if answer == 'y':
            os.system('xdg-open "%s"' % path_basket)
            sys.exit()


def restore_file_django(path_basket, path_information, name, conflict, dry_run=False, confirm=False):
    try:
        check_confirm(confirm)
        my_file = open(path_information, "r")
        lines = my_file.readlines()
        my_file.close()
        result = ""
        with open(path_information, 'w') as fp:
            for line in lines:
                info = json.loads(line)
                if info['fileName'] == name and info['conflict'] == conflict:
                    old_name = info['oldPath'] + '/' + name
                    if info['conflict'] > 0:
                        os.rename("{0}.{1}".format(path_basket + name, info['conflict']), old_name)
                    else:
                        os.rename(path_basket + name, old_name)
                    logging.info("{0} file recovered".format(old_name))
                    result = old_name + " size:" + str(os.path.getsize(old_name)) + " recovered successfully"
                else:
                    json.dump(info, fp)
                    fp.write('\n')
        return result
    except Exception as error:
        logging.error(error)
        return error



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("name", nargs='*', help="Delete file")
    parser.add_argument("-res", dest="restore", help="Restore")
    parser.add_argument("-u", dest="update", help="Update", action="store_true")
    parser.add_argument("-clean", dest="clean", help="Clean", action="store_true")
    parser.add_argument("-size", help="Size")
    parser.add_argument("-show", help="Show", action="store_true")
    parser.add_argument("-c", dest="confirm", help="confirm", action="store_true")
    parser.add_argument("-dry",  help="Dry Run", action="store_true")
    parser.add_argument("-reg", dest="regex", help="regex")
    parser.add_argument("-s", dest="silent", help="silent mod", action="store_true")
    args = parser.parse_args()

    config = Load_config()
    path_basket = config['trash_path']
    dry_run = config['dry']
    day = config['day']
    size = config['size']
    confirm = config['confirm']
    silent = config['silent']
    log_path = config['log_path']
    path_information = config['information_path']

    logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG,
                        filename=log_path)
    if not os.path.exists(path_basket):
        os.makedirs(path_basket)

    if args.dry:
        dry_run = True
    if args.silent:
        silent = True
    if args.confirm:
        confirm = True
    if args.size:
        size = int(args.size)
    if args.name:
        for name in args.name:
            result = del_file(path_basket, path_information, name, dry_run, confirm, silent)
            if silent is False:
                print(result)
    if args.restore:
        result = restore_file(path_basket, path_information, args.restore, dry_run, confirm)
        print result
    if args.clean:
        result = clean_basket(path_basket, path_information, dry_run, confirm)
        print result
    if args.update:
        result = update_basket(path_basket, path_information)
        print result
    if args.regex:
        result = del_by_regex(args.regex, path_basket, path_information, dry_run, confirm)
        print result
    if args.show:
        show_basket(path_basket)

    automatic_clean(path_basket, path_information, day, size)

if __name__ == '__main__':
    main()

"""    try:
        _check_confirm(confirm)
        file = open(path_information, "r")
        lines = file.readlines()
        target = 0
        count = 0
        conf_count = 0
        end_conflict = 0
        not_conflict = 0
        for line in lines:
            info = json.loads(line)
            count += 1
            if info['fileName'] == name:
                not_conflict = count
                if dry_run is True:
                    return path_basket + name + "  Was recovered"
                if info['fileName'] == name and info['conflict'] > 0:
                    conf_count += 1
                    print "{0}. {1} , old path = {2}".format(info['conflict'], info['fileName'], info['oldPath'])
                    end_conflict = count
        if conf_count > 0:
            target = raw_input("{0}. {1} , old path = {2} \nchoose you file".format(conf_count+1, name, info['oldPath']))
            count = end_conflict - conf_count + int(target)
        else:
            count = not_conflict
        it = lines.__getitem__(count - 1)
        it = json.loads(it)
        filenam = it['fileName']
        print filenam
        file.close()
        result = ""
        with open(path_information, 'w') as fp:
            new_count = 0
            for line in lines:
                new_count += 1
                info = json.loads(line)
                if new_count == count:
                    print info['fileName']
                    old_name = info['oldPath'] + '/' + name
                    os.rename("{0}.{1}".format(path_basket + name, target), old_name)
                    logging.info("{0} file recovered".format(old_name))
                    result = old_name + " size:" + str(os.path.getsize(old_name)) + " recovered successfully"
                else:
                    json.dump(info, fp)
                    fp.write('\n')
        return result
    except Exception as error:
        logging.error(error)
        return error"""