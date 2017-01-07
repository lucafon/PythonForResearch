import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster.bicluster import SpectralCoclustering
from bokeh.models import HoverTool, ColumnDataSource
from bokeh.plotting import figure, output_file, show
import numpy as np



def location_plot(title, colors):
    output_file(title+".html")
    location_source = ColumnDataSource(
        data={
            "x": whisky[" Latitude"],
            "y": whisky[" Longitude"],
            "colors": colors,
            "regions": whisky.Region,
            "distilleries": whisky.Distillery
        }
    )
    
    fig = figure(title = title,
        x_axis_location = "above", tools="resize, hover, save")
    fig.plot_width  = 400
    fig.plot_height = 500
    fig.circle("x", "y", 10, 10, size=9, source=location_source,
         color='colors', line_color = None)
    fig.xaxis.major_label_orientation = np.pi / 3
    hover = fig.select(dict(type = HoverTool))
    hover.tooltips = {
        "Distillery": "@distilleries",
        "Location": "(@x, @y)"
    }
    show(fig)


whisky = pd.read_csv('./whiskies.txt')
whisky['Region'] = pd.read_csv('./regions.txt')
print(whisky.head())

flavors = whisky.iloc[:, 2:14]
print(flavors)

# plt.figure(figsize=(10,10))
corr_flavors = pd.DataFrame.corr(flavors)
# plt.pcolor(corr_flavors)
# plt.colorbar()
# plt.show()

corr_whisky = pd.DataFrame.corr(flavors.transpose())
# plt.pcolor(corr_whisky)
# plt.axis('tight') 
# plt.colorbar()
# plt.show()

model = SpectralCoclustering(n_clusters=6, random_state=0)
model.fit(corr_whisky)
print(np.sum(model.rows_, axis=1))

whisky['Group'] = pd.Series(model.row_labels_, index=whisky.index)
whisky = whisky.ix[np.argsort(model.row_labels_)]
whisky = whisky.reset_index(drop = True)

correlations = np.array(pd.DataFrame.corr(whisky.iloc[:, 2:14].transpose()))

plt.figure(figsize=(14,7))
plt.subplot(121)
plt.pcolor(corr_whisky)
plt.title('Original')
plt.axis('tight') 
plt.subplot(122)
plt.pcolor(correlations)
plt.title('Rearranged')
plt.axis('tight') 
plt.colorbar()
plt.show()

distilleries = list(whisky.Distillery)
cluster_colors = ['red', 'orange', 'green', 'blue', 'purple', 'gray']
correlation_colors = []
for i in range(len(distilleries)):
    for j in range(len(distilleries)):
        if correlations[i,j] < 0.7:   
            correlation_colors.append('white')        
        else:                                         
            if whisky.Group[i] == whisky.Group[j]:
                correlation_colors.append(cluster_colors[whisky.Group[i]]) 
            else:                                      
                correlation_colors.append('lightgray') 


source = ColumnDataSource(
    data = {
        "x": np.repeat(distilleries,len(distilleries)),
        "y": list(distilleries)*len(distilleries),
        "colors": correlation_colors,
        "alphas": correlations.flatten(),
        "correlations": correlations.flatten(),
    }
)

output_file("Whisky Correlations.html", title="Whisky Correlations")
fig = figure(title="Whisky Correlations",
    x_axis_location="above", tools="resize,hover,save",
    x_range=list(reversed(distilleries)), y_range=distilleries)
fig.grid.grid_line_color = None
fig.axis.axis_line_color = None
fig.axis.major_tick_line_color = None
fig.axis.major_label_text_font_size = "5pt"
fig.xaxis.major_label_orientation = np.pi / 3

fig.rect('x', 'y', .9, .9, source=source,
     color='colors', alpha='alphas')
hover = fig.select(dict(type=HoverTool))
hover.tooltips = {
    "Whiskies": "@x, @y",
    "Correlation": "@correlations",
}
show(fig)

cluster_colors = ["red", "orange", "green", "blue", "purple", "gray"]
regions = ["Speyside", "Highlands", "Lowlands", "Islands", "Campbelltown", "Islay"]
region_colors = dict(zip(regions, cluster_colors))
region_cols = [region_colors[whisky.Region[i]] for i in range(whisky.Region.shape[0])]
classification_cols = [cluster_colors[whisky.Group[i]] for i in range(whisky.Group.shape[0])]

location_plot("Whisky Locations and Regions", region_cols)
location_plot("Whisky Locations and Groups", classification_cols)

