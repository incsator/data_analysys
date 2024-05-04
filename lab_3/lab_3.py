#ФБ-25 Заєць Микола
#Лабораторна робота №3

from spyre import server
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def read_csv_data(file_name):
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'area']
    df_all = pd.read_csv(file_name, header=1, names=headers, delimiter=',')
    df_all['Year'] = df_all['Year'].astype(int)
    df_all['Week'] = df_all['Week'].astype(int)
    df_all['area'] = df_all['area'].astype(int)
    return df_all

class StockExample(server.App):
    title = "data vizualization"
    inputs = [{
        'type': 'dropdown',
        'label': 'Індекси',
        'options': [
            {'label': 'VCI', 'value': 'VCI'},
            {'label': 'TCI', 'value': 'TCI'},
            {'label': 'VHI', 'value': 'VHI'}
        ],
        'value': 'VCI',
        'key': 'noaa',
        'action_id': 'update_data'
    },
        {
            'type': 'dropdown',
            "type": "dropdown",
            "label": "Області України:",
            "options": [
                {"label": "Вінницька", "value": "1"},
                {"label": "Волинська", "value": "2"},
                {"label": "Дніпропетровська", "value": "3"},
                {"label": "Донецька", "value": "4"},
                {"label": "Житомирська", "value": "5"},
                {"label": "Закарпатська", "value": "6"},
                {"label": "Запорізька", "value": "7"},
                {"label": "Івано-Франківська", "value": "8"},
                {"label": "Київська", "value": "9"},
                {"label": "Кіровоградська", "value": "10"},
                {"label": "Луганська", "value": "11"},
                {"label": "Львівська", "value": "12"},
                {"label": "Миколаївська", "value": "13"},
                {"label": "Одеська", "value": "14"},
                {"label": "Полтавська", "value": "15"},
                {"label": "Рівенська", "value": "16"},
                {"label": "Сумська", "value": "17"},
                {"label": "Тернопільська", "value": "18"},
                {"label": "Харківська", "value": "19"},
                {"label": "Херсонська", "value": "20"},
                {"label": "Хмельницька", "value": "21"},
                {"label": "Черкаська", "value": "22"},
                {"label": "Чернівецька", "value": "23"},
                {"label": "Чернігівська", "value": "24"},
                {"label": "Крим", "value": "25"}
            ],
            'value': '9',
            'key': 'regions',
            'action_id': 'update_data'
        },
        {
            "type": "text",
            "label": "Інтервал тижнів:",
            "key": "weeks",
            "value": "9-50",
            "action_id": "update_data"
        },

        {
            "type": "text",
            "label": "Інтервал років:",
            "key": "year",
            "value": "2004-2006",
            "action_id": "update_data"
        },

        # {
        #     "type":'slider',
        #     "label": 'Рік:',
        #     "min" : 1981,
        #     "max" : 2024,
        #     "key": 'year',
        #     "action_id" : "update_data"
        # },
    ]

    controls = [{"type": "hidden",
                 "id": "update_data"}]

    tabs = ['Plot', 'Table']

    outputs = [{
        'type': 'plot',
        'id': 'plot',
        'control_id': 'update_data',
        'tab': 'Plot'
    },
        {
            'type': 'table',
            'id': 'table_id',
            'control_id': 'update_data',
            'tab': 'Table',
            'on_page_load': True
        }]

    def getData(self, params):
        noaa = params['noaa']
        region = int(params['regions'])
        weeks = params['weeks']
        year = params['year']

        df_all = read_csv_data(r'C:\Users\ethan\OneDrive\Desktop\Subjects\2_semester\data_analysys\lab_2\csv_lab2\NOAA_ALL_CSV.csv')
        min_week, max_week = map(int, weeks.split("-"))
        year_min, year_max = map(int, year.split("-"))
        df = df_all[(df_all['area'] == region) &
                    (df_all['Year'] >= year_min) &
                    (df_all['Year'] <= year_max) &
                    (df_all['Week'] >= min_week) &
                    (df_all['Week'] <= max_week)][['Year',  'Week', noaa]]
        return df

    def getPlot(self, params):
        noaa = params['noaa']
        data = self.getData(params)

        plt.figure(figsize=(9, 5))
        sns.set_style("whitegrid")
        with sns.color_palette("Set2"):
            for i in data['Year'].unique():
                data2 = data[data['Year'].astype(int) == int(i)]
                print(data2)
                fig = sns.lineplot(data=data2, x='Week', y=noaa, zorder=1)

        return fig

if __name__ == '__main__':
    app = StockExample()
    app.launch(port=7474)
