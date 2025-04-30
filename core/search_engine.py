import ctypes
import struct
import datetime
from pathlib import Path

# ----- Constants for Everything flags -----
EVERYTHING_REQUEST_FILE_NAME = 0x00000001
EVERYTHING_REQUEST_PATH = 0x00000002
EVERYTHING_REQUEST_SIZE = 0x00000010
EVERYTHING_REQUEST_DATE_MODIFIED = 0x00000040

# ----- Load DLL -----
everything_dll = ctypes.WinDLL("E:\\Projects\\RealProjects\\Creative\\Python\\MyAgent\\config\\SearchEngine\\dll\\Everything64.dll")

everything_dll.Everything_SetSearchW.argtypes = [ctypes.c_wchar_p]
everything_dll.Everything_GetResultDateModified.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ulonglong)]
everything_dll.Everything_GetResultSize.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_ulonglong)]
everything_dll.Everything_GetResultFullPathNameW.argtypes = [ctypes.c_int, ctypes.c_wchar_p, ctypes.c_int]
everything_dll.Everything_GetResultFullPathNameW.restype = ctypes.c_int

# ----- Time converter -----
def convert_filetime_to_datetime(filetime):
    WINDOWS_TICKS = int(1 / 10**-7)
    WINDOWS_EPOCH = datetime.datetime(1601, 1, 1)
    winticks = filetime.value
    microsecs = winticks / WINDOWS_TICKS
    return WINDOWS_EPOCH + datetime.timedelta(seconds=microsecs)


def build_search_query(keywords: list[str], allowed_paths = "C:\\", type_name = None) -> str:
    query_parts = []

    for key in keywords:
        query_parts.append(f"{allowed_paths} type:{type_name} {key}")
    
    # همه چی رو با OR ترکیب کن
    final_query = " | ".join(query_parts)

    print(f"[DEBUG] Final Query: {final_query}")  
    return final_query


# ----- File search function -----
def search_raw_files(keywords: list[str], typing: str , max_results: int = 1000) -> list[dict]:
    query = build_search_query(keywords=keywords, type_name=typing)

    everything_dll.Everything_SetSearchW(query)
    everything_dll.Everything_SetRequestFlags(
        EVERYTHING_REQUEST_FILE_NAME | EVERYTHING_REQUEST_PATH | EVERYTHING_REQUEST_SIZE | EVERYTHING_REQUEST_DATE_MODIFIED
    )
    everything_dll.Everything_QueryW(True)

    num_results = min(everything_dll.Everything_GetNumResults(), max_results)

    filename_buf = ctypes.create_unicode_buffer(260)
    date_modified = ctypes.c_ulonglong(1)
    file_size = ctypes.c_ulonglong(1)

    results = []

    for i in range(num_results):
        everything_dll.Everything_GetResultFullPathNameW(i, filename_buf, 260)
        everything_dll.Everything_GetResultDateModified(i, ctypes.byref(date_modified))
        everything_dll.Everything_GetResultSize(i, ctypes.byref(file_size))

        full_path = Path(filename_buf.value)
        results.append({
            "name": full_path.name,
            "path": str(full_path),
            "size": file_size.value,
            # "modified": convert_filetime_to_datetime(date_modified)
        })

    return results



# ----- File search function -----
from pprint import pprint

if __name__ == "__main__":
    # folders = search_files(['telegram'], max_results=10000, type_name=['exe'])
    # pprint(folders)
    print(search_raw_files(["telegram"], "app"))
    
    