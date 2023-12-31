"""
MIT License

Copyright (c) 2023 William A Pringle

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from browser import document, html, alert
from browser.html import * 
from browser.widgets.dialog import InfoDialog
from aq_data import decade_index, decade_data

import brycharts

testing = False

def TRTD(*args,**kwargs):
    return TR(TD(*args, **kwargs))

def init():
    """
    Present list of cities.
    Select up to 3 and show in separate list - chosen
    Go button when  done
    Cant select city if in chosen list
    Cant select city if chosen full
    Cant press go button if chosen empty
    City can be deleted from chosen list
    """
    choices = ["one","two","three","four","five", "six", "seven"]
    
    city_list = SELECT(id="city_list", size=10, multiple=True, Class="select_list")
    for item in decade_index:
        city_list <= OPTION(item)
        
    select = BUTTON("+", disabled=True, Class="selector")
    
    chosen = SELECT(size=3, Class="select_list")
    
    remove = BUTTON("-", disabled=True, Class="selector")
    
    go = BUTTON("Compare", disabled=not testing, Class="selector")
    

    def layout():
        paragraph1 = """
Data is the concentration of particulate matter (e.g. soot particles) extracted from the UK Earth System  Model and averaged per decade. 
"""

        inner = DIV(
            select+
            remove
        )
        
        main= DIV(
            DIV(
            SVG(style={"width": "95%", "height": "45%", "background-color": "white",}), Class="chart"), 
            id="chartarea",xstyle={"width": "100%", "height": "100%"})  

        document <=  DIV(
            DIV(
                DIV(H1("Compare Historic Air Pollution Between Cities")) + 
                P(paragraph1) +
                P("Select up to 3 cities for Comparison using the + button. Remove from selection using the - button. Use the Compare button to generate graph.") + 
                P("Click " + A("here", href="../aqcity/topten.html") + " to track top ten cities through time."), 
                
                Class="header"
            )+
            TABLE(
                TR(
                    TD(
                        SPAN("Cities to Compare") +
                        DIV(city_list, id="city_list")+
                        DIV(inner) + 
                        DIV("Selected Cities") +
                        DIV(chosen) + DIV(go),
                        Class="td_left"
                    ) +
                    TD(main)
                    ),
                Class="body"
                ),
            Class="background"
            )

    def already_chosen():
        chosen_values = [v.value for v in chosen.options]
        candidate = city_list.selectedIndex
        item = city_list.options[candidate].value
        
        print(item,  chosen_values)
        return item in  chosen_values
        
    def on_select_click(ev):
        if already_chosen():
            return
        
        dropdown = ev.target
        num = city_list.selectedIndex
        item = city_list.options[num].value
        chosen <= OPTION(item)
        go.disabled = False
        select.disabled = True
    
    def on_remove_click(ev):
        dropdown = ev.target
        
        selected = [(i, option.value) for i, option in enumerate(chosen) if option.selected]
        for (num, item) in reversed(selected):
            
            chosen.remove(num)
        if len(chosen.options) == 0:
            go.disabled = True
        remove.disabled = True
        
    def on_city_list_change(ev):
        select.disabled = (already_chosen() or len(chosen.options) >=3) 

    def on_chosen_change(ev):
        remove.disabled = False
        
    def on_go_click(ev):
        print(len(document.getElementsByClassName("chart")))
        for div in document.getElementsByClassName("chart"):
            print("removing", div)
            div.remove()
            
        chart2 = DIV(Class="chart")   
        
        
        document["chartarea"] <= chart2
        
        if not testing:
            chosen_values = [v.value for v in chosen.options]
            fields = chosen_values
            data = dict([(k, decade_data[k]) for k in chosen_values ])
        else:
              
            data = {'Beijing, China': {'185': 9.995012560808409, '186': 9.684169062767799, '187': 9.527474806309987, '188': 9.714275055322798, '189': 9.979191312496239, '190': 10.177958068932714, '191': 11.031791079141199, '192': 11.509275657221055, '193': 11.941068405106662, '194': 12.114836913552136, '195': 16.172985960357515, '196': 20.692509427692123, '197': 25.700616795911138, '198': 35.253043300417566, '199': 43.20706760305601, '200': 55.58410470065227, '201': 69.20189618388066}, 'London, United Kingdom': {'185': 7.85060554803318, '186': 9.134226935862253, '187': 9.912712084762754, '188': 10.752737952060066, '189': 11.495180835625778, '190': 12.447836011815816, '191': 12.899655091909693, '192': 11.631724848687648, '193': 12.18617366203635, '194': 12.079535494446134, '195': 13.198102365141427, '196': 12.250948169676278, '197': 8.238790169622593, '198': 7.057462987826206, '199': 5.696491046180793, '200': 4.3652121481206265, '201': 3.985589388189527}}
            fields = ['Beijing, China', 'ZZZ']
      
        title = "Comparison between " + '; '.join(fields)
        ldd = brycharts.LabelledDataDict(data, "Particulate Concentration")
        brycharts.GroupedBarChart(chart2, ldd, title, direction="vertical", height="45%")

    layout()

    city_list.bind("change", on_city_list_change )
    chosen.bind("change", on_chosen_change)
    select.bind("click", on_select_click)
    remove.bind("click", on_remove_click)
    
        
    go.bind("click", on_go_click)
        
    
#init()    
