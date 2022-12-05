import plotly.express as px
df = px.data.iris()
fig = px.parallel_coordinates(df, dimensions=["sepal_length", "sepal_width", "petal_length", "petal_width"],
                             color="species_id", range_color=[0.5, 3.5],
                             color_continuous_scale=[(0.00, "red"),   (0.33, "red"),
                                                     (0.33, "green"), (0.66, "green"),
                                                     (0.66, "blue"),  (1.00, "blue")])

fig.update_layout(coloraxis_colorbar=dict(
    title="Species",
    tickvals=[1,2,3],
    ticktext=["setosa","versicolor","virginica"],
    lenmode="pixels", len=100,
))
fig.show()