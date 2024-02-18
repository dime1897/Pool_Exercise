from google.cloud import firestore
import datetime
import json

class Pool(object):
    def __init__(self) -> None:
        self.db = firestore.Client()
        #self.clean_db()
        self.lane_order = [4, 5, 3, 6, 2, 7, 1, 8]
        self.time_gap = ['08-10', '10-12', '12-14', '14-16', '16-18', '18-20']

    def insert_reservation(self, user:str, date:str, time:str) -> list:
        ref = self.db.collection('pool')
        doc_ref = ref.document(date).get()
        reservations = {}
        official_lane = -1
        if doc_ref.exists:
            reservations = doc_ref.to_dict()
            if len(reservations[time].keys()) != 8:
                official_lane = str(self.lane_order[len(reservations[time].keys())])
                reservations[time][official_lane]=[user]
            else:
                for lane in self.lane_order:
                    if len(reservations[time][str(lane)]) < 2:
                        official_lane = str(lane)
                        reservations[time][official_lane].append(user)
                        break
        else:
            for gap in self.time_gap:
                reservations[gap] = {}
            official_lane = str(self.lane_order[0])
            reservations[time][official_lane] = [user]
        if official_lane == -1:
            return None
        ref.document(date).set(reservations)
        recap = {
            'date': date,
            'lane': official_lane,
            'time': time
        }
        return recap

    def insert_multiple_reservations(self, user:str, reservations:list) -> list:
        return [self.insert_reservation(user, reservation['date'], reservation['time']) for reservation in reservations]

    def get_reservation(self, user:str, date:str):
        ref = self.db.collection('pool')
        doc = ref.document(date).get()
        day = doc.to_dict() if doc.exists else None
        if day is None: return None
        for time, hour in day.items():
            for lane, users_list in hour.items():
                if user in users_list:
                    return {'date': date, 'time': time, 'lane': lane}
        return None

    def get_pool_state(self, date:str):
        ref = self.db.collection('pool')
        doc = ref.document(date).get()
        state = doc.to_dict() if doc.exists else None
        if state is None: return None
        for time, lanes in state.items():
            if len(lanes.keys())==8:
                for lane, users in lanes.items():
                    if len(users) < 2:
                        users.append("FREE_SPACE_FOR_SOMEONE")
            for lane in self.lane_order[:len(lanes.keys())]:
                lanes[str(lane)].append("FREE_SPACE_FOR_SOMEONE")
            for lane in self.lane_order[len(lanes.keys()):]:
                lanes[str(lane)]=["FREE_SPACE_FOR_SOMEONE", "FREE_SPACE_FOR_SOMEONE"]
        return state


    def clean_db(self) -> None:
        ref = self.db.collection('pool')
        doc_list = ref.list_documents()
        for doc in doc_list:
            doc.delete()

#if __name__ == '__main__':
#    dao = Pool()
#    reservations = [
#        {'date': '2024-02-22', 'time': '08-10'},
#        {'date': '2024-02-23', 'time': '10-12'},
#        {'date': '2024-02-24', 'time': '10-12'},
#        {'date': '2024-02-25', 'time': '14-16'},
#        {'date': '2024-02-26', 'time': '16-18'},
#        {'date': '2024-02-19', 'time': '10-12'},
#        {'date': '2024-02-21', 'time': '10-12'},
#        {'date': '2024-03-22', 'time': '08-10'},
#        {'date': '2024-03-23', 'time': '10-12'},
#        {'date': '2024-03-24', 'time': '12-14'},
#        {'date': '2024-02-14', 'time': '08-10'},
#        {'date': '2024-04-22', 'time': '10-12'}
#    ]
#    dao.insert_multiple_reservations('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', reservations)
#    dao.insert_reservation('9c5b94b1-35ad-49bb-b118-8e8fc24abf80', '2024-02-22', '10-12')
#    dao.insert_reservation('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '2024-02-22', '10-12')
#    dao.insert_reservation('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '2024-02-22', '10-12')
#    dao.insert_reservation('cccccccc-cccc-cccc-cccc-cccccccccccc', '2024-02-22', '10-12')
#    dao.insert_reservation('dddddddd-dddd-dddd-dddd-dddddddddddd', '2024-02-22', '10-12')
#    dao.insert_reservation('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', '2024-02-22', '10-12')
#    dao.insert_reservation('ffffffff-ffff-ffff-ffff-ffffffffffff', '2024-02-22', '10-12')
#    dao.insert_reservation('gggggggg-gggg-gggg-gggg-gggggggggggg', '2024-02-22', '10-12')
#    dao.insert_reservation('hhhhhhhh-hhhh-hhhh-hhhh-hhhhhhhhhhhh', '2024-02-22', '10-12')
#    dao.insert_reservation('iiiiiiii-iiii-iiii-iiii-iiiiiiiiiiii', '2024-02-22', '10-12')
#    dao.insert_reservation('jjjjjjjj-jjjj-jjjj-jjjj-jjjjjjjjjjjj', '2024-02-22', '10-12')
#    dao.insert_reservation('kkkkkkkk-kkkk-kkkk-kkkk-kkkkkkkkkkkk', '2024-02-22', '10-12')
#    print(dao.get_reservation('dddddddd-dddd-dddd-dddd-dddddddddddd', '2024-02-22'))