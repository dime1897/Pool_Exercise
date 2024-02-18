from flask import Flask, render_template, request
from pool import Pool
from flask_restful import Resource, Api
import datetime

app = Flask(__name__,
            static_url_path='/static', 
            static_folder='static')
dao=Pool()

api = Api(app)
basePath = '/api/v1'
time_gap = ['08-10', '10-12', '12-14', '14-16', '16-18', '18-20']

def validate_user(user:str) -> bool:
    user = user.split('-')
    if (len(user)!=5) or (len(user[0])!=8) or (len(user[1])!=4) or (len(user[2])!=4) or (len(user[3])!=4) or (len(user[4])!=12):
        return False
    return True

def validate_date(date:str) -> bool:
    try:
        new_date = datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except Exception as e:
        print(e)
        return False

def validate_time(time:str) -> bool:
    if not time in time_gap:
        return False
    return True

def get_time_gap() -> str:
    now = int(str(datetime.datetime.now().time()).split(":")[0])
    for gap in time_gap:
        hours = gap.split("-")
        if now>=int(hours[0]) and now <=int(hours[1]):
            return gap

class Pool_Management(Resource):
    def get(self, user, date):
        if validate_user(user) and validate_date(date):
            reservation = dao.get_reservation(user,date)
            if not reservation is None: return reservation,200
        return None, 404
        
    def post(self, user, date):
        if not validate_user(user) or not validate_date(date):
            return None, 400
        input = request.json
        if isinstance(input, dict):
            if not 'time' in input.keys():
                return None, 400
            if not dao.get_reservation(user, date) is None:
                return None, 409
            if validate_time(input['time']):
                ret=dao.insert_reservation(user,date,input['time'])
                if ret is None:
                    return None, 412
                return ret, 201
        else:
            ret = []
            for reservation in input:
                if list(reservation.keys()) != ['date', 'time']:
                    return None, 400
                if validate_date(reservation['date']) and validate_time(reservation['time']):
                    if not dao.get_reservation(user, reservation['date']) is None:
                        continue
                    result = dao.insert_reservation(user, reservation['date'], reservation['time'])
                    if not result is None:
                        ret.append(result)
            if len(ret) == 0:
                return None, 400
            return ret, 201

class Pool_Status(Resource):
    def get(self, date):
        if not validate_date(date): return None, 400
        status = dao.get_pool_state(date)
        if status is None: return None, 404
        else: return status, 201

@app.route(f'{basePath}/<date>', methods = ['GET'])
def get_actual_state(date):
    if not validate_date(date):
        return render_template('404.html'), 404
    day = dao.get_pool_state(date)
    time = get_time_gap()
    print(time)
    return render_template('pool.html', time=time, users=day[time], lanes=['1','2','3','4','5','6','7','8']), 200


api.add_resource(Pool_Management, f'{basePath}/<string:user>/<string:date>')
api.add_resource(Pool_Status, f'{basePath}/<string:date>')

if __name__ == '__main__':
    app.run()