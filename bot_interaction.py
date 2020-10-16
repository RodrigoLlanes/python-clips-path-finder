from clips import Environment, Symbol
import collections

def assert_dynamic(env, dynamic_data):
    data = '(dynamic robot ' + str(dynamic_data['pos'][0]) + ' ' + str(dynamic_data['pos'][1]) + ' ' + str(dynamic_data['ammo']) + ' '
    for enemy in dynamic_data['enemies']:
        data += 'enemigo ' + str(enemy[0]) + ' ' +  str(enemy[1]) + ' '
    for box in dynamic_data['boxes']:
        data += 'caja ' + str(box[0]) + ' ' + str(box[1]) + ' '
    data += 'movimiento null nivel 0 prev 0)'
    env.assert_string(data)
    
def assert_static(env, static_data):
    env.assert_string('(profundidad-maxima ' + str(static_data['max_depth']) + ')')
    env.assert_string('(tamanyo ' + str(static_data['size'][0]) + ' ' + str(static_data['size'][1]) + ')')
    for leader in static_data['leaders']:
        env.assert_string('(escalera ' + str(leader[0]) + ' ' + str(leader[1]) + ')')
    for hole in static_data['holes']:
        env.assert_string('(hueco ' + str(hole[0]) + ' ' + str(hole[1]) + ')')

def get_path(static_data, dynamic_data):
    environment = Environment()
    environment.load('resources/scripts/RobotPath.CLP')

    environment.reset()

    assert_static(environment, static_data)
    assert_dynamic(environment, dynamic_data)

    environment.run()

    _path = [ str(x)[str(x).index('(')+1:-1].split() for x in environment.find_function('camino').__call__(str(len([x for x in environment.facts()])-1))]
    path = []
    for dynamic in _path:
        dic = collections.defaultdict(lambda: [])
        for i in range(len(dynamic)):
            if dynamic[i] == 'robot':
                dic['pos'] = (int(dynamic[i+1]), int(dynamic[i+2]))
            elif dynamic[i] == 'enemigo':
                dic['enemies'].append((int(dynamic[i+1]), int(dynamic[i+2])))
            elif dynamic[i] == 'caja':
                dic['boxes'].append((int(dynamic[i+1]), int(dynamic[i+2])))
        path.append(dic)
    return path