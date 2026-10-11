import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread("BCBS_grid.png")

fig, ax = plt.subplots(figsize=(10, 13))
ax.imshow(img)

def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        print(
            f"Image=({int(event.xdata)}, {int(event.ydata)}) "
            f"PDF=({int(event.xdata/3)}, {int(event.ydata/3)})"
        )

fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
