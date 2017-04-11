def GetColor(value):
    power = value / 255.0
    if 0 <= power < 0.25:
        blue = power * 4
        red = 0
        green = 0
    elif 0.25 <= power < .5:
        blue = 2 - power * 4
        red = (power - .25) * 4.0
        green = 0
    elif .5 <= power < .75:
        blue = 0
        red = 1
        green = (power - .5) * 4.0
    else:
        red = 1
        green = 1
        blue = (power - .75) * 4.0
    return (int(red*255),int(green*255),int(blue*255))    
    
target = open("colors.pal", 'w')
target.truncate()
    
for i in range(256):
    red, green, blue = GetColor(i)
    target.write(str(red) + " " + str(green) + " " + str(blue))
    target.write("\n")
    
target.close() 
