from config.model import client
from core.model_interface import extract_best_match

if __name__ == "__main__":
    a = ['01_creativity_for_all_445x239.mp4', 
         'A001_C037_0921FG_001.mp4', 
         'A001_C064_09224Y_001.mp4', 
         'A002_C009_092221_001.mp4', 
         'A002_C018_0922BW_001.mp4', 
         'A002_C018_0922BW_002.mp4', 'A002_C052_0922T7_001.mp4', 'A002_C076_0922S1_001.mp4', 'A002_C086_09220G_001.mp4', 'A003_C021_0923NJ_001.mp4', 'A003_C092_09231C_001.mp4', 'A004_C002_09244Q_001.mp4', 'A004_C010_0924AL_001.mp4', 'A005_C029_0925TO_001.mp4', 'A005_C037_09255G_001.mp4', 'A005_C049_09253L_001.mp4', 'A005_C052_0925BL_001.mp4', 'Chrome2-HUCOCIY4.mp4', 'Edge2-KNQF5TSI.mp4', 'Friends.S03E02.BluRay.720p.x264.mkv', 'Friends.S03E03.BluRay.720p.x264.mkv', 'Friends.S03E04.BluRay.720p.x264.mkv', 'input-translation-demo-P2CUZKFF.mp4', 'offline-video_9ff1a430b8d1fb095a75666ce8bc22e0.mp4', 'offline-video_9ff1a430b8d1fb095a75666ce8bc22e0.mp4', 'OneNoteFirstRunCarousel_Animation2.mp4', 'people_fre_motionAsset_p2.mp4', 'people_fre_motionAsset_p2.mp4']
    
    res = extract_best_match(a, "سلام قسمت 2 از فصل 3 سریال  friends رو برام پخش کن")
    print(res)
    print("found: " + a[int(res['index'])])
    print(a[17])
    print(a[18])
    print(a[19])

