import pandas as pd
import plotly.express as px
import mysql.connector
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Conectarse a la base de datos
conn = mysql.connector.connect(
    user='root',
    password='',
    host='localhost',
    database='datosbd'
)


# Consulta SQL para obtener los datos necesarios para el gráfico de pastel
query_pastel = "SELECT Año, Mes, SUM(Presupuesto_Dado) AS Presupuesto_Mes FROM presupuesto_anual GROUP BY Año, Mes;"
# Consulta SQL para obtener los datos necesarios para el gráfico de barras
query_barras = "SELECT Año, Mes, SUM(Presupuesto_Dado) AS Presupuesto_Mes FROM presupuesto_anual GROUP BY Año, Mes;"
# Consulta SQL para obtener los datos necesarios para el gráfico de puntos
query_puntos = "SELECT Año, Mes, SUM(Monto_Ingreso) AS Monto_Ingreso_Mes FROM ingresos_brutos GROUP BY Año, Mes;"
# Consulta SQL para obtener los datos necesarios para el gráfico de área
query_area = "SELECT Año, Mes, SUM(Inversion) AS Inversion_Mes FROM egresos_por_obras GROUP BY Año, Mes;"
# Consulta SQL para obtener los datos necesarios para el gráfico de barras de egresos a empleadores
query_barras_empleadores = "SELECT Año, Mes, SUM(Pago) AS Pago_Mes FROM egresos_pago_empleadores GROUP BY Año, Mes;"

# Consulta SQL para obtener los datos necesarios para el gráfico de pastel de porcentajes
query_pastel_porcentajes = """
    SELECT ingresos_brutos.Año, 
           SUM(ingresos_brutos.Monto_Ingreso) AS Monto_Ingreso_Acumulado, 
           SUM(presupuesto_anual.Presupuesto_Dado) AS Presupuesto_Acumulado
      FROM ingresos_brutos
           INNER JOIN presupuesto_anual
           ON ingresos_brutos.Año = presupuesto_anual.Año
      GROUP BY ingresos_brutos.Año;
"""
# Consulta SQL para obtener los datos necesarios para el gráfico de barras de porcentajes
query_barras_porcentajes = """
    SELECT egresos_pago_empleadores.Año,
           SUM(egresos_pago_empleadores.Pago) AS Pago_Acumulado,
           SUM(egresos_por_obras.Inversion) AS Inversion_Acumulada
      FROM egresos_pago_empleadores
           INNER JOIN egresos_por_obras
           ON egresos_pago_empleadores.Año = egresos_por_obras.Año
      GROUP BY egresos_pago_empleadores.Año;
"""

# Leer los datos desde la base de datos usando Pandas
df_pastel = pd.read_sql_query(query_pastel, conn)
df_barras = pd.read_sql_query(query_barras, conn)
df_puntos = pd.read_sql_query(query_puntos, conn)
df_area = pd.read_sql_query(query_area, conn)
df_barras_empleadores = pd.read_sql_query(query_barras_empleadores, conn)
df_pastel_porcentajes = pd.read_sql_query(query_pastel_porcentajes, conn)
df_barras_porcentajes = pd.read_sql_query(query_barras_porcentajes, conn)

# Cerrar la conexión a la base de datos
conn.close()

# Generar el gráfico de pastel con Plotly (Presupuesto Total por Año)
fig_pie_total = px.pie(
    df_pastel,
    names='Año',
    values='Presupuesto_Mes',
    title='Presupuesto Total por Año'
)

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Opciones para el filtro de año del gráfico de barras
opciones_anio_bar = [{'label': str(ano), 'value': ano}
                     for ano in df_barras['Año'].unique()]

# Opciones para el filtro de año del gráfico de puntos
opciones_anio_puntos = [
    {'label': str(ano), 'value': ano} for ano in df_puntos['Año'].unique()]

# Opciones para el filtro de año para el gráfico de área
opciones_anio_area = [{'label': str(ano), 'value': ano}
                      for ano in df_area['Año'].unique()]

# Opciones para el filtro de año para el gráfico de barras de egresos a empleadores
opciones_anio_barras_empleadores = [{'label': str(
    ano), 'value': ano} for ano in df_barras_empleadores['Año'].unique()]


# Opciones para el filtro de año para el gráfico de pastel de porcentajes
opciones_anio_pastel_porcentajes = [{'label': str(
    ano), 'value': ano} for ano in df_pastel_porcentajes['Año'].unique()]

