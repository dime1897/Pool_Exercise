from google.cloud import firestore
import datetime

db = firestore.Client()

def get_time_gap(time_gap) -> str:
    now = int(str(datetime.datetime.now().time()).split(":")[0])
    for gap in time_gap:
        hours = gap.split("-")
        if now>=int(hours[0]) and now <=int(hours[1]):
            return gap
        
def get_next_time_gap(time_gap) -> str:
    now = int(str(datetime.datetime.now().time()).split(":")[0])
    index=0
    i=0
    for gap in time_gap:
        hours = gap.split("-")
        if now>=int(hours[0]) and now <=int(hours[1]):
            index= i+1
            break
        i+=1
    return time_gap[index]

def check_reservation(request) -> str:
        user = request.get_json().get('user')
        ref = db.collection('pool')
        today = '2024-02-22'#datetime.datetime.today().strftime('%Y-%m-%d')
        doc = ref.document(today).get()
        day = doc.to_dict() if doc.exists else None
        if day is None: return 'Day is None'

        now_gap = '10-12'#get_time_gap(['08-10', '10-12', '12-14', '14-16', '16-18', '18-20'])
        for lane, users in day[now_gap].items():
            if user in users: return 'True'
        next_gap = get_time_gap(['08-10', '10-12', '12-14', '14-16', '16-18', '18-20'])
        for lane, users in day[next_gap].items():
            if user in users: return 'True'

        return 'No reservation found'