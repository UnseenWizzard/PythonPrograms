from PIL import Image, ImageDraw
width = 1920
height = 2160
image = Image.new( 'RGBA', ( width, height ), ( 0, 0, 0, 255 ) )
x = 0
y = 0
down = True
counter = 1
draw = ImageDraw.Draw(image)
while ( y <= (height+240) ):
    while ( x <= (width) ):
        color = (  48, 45, 43,150 )
        if counter%5==0:
            color = ( 255, 139 , 0, 150 )
        elif counter%3==0:
            color=( 65, 65, 64, 150 )
        if down:
            draw.polygon([(x,y),(x+480,y),(x+240,y+240)],fill=color)
        else:
            draw.polygon([(x-240,y),(x+240,y),(x,y-240)],fill=color)
        x += 240
        counter+=1
    x = 0
    counter+=3
    if down:
        y += 240  
    down = ( not down )
image.save( 'test.png', format='PNG' )
