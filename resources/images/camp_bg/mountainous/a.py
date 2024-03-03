# import matplotlib.pyplot as plt
# from matplotlib.patches import Circle
# from PIL import Image
# import numpy as np

# # Load your background image
# image_path = 'resources\images\camp_bg\mountainous\greenleaf_camp4_light.png'  # Update this to the path of your image
# img = Image.open(image_path)

# # Initial coordinates of circles
# circles = [(100, 100), (150, 200)]  # Add more if needed

# fig, ax = plt.subplots()
# ax.imshow(img)

# # Create and add circles to the plot
# patches = []
# for x, y in circles:
#     circle = Circle((x, y), 25, fill=False, color='red', linewidth=2)
#     ax.add_patch(circle)
#     patches.append(circle)

# def on_press(event):
#     """Callback for mouse press event."""
#     for circle in patches:
#         contains, _ = circle.contains(event)
#         if contains:
#             circle.picked = True
#             circle.pickradius = circle.radius
#             break

# def on_release(event):
#     """Callback for mouse release event."""
#     for circle in patches:
#         circle.picked = False
#         x, y = circle.center  # circle.center contains the (x, y) coordinates
#         print(f"Circle released at: x={x*2}, y={y*2}")

# def on_move(event):
#     """Callback for mouse move event."""
#     for circle in patches:
#         if hasattr(circle, 'picked') and circle.picked:
#             # Update circle position
#             circle.center = event.xdata, event.ydata
#             # Update the figure
#             fig.canvas.draw()

# # Connect the callbacks to the figure
# fig.canvas.mpl_connect('button_press_event', on_press)
# fig.canvas.mpl_connect('button_release_event', on_release)
# fig.canvas.mpl_connect('motion_notify_event', on_move)

# plt.show()
