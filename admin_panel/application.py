import random
import json
from service_functions import getAllData,makeLists
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
from bokeh.models.glyphs import VBar
from bokeh.plotting import figure
from bokeh.charts import Bar
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/<int:bars_count>/")
def chart(bars_count):

    data=getAllData()
    with open('response.json', 'w') as f:
        json.dump(data,f)

    date,success,fail,interval=makeLists('response.json',bars_count)
    test=[]

    for i in range(1,len(success)+1):
        test.append(i)

    data={"date":date,"success":success,"fail":fail,"interval":interval,"test":test}
    
    hover= create_hover_tool(True)
    color_sc = "#008000"
    plot_sc = create_bar_chart(data, "", "test", "success", hover, color_sc)
    script_sc, div_sc = components(plot_sc)

    hover_f = create_hover_tool(False)
    color_f="#e12127"
    plot_f = create_bar_chart(data, "", "test", "fail", hover_f, color_f)
    script_f, div_f = components(plot_f)


    return render_template("chart.html", bars_count=bars_count,
                           the_div_s=div_sc, the_script_s=script_sc,the_div_f=div_f,the_script_f=script_f)
def create_hover_tool(success):
    """Generates the HTML for the Bokeh's hover data tool on our graph."""
    if success:
        hover_html = """
      <div>
        <span class="hover-tooltip">@date</span>
      </div>
      <div>
        <span class="hover-tooltip">@interval<span>

      </div>
      <div>
        <span class="hover-tooltip">@success</span>
      </div>
        """
    else:
         hover_html = """
      <div>
        <span class="hover-tooltip">@date</span>
      </div>
      <div>
        <span class="hover-tooltip">@interval<span>

      </div>
      <div>
        <span class="hover-tooltip">@fail</span>
      </div>
        """

    return HoverTool(tooltips=hover_html)



def create_bar_chart(data, title, x_name, y_name, hover_tool=None, color=None, width=1200, height=300):
    
    """Создаёт столбчатую диаграмму.
        Принимает данные в виде словаря, подпись для графика,
        названия осей, шаблон подсказки при наведении, цвет.
    """
    source = ColumnDataSource(data)
    xdr = FactorRange(factors=data[x_name])
    ydr = Range1d(start=0,end=max(data[y_name])*1.5)

    tools = []
    if hover_tool:
        tools = [hover_tool,]

    plot = figure(title=title, x_range=xdr, y_range=ydr, plot_width=width,
                  plot_height=height, h_symmetry=False, v_symmetry=False,
                  min_border=0, toolbar_location="above", tools=tools,
                  responsive=True, outline_line_color="#666666")

    glyph = VBar(x=x_name, top=y_name, bottom=0, width=.8,
                 fill_color=color)
    #e12127 
    plot.add_glyph(source, glyph)

    xaxis = LinearAxis()
    yaxis = LinearAxis()

    plot.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    plot.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    plot.toolbar.logo = None
    plot.min_border_top = 0
    plot.xgrid.grid_line_color = None
    plot.ygrid.grid_line_color = "#999999"
    plot.yaxis.axis_label = "Work"
    return plot
if __name__ == "__main__":
    app.run(host='0.0.0.0',port='5030')
