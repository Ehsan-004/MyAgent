from core.model_interface import query_model, extract_best_match
from core.search_engine import search_files
from datetime import datetime
import os


def handle(user_command):
    res = query_model(user_command)
    print("------------------------------")
    print(res)
    if res['status'] != 'ok':
        print("[debug] status is not ok.")
        return 'یه چیزی مشکل داره مشتی اینم متن خطا ' + res['error']
    
    action = res['action']
    if action == 'run':
        print('[debug] action is run')
        
        found_files_paths = search_files(res['keys'], res['type'])
        if len(found_files_paths) == 0:
            print('[debug] search engine found nothing')
            return 'این برنامه پیدا نشد'
        
        print('[debug] trying to find best match')
        
        files_names = [fn.name for fn in found_files_paths]
        
        result = extract_best_match(files_names, user_command)
        if result['status'] != 'ok':
            print('[debug] no file found reason is: ' + result['reason']) 
            return result['reason']
        
        print('[debug] found the file')
        path = str(found_files_paths[int(result['index'])])
        print('[debug] path of file is: ' + path)
        os.startfile(path)
        return path
    elif action == 'play':
        print('[debug] action is play')
        found_files_paths = search_files(res['keys'], res['type'])
        if len(found_files_paths) == 0:
            print('[debug] search engine found nothing')
            return 'متاسفانه نتونستم چیزی برات پیدا کنم'
        
        print('[debug] trying to find best match')
        
        files_names = [fn.name for fn in found_files_paths]
        
        result = extract_best_match(files_names, user_command)
        if result['status'] != 'ok':
            print('[debug] no file found reason is: ' + result['reason']) 
            return result['response']
        
        print('[debug] found the file')
        path = str(found_files_paths[int(result['index'])])
        print('[debug] path of file is: ' + path)
        os.startfile(path)
        return path
    elif action == "cdir":
        print('[debug] action is cdir')
        found_files_paths = search_files(res['keys'], res['type'])
        if len(found_files_paths) == 0:
            print('[debug] search engine found nothing')
            return 'متاسفانه نتونستم چیزی برات پیدا کنم'
        
        print('[debug] trying to find best match')
        
        files_names = [fn.name for fn in found_files_paths]
        
        result = extract_best_match(files_names, user_command)
        if result['status'] != 'ok':
            print('[debug] no file found reason is: ' + result['reason']) 
            return result['response']
        
        print('[debug] found the file')
        path = str(found_files_paths[int(result['index'])])
        print('[debug] path of file is: ' + path)
        os.startfile(path)
        return path
    elif action == "conversation":
        print("[debut] conversation detected")
        return res["responce"]
    
    return "یک دستور ناشناخته یا مشکل دیگر وجود دارد"
