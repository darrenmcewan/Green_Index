def show_resources(state='AK'):
    import pandas as pd
    def make_clickable(link):
        url = link.split('#')[1]
        name = link.split('#')[0]

        return f'<a target="_blank" href="{url}">{name}</a>'

    data = pd.read_csv('data/state_incentives.csv', index_col=False)
    data = data[data['State'] == state]
    data['name_url'] = data['Name'] + "#" + data['URL']
    data['Program Name'] = data['name_url'].apply(make_clickable)
    data = data.iloc[:, [7, 3, 4, 5]]
    data = data.to_html(escape=False)

    return data


