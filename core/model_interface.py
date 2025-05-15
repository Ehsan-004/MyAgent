from config.model import client
from pprint import pprint
import json


def parse_model_response(response_str: str) -> dict:
    try:
        return json.loads(response_str)
    except Exception:
        return {
            "status": "error",
            "error": "Model response is not valid JSON.",
            "raw": response_str
        }


def query_model(message: str) -> dict:
    system_prompt = """تو باید به کاربر کمک کنی تا فایل یا فایل ها و عملی که کاربر میخواهد انجام دهد مشخص شود
دقت کن که کاربر ممکن است غلط املایی داشته باشد، انها را تا جایی که میتوانی اصلاح کن.
اگر که کاربر اسامی خاصی را به فارسی بیان کرد تو نسخه انگلیسی آنها را هم برگردان مثلا:
کاربر میگوید سریال فرندز - تو باید freinds را هم برگردانی
یک شی json با این فیلد ها برگردان
{
  "status": "ok",
  "action": "delete | move | play | open(just files except video and image) | rename | run(applications) | cdir(open directory)",
  "type": "video | pic | audio | app | folder",
  "keys": [یک لیست از کلمات کلیدی که کاربر گفته است، کلمات مهم را جدا کن و هر آیتم فقط یک کلمه باشد],
}

If a keyword contains a number (for example "Season 3"), 
just **add** the number **as a separate keyword**.

Example:
Input: play friends season 3 episode 5
Output: ["friends", "3", "5"]

Only important keywords, no combinations.
Respond only with a valid JSON. No explanations.
اگر دیدی کاربر دارد با تو گفتگو میکند آن را ادامه بده و با او به صورتی امن گفتگو کن و در این قالب جواب بده:
{
    status="ok",
    action= "conversation",
    responce="جواب صمیمی به گفتگو"
}
"""

    response = client.chat.completions.create(
        model="rhino",  # یا هر مدل دیگه‌ای که داری
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        temperature=0.3
    )

    content = response.choices[0].message.content.strip()
    return parse_model_response(content.strip("`json").strip("`"))


def extract_best_match(file_names, user_prompt):
    
    enumerated_list = "\n".join([f"{i}. {name}" for i, name in enumerate(file_names)])
    
    system_prompt = """
    تو یک دستیار هوشمند هستی که باید از بین لیستی از عنوان‌ها، نزدیک‌ترین عنوان به چیزی که کاربر خواسته است را برگردانی.
    لیست شامل فایل‌هایی شماره‌گذاری‌شده به شکل "شماره. نام فایل" است.
    قالب جواب به اینصورت است:
    {
        status="ok",
        index = "شماره ایندکس فایل (عدد صحیح)",
        path = "نام کامل فایلی که تطابق کامل را دارد"  
    }
    اگر که نام نزدیک و مناسبی پیدا نکردی status="error" برگردان و در error= به اینصورت ذکر کن که چرا خطا وجود دارد
    {
        status="error",
        response="متنی برای راهنمایی کاربر"
    }
    فقط و فقط مطابق همین قالب خروجی بده. هیچ توضیح اضافه ننویس.
    """
    
    message = f"""
    کاربر گفته است: {user_prompt}
    لیست فایل ها: 
    {enumerated_list}"""
    
    response = client.chat.completions.create(
        model="rhino",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()
    return parse_model_response(content.strip("`json").strip("`"))


if __name__ == "__main__":
    # msg = "delete friends episode 3 season 4"
    # result = query_model(msg)
    # pprint(result)
    # print(query_model("سلام تو میتونی صدا رو به متن تبدیل کنی؟"))
    a = ['01_creativity_for_all_445x239.mp4', 
         'A001_C037_0921FG_001.mp4', 
         'A001_C064_09224Y_001.mp4', 
         'A002_C009_092221_001.mp4', 
         'A002_C018_0922BW_001.mp4', 
         'A002_C018_0922BW_002.mp4', 'A002_C052_0922T7_001.mp4', 'A002_C076_0922S1_001.mp4', 'A002_C086_09220G_001.mp4', 'A003_C021_0923NJ_001.mp4', 'A003_C092_09231C_001.mp4', 'A004_C002_09244Q_001.mp4', 'A004_C010_0924AL_001.mp4', 'A005_C029_0925TO_001.mp4', 'A005_C037_09255G_001.mp4', 'A005_C049_09253L_001.mp4', 'A005_C052_0925BL_001.mp4', 'Chrome2-HUCOCIY4.mp4', 'Edge2-KNQF5TSI.mp4', 'Friends.S03E02.BluRay.720p.x264.mkv', 'Friends.S03E03.BluRay.720p.x264.mkv', 'Friends.S03E04.BluRay.720p.x264.mkv', 'input-translation-demo-P2CUZKFF.mp4', 'offline-video_9ff1a430b8d1fb095a75666ce8bc22e0.mp4', 'offline-video_9ff1a430b8d1fb095a75666ce8bc22e0.mp4', 'OneNoteFirstRunCarousel_Animation2.mp4', 'people_fre_motionAsset_p2.mp4', 'people_fre_motionAsset_p2.mp4']
    print(extract_best_match(a, "سلام قسمت 2 از فصل 3 سریال  friends رو برام پخش کن"))
    
    