# Opciones para el filtro de año para el gráfico de barras de porcentajes
opciones_anio_barras_porcentajes = [{'label': str(
    ano), 'value': ano} for ano in df_barras_porcentajes['Año'].unique()]


# Diseño del dashboard
app.layout = html.Div(children=[
    html.H1('Dashboard GAD Parroquial de Barbones', style={
        'marginBottom': '30px', 'paddingLeft': '160px'}),
    html.Div([
        dcc.Graph(
            id='pie-chart-total',
            figure=fig_pie_total,
            style={'width': '60%', 'height': '400px'}
        )
    ]),
    html.Div([
        dcc.Dropdown(
            id='filtro-anio-bar',
            options=opciones_anio_bar,
            value=df_barras['Año'].max(),
            style={'width': '30%', 'marginRight': '20px'}
        ),
        dcc.Graph(
            id='bar-chart',
            style={'width': '65%', 'height': '400px',
                   'display': 'inline-block'}
        )
    ]),
    html.Div([
        dcc.Dropdown(
            id='filtro-anio-puntos',
            options=opciones_anio_puntos,
            value=df_puntos['Año'].max(),
            style={'width': '30%', 'marginRight': '20px'}
        ),
        dcc.Graph(
            id='scatter-chart',
            style={'width': '65%', 'height': '400px',
                   'display': 'inline-block'}
        )
    ]),
    html.Div([
        dcc.Dropdown(
            id='filtro-anio-area',
            options=opciones_anio_area,
            value=df_area['Año'].max(),
            style={'width': '30%', 'marginRight': '20px'}
        ),
        dcc.Graph(
            id='area-chart',
            style={'width': '65%', 'height': '400px',
                   'display': 'inline-block'}
        )
    ]),
    html.Div([
        dcc.Dropdown(
             id='filtro-anio-barras-empleadores',
             options=opciones_anio_barras_empleadores,
             value=df_barras_empleadores['Año'].max(),
             style={'width': '30%', 'marginRight': '20px'}
             ),
        dcc.Graph(
            id='barras-empleadores-chart',
            style={'width': '65%', 'height': '400px',
                   'display': 'inline-block'}
        )
    ]), html.Div([
        dcc.Dropdown(
            id='filtro-anio-pastel-porcentajes',
            options=opciones_anio_pastel_porcentajes,
            value=df_pastel_porcentajes['Año'].max(),
            style={'width': '30%', 'marginRight': '20px'}
        ),
        dcc.Graph(
            id='pastel-porcentajes-chart',
            style={'width': '65%', 'height': '400px',
                   'display': 'inline-block'}
        )
    ]), html.Div([
        dcc.Dropdown(
            id='filtro-anio-barras-porcentajes',
            options=opciones_anio_barras_porcentajes,
            value=df_barras_porcentajes['Año'].max(),
            style={'width': '30%', 'marginRight': '20px'}
        ),
        dcc.Graph(
            id='barras-porcentajes-chart',
            style={'width': '65%', 'height': '400px',
                   'display': 'inline-block'}
        )
    ])
], style={'paddingLeft': '20%'})


# Callback para actualizar el gráfico de barras al cambiar el filtro de año


@app.callback(
    Output('bar-chart', 'figure'),
    [Input('filtro-anio-bar', 'value')]
)
def update_figure_bar(selected_year):
    # Filtrar el DataFrame por el año seleccionado
    df_barras_filtered = df_barras[df_barras['Año'] == selected_year]

    # Actualizar el gráfico de barras
    fig_bar = px.bar(
        df_barras_filtered,
        x='Mes',
        y='Presupuesto_Mes',
        barmode='group',
        title='Presupuesto por mes y año'
    )

    return fig_bar

# Callback para actualizar el gráfico de puntos al cambiar el filtro de año


@app.callback(
    Output('scatter-chart', 'figure'),
    [Input('filtro-anio-puntos', 'value')]
)
def update_figure_scatter(selected_year):
    # Filtrar el DataFrame por el año seleccionado
    df_puntos_filtered = df_puntos[df_puntos['Año'] == selected_year]

    # Actualizar el gráfico de puntos
    fig_scatter = px.scatter(
        df_puntos_filtered,
        x='Mes',
        y='Monto_Ingreso_Mes',
        title='Ingresos brutos por mes y año',
    )
    return fig_scatter


