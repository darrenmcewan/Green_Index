def show_resources(state='AK'):
    import pandas as pd
    def make_clickable(link):
        text = link.split('#')[1]
        return f'<a target="_blank" href="{link}">{text}</a>'

    data = pd.read_csv('data/state_incentives.csv', index_col=False)
    data = data[data['State'] == state]
    data['name_url'] = data['Name'] + "#" + data['URL']
    data['Program Link'] = data['name_url'].apply(make_clickable)
    data = data.iloc[:, [0, 3, 4, 5, 7]]
    data = data.to_html(escape=False)

    return data


