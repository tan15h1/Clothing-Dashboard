'''
DS3500 Spring 24
Tanishi Datta and Kaydence Lin
filename: hw3_dash.py
HW3: Dashboards
main script
https://www.kaggle.com/datasets/mrsimple07/clothes-price-prediction/data
'''
from hw3_api import ClothesAPI
from clothes_objects import Clothes
from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

def main():
    # connect to database and get data from api
    api = ClothesAPI()
    materials = api.clothes_data()['material'].unique()
    categories = api.clothes_data()['category'].unique()
    sizes = ['All'] + ['XS', 'S', 'M', 'L', 'XL', 'XXL']

    # read data into database
    clothes_df = pd.read_csv('clothes_price_prediction_data.csv')

    for index, row in clothes_df.iterrows():
        clothes = Clothes(brand=row['Brand'], category=row['Category'], color=row['Color'], size=row['Size'],
                          material=row['Material'], price=row['Price'])
        api.get_clothes(clothes)

    # create dashboard
    app = Dash(__name__)

    app.layout = html.Div([
        html.H4('Athletic Clothes'),

        # material dropdown
        html.P('Select Material'),
        dcc.Dropdown(id='material_drop',options=[{'label': 'All Materials', 'value': 'All'}] + [{'label': material,
                     'value': material} for material in materials], value='All'),

        # category dropdown
        html.P('Select Category'),
        dcc.Dropdown(id='category_drop', options=[{'label': 'All Categories', 'value': 'All'}] + [{'label': category,
                    'value': category} for category in categories], value='All'),

        # boxplot
        dcc.Graph(id='boxplot'),

        html.Div([
            # size slider
            html.P('Select Size'),
            dcc.Slider(id='size_slider', min=0, max=len(sizes) - 1, step=1,
                       marks={i: sizes[i] for i in range(len(sizes))}, value=0),

            # histogram
            dcc.Graph(id='histogram')
        ])
    ])

    @app.callback(
        Output('boxplot', 'figure'),
        [Input('material_drop', 'value')],
        [Input('category_drop', 'value')]
    )

    def display_boxplot(material, category):
        '''Method to update boxplot data'''
        data = api.clothes_data(material, category)

        fig_box = px.box(data, y='price', x='brand',
                         title=f'Athletic Clothing Prices for {material} Material and {category} Category',
                         labels={'price': 'Price', 'brand': 'Brand'}, hover_data={'brand': True, 'price': True},
                         orientation='v')

        return fig_box

    @app.callback(
        Output('histogram', 'figure'),
        [Input('size_slider', 'value')]
    )

    def display_histogram(size):
        '''Method to update histogram data'''
        size_select = sizes[size]
        if size_select == 'All':
            data = clothes_df
        else:
            data = clothes_df[clothes_df['Size'] == size_select]

        fig = px.histogram(data, x='Price', color='Material', title=f'Frequency of Prices for {size_select}',
                           labels={'Price': 'Price'}, hover_data=['Brand', 'Category'])

        return fig

    app.run_server(debug=True)

if __name__ == '__main__':
    main()