# Callback para actualizar el gráfico de área al cambiar el filtro de año
@app.callback(
    Output('area-chart', 'figure'),
    [Input('filtro-anio-area', 'value')]
)
def update_figure_area(selected_year_area):
    # Filtrar el DataFrame por el año seleccionado para el gráfico de área
    df_area_filtered = df_area[df_area['Año'] == selected_year_area]

    # Actualizar el gráfico de área
    fig_area = px.area(
        df_area_filtered,
        x='Mes',
        y='Inversion_Mes',
        title='Inversion de obras por mes'
    )
    return fig_area

# Callback para actualizar el gráfico de barras de egresos a empleadores al cambiar el filtro de año


@app.callback(
    Output('barras-empleadores-chart', 'figure'),
    [Input('filtro-anio-barras-empleadores', 'value')]
)
def update_figure_barras_empleadores(selected_year_barras_empleadores):
    # Filtrar el DataFrame por el año seleccionado para el gráfico de barras de egresos a empleadores
    df_barras_empleadores_filtered = df_barras_empleadores[
        df_barras_empleadores['Año'] == selected_year_barras_empleadores]

    # Actualizar el gráfico de barras de egresos a empleadores
    fig_barras_empleadores = px.bar(
        df_barras_empleadores_filtered,
        x='Mes',
        y='Pago_Mes',
        barmode='group',
        title='Egresos de Pago a Empleadores por Mes y año'
    )

    return fig_barras_empleadores

# Callback para actualizar el gráfico de pastel de porcentajes al cambiar el filtro de año


@app.callback(
    Output('pastel-porcentajes-chart', 'figure'),
    [Input('filtro-anio-pastel-porcentajes', 'value')]
)
def update_figure_pastel_porcentajes(selected_year_pastel_porcentajes):
    # Filtrar el DataFrame por el año seleccionado para el gráfico de pastel de porcentajes
    df_pastel_porcentajes_filtered = df_pastel_porcentajes[
        df_pastel_porcentajes['Año'] == selected_year_pastel_porcentajes]

    # Calcular los porcentajes de Monto_Ingreso_Acumulado y Presupuesto_Acumulado
    total_monto_ingreso = df_pastel_porcentajes_filtered['Monto_Ingreso_Acumulado'].sum(
    )
    total_presupuesto = df_pastel_porcentajes_filtered['Presupuesto_Acumulado'].sum(
    )
    porcentaje_monto_ingreso = (
        total_monto_ingreso / (total_monto_ingreso + total_presupuesto)) * 100
    porcentaje_presupuesto = (
        total_presupuesto / (total_monto_ingreso + total_presupuesto)) * 100

    # Actualizar el gráfico de pastel de porcentajes
    fig_pastel_porcentajes = px.pie(
        values=[porcentaje_monto_ingreso, porcentaje_presupuesto],
        names=['Monto_Ingreso', 'Presupuesto'],
        title='Porcentajes de Monto_Ingreso y Presupuesto por Año'
    )

    return fig_pastel_porcentajes


# Callback para actualizar el gráfico de barras de porcentajes al cambiar el filtro de año
@app.callback(
    Output('barras-porcentajes-chart', 'figure'),
    [Input('filtro-anio-barras-porcentajes', 'value')]
)
def update_figure_barras_porcentajes(selected_year_barras_porcentajes):
    # Filtrar el DataFrame por el año seleccionado para el gráfico de barras de porcentajes
    df_barras_porcentajes_filtered = df_barras_porcentajes[
        df_barras_porcentajes['Año'] == selected_year_barras_porcentajes]

    # Calcular los porcentajes de Pago_Acumulado e Inversion_Acumulada
    total_pago = df_barras_porcentajes_filtered['Pago_Acumulado'].sum()
    total_inversion = df_barras_porcentajes_filtered['Inversion_Acumulada'].sum(
    )
    porcentaje_pago = (total_pago / (total_pago + total_inversion)) * 100
    porcentaje_inversion = (
        total_inversion / (total_pago + total_inversion)) * 100

    # Actualizar el gráfico de barras de porcentajes
    fig_barras_porcentajes = px.bar(
        x=['Pago', 'Inversion'],
        y=[porcentaje_pago, porcentaje_inversion],
        title='Porcentajes de Pago e Inversion por Año'
    )

    return fig_barras_porcentajes


if __name__ == '__main__':
    app.run_server(debug=True)
