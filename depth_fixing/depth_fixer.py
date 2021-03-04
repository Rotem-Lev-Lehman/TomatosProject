from PIL import Image
import numpy as np

before_scale_path = r"C:\Users\User\coding\pythonProjects\ZSSR\test_data\20200916_172800_color_0_321_163_598_449.png"
after_scale_path = r"C:\Users\User\coding\pythonProjects\ZSSR\results\test_Sep_24_19_28_44\20200916_172800_color_0_321_163_598_449_zssr_X2.00X2.00.png"

before_img = Image.open(before_scale_path)
before_img.load()
before_img_array = np.asarray(before_img, dtype='int32')

after_img = Image.open(after_scale_path)
after_img.load()
after_img_array = np.asarray(after_img, dtype='int32')

print('hello')
