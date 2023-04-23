from PIL import Image

basewidth = 300
img = Image.open('C:\\Users\\User\\Downloads\\S2_Stage_Skipper_Pavilion.png')
wpercent = (basewidth / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)))
img = img.resize((basewidth, hsize), Image.ANTIALIAS)
img.save('C:\\Users\\User\\Downloads\\S2_Stage_Skipper_Pavilion_resized.png')