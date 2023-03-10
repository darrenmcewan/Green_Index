def state_data(data):
    state_groups = data.groupby(['StateName', 'PrimSource'])
    state_dict = {}

    for (state, res_type), group in state_groups:
        if state not in state_dict:
            state_dict[state] = {}
        state_dict[state][res_type] = group[['Latitude', 'Longitude']].values.tolist()
    return state_dict


def resource_locations(data):
    wind = data[data['PrimSource'] == 'Wind'][['Latitude', 'Longitude']].values.tolist()
    water = data[data['PrimSource'] == 'Hydroelectric'][['Latitude', 'Longitude']].values.tolist()
    solar = data[data['PrimSource'] == 'Solar'][['Latitude', 'Longitude']].values.tolist()
    return wind, water, solar
