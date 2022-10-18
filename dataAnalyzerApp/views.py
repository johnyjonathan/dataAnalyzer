import pandas, urllib, base64, io, json
import matplotlib.pyplot as plt
import numpy as np
from django.shortcuts import redirect, render
from django.http import HttpResponse
from dataAnalyzerApp import utilities


def uploadView(request):
    if request.method == "GET":
        return render(request, 'uploadview.html')
    else:
        if request.POST.get("file_submit_button"):
            post_files = request.FILES
            csv_data = post_files['csv_file']
            if request.POST['columns'] == "on":
                inputs_number = int(request.POST["member"])
                inputs_names = ['column'+ str(number) for number in range(0,inputs_number)]
                inputs_values = [request.POST[name] for name in inputs_names]
                data_frame = pandas.read_csv(csv_data, names=inputs_values, header=None)
                request.session['columns'] = inputs_values
            else:
                data_frame = pandas.read_csv(csv_data)

            request.session['data'] = data_frame.to_json()
            return redirect("mainView")

def mainView(request):
    json_data = request.session['data']
    data_frame = pandas.read_json(json_data)
    html_table = data_frame.to_html(classes="table", justify="left")
    numeric_cols = utilities.isColumnNumeric(data_frame, request.session['columns'])
    classes = [x for x in request.session['columns'] if x not in numeric_cols]

    if request.method == "GET":
        return render(request,'mainview.html',{'html_table': html_table, 'columns': request.session['columns'], 'numeric_cols': numeric_cols, 'classes': classes})
    else: 
        if request.POST.get('execute_mode'):
            col_ = request.POST['col_select']
            mode_df = data_frame[col_].mode()
            
            list_of_values = mode_df[0]
            
            return render(request,'mainview.html',{'html_table': html_table, 'columns': request.session['columns'], 'values':list_of_values, 'col': col_, 'numeric_cols': numeric_cols, 'classes': classes})
        
        if request.POST.get('execute_mean'):
            col_ = request.POST['col_select']
            mean_df = float(data_frame[col_].mean())
            
            return render(request,'mainview.html',{'html_table': html_table, 'columns': request.session['columns'], 'col': col_, 'values_mean': round(mean_df,2), 'numeric_cols': numeric_cols, 'classes': classes})
        
        if request.POST.get('execute_median'):
            col_ = request.POST['col_select']
            median_df = float(data_frame[col_].median())
            return render(request,'mainview.html',{'html_table': html_table, 'columns': request.session['columns'], 'col': col_, 'values_median': round(median_df,2), 'numeric_cols': numeric_cols, 'classes': classes})
        
        if request.POST.get('execute_datarange'):
            col_ = request.POST['col_select']
            values = [float(x) for x in data_frame[col_].tolist()]
            data_range = utilities.rangeData(values)
            return render(request,'mainview.html',{'html_table': html_table, 'columns': request.session['columns'], 'col': col_, 'values_range': round(data_range,2), 'numeric_cols': numeric_cols, 'classes': classes})

        if request.POST.get("execute_q1"):
            col_ = request.POST['col_select']
            q1 = utilities.getQuantile(data_frame[col_],1)
            return render(request,'mainview.html',{'html_table': html_table, 'columns': request.session['columns'], 'col': col_, 'values_q1': round(q1,2), 'numeric_cols': numeric_cols, 'classes': classes})

        if request.POST.get("execute_q2"):
            col_ = request.POST['col_select']
            q2 = utilities.getQuantile(data_frame[col_],2)
            return render(request,'mainview.html',{'html_table': html_table, 'columns': request.session['columns'], 'col': col_, 'values_q2': round(q2,2), 'numeric_cols': numeric_cols, 'classes': classes})

        if request.POST.get("execute_q3"):
            col_ = request.POST['col_select']
            q3 = utilities.getQuantile(data_frame[col_],3)
            return render(request,'mainview.html',{'html_table': html_table, 'columns': request.session['columns'], 'col': col_, 'values_q3': round(q3,2), 'numeric_cols': numeric_cols, 'classes': classes})
        
        if request.POST.get("execute_IQR"):
            col_ = request.POST['col_select']
            iqr = utilities.getIQR(data_frame[col_])
            
            return render(request,'mainview.html',{'html_table': html_table, 'columns': request.session['columns'], 'col': col_, 'values_iqr': round(iqr,2), 'numeric_cols': numeric_cols, 'classes': classes})
        
        if request.POST.get("execute_summary"):
            col_ = request.POST['col_select']
            summary = utilities.summaryFiveNumbers(data_frame[col_])
            return render(request,'mainview.html',{'html_table': html_table, 'columns': request.session['columns'], 'col': col_, 'values_summary': summary, 'numeric_cols': numeric_cols, 'classes': classes})
        
        if request.POST.get("generate_plot"):
            selected_columns = request.POST.getlist("cols_for_plot")
            if request.POST.get("class_separation"):
                selected_class = request.POST["class_select"]
                list_of_unique_classes = data_frame[selected_class].unique()
                list_of_dfs_by_class = [data_frame.loc[data_frame[selected_class] == element] for element in list_of_unique_classes]
                classes_graphs = []
                for df in range(len(list_of_dfs_by_class)):
                    fig = plt.figure()
                    plt.title(list_of_unique_classes[df])
                    boxplot = list_of_dfs_by_class[df].boxplot(column=selected_columns)
                    buffer = io.BytesIO()
                    plt.savefig(buffer,format="png")
                    buffer.seek(0)
                    image_png = buffer.getvalue()
                    graph = base64.b64encode(image_png)
                    graph = graph.decode('utf-8')
                    buffer.close()
                    classes_graphs.append(graph)
                
                return render(request,'plotview.html',{'plots':classes_graphs}) 
            else:
        
                fig = plt.figure()
                boxplot = data_frame.boxplot(column=selected_columns)
                buffer = io.BytesIO()
                plt.savefig(buffer,format="png")
                buffer.seek(0)
                image_png = buffer.getvalue()
                graph = base64.b64encode(image_png)
                graph = graph.decode('utf-8')
                buffer.close()

            return render(request,'plotview.html',{'plot':graph}) 