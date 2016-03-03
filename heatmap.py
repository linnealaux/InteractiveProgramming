from bokeh.charts import HeatMap, output_file, show

# (dict, OrderedDict, lists, arrays and DataFrames are valid inputs)
data = {'fruit': ['apples']*3 + ['bananas']*3 + ['pears']*3,
        'fruit_count': [4, 5, 8, 1, 2, 4, 6, 5, 4],
        'sample': [1, 2, 3]*3}

hm = HeatMap(data, x='fruit', y='sample', values='fruit_count',
             title='Fruits', stat=None)

output_file('heatmap.html')
show(hm)