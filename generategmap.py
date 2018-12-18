#!/usr/bin/python
# Based on older script by Hayden Eskriett
# and https://gis.stackexchange.com/questions/46729/corner-coordinates-of-google-static-map-tile
# Updated 2/2018 to use newer api
### GoogleMapDownloader.py 
### Based on by Hayden Eskriett [http://eskriett.com]
### A script which when given a longitude, latitude and zoom level downloads a
### high resolution google map

import urllib
from PIL import Image
import os
import math

def generateImage(lat,lng,map_tile_width,map_tile_height,zoom,scale,apikey,format_image,maptype,style,size_tile_x,size_tile_y):
        
        tilesize_width=size_tile_x*scale
        tilesize_height=size_tile_y*scale
        width_final=map_tile_width*tilesize_width
        ##Special usecase add another line of tiles at the end for better world map editing
        #width_final=map_tile_width*(tilesize_width+1)
        height_final=map_tile_height*(tilesize_height-50*scale)
        map_img = Image.new('RGB', (width_final,height_final))
        #Get coordinates of starting pixels
        pixel_x, pixel_y = LatLonToPixels(lat, lng,zoom)
        for x in range(0, map_tile_width):
            for y in range(0, map_tile_height) :
                #Get coordinnates for next center of the map
                #Removes 50pix for footer
                final_lat,final_long=PixelsToLat(pixel_x+size_tile_x*x,pixel_y+((size_tile_y-50)*y),zoom)
                #print(final_lat,final_long)
                url = 'https://maps.googleapis.com/maps/api/staticmap?key='+apikey+'&scale='+str(scale)+'&center='+str(final_lat)+','+str(final_long)+'&zoom='+str(zoom)+'&format='+format_image+'&maptype='+maptype+'&style='+style+'&size='+str(size_tile_x)+'x'+str(size_tile_y)
                print(url)
                current_tile = str(x)+'-'+str(y)
                urllib.urlretrieve(url, current_tile)            
                im = Image.open(current_tile)
                # Removes bottom of the image
                im = im.crop((0, 0, tilesize_width, tilesize_height-(50*scale)))
                #If you want to download all tiles manually 
                #im.save("high_resolution_image"+f'{x:02}'+"-"+f'{y:02}'+".png")
                #files.download("high_resolution_image"+f'{x:02}'+"-"+f'{y:02}'+".png")
                map_img.paste(im, (x*tilesize_width, (map_tile_height-1-y)*(tilesize_height-50*scale)))
                ### Special usecase -  add another line of tiles at the end for better world map editing
                #if x==1:
                #       print('pasting_side')
                #       map_img.paste(im, ((x-1+map_tile_width)*tilesize_width, (map_tile_height-1-y)*(tilesize_height-50*scale)))
              
                os.remove(current_tile)
        map_img.save("high_resolution_image.png")
        #return map_img

#Google uses this tile size
#based on https://gis.stackexchange.com/questions/46729/corner-coordinates-of-google-static-map-tile
tileSize = 256
initialResolution = 2 * math.pi * 6378137 / tileSize
originShift = 2 * math.pi * 6378137 / 2.0

def LatLonToPixels( lat, lon,zoom ):
        "Converts given lat/lon in WGS84 Datum to XY in Spherical Mercator EPSG:900913"
        mx = lon * originShift / 180.0
        my = math.log( math.tan((90 + lat) * math.pi / 360.0 )) / (math.pi / 180.0)
        my = my * originShift / 180.0
        res = initialResolution / (2**zoom)
        
        px = (mx + originShift) / res
        py = (my + originShift) / res
        return px, py
      
def PixelsToLat( px, py, zoom):
    "Converts pixel coordinates in given zoom level of pyramid to EPSG:900913"
    res = initialResolution / (2**zoom)
    mx = px * res - originShift
    my = py * res - originShift
    lon = (mx / originShift) * 180.0
    lat = (my / originShift) * 180.0
    lat = 180 / math.pi * (2 * math.atan(math.exp(lat * math.pi / 180.0)) - math.pi / 2.0)
    return lat, lon

from PIL import Image
lat,lng = 41.289964,2.022324
#AWESOMELLY RESOLUTION CITY MAP
# map_tile_width,map_tile_height= 17,15
# zoom=15
#GOOD RESOLUTION CITY MAP
map_tile_width,map_tile_height= 6,7
zoom=14
#MID RESOLUTION CITY MAP
map_tile_width,map_tile_height= 4,5
zoom=13

size_tile_x,size_tile_y=512,512
scale=2
apikey='AIzaSyCYZEYp_BSqAjksRDqBX0cQx_EFf6YANOo'
format_image='png'
maptype='roadmap'
#regular style='element:geometry%7Ccolor:0xebe3cd&style=element:labels%7Cvisibility:off&style=element:labels.text.fill%7Ccolor:0x523735&style=element:labels.text.stroke%7Ccolor:0xf5f1e6&style=feature:administrative%7Celement:geometry%7Cvisibility:off&style=feature:administrative%7Celement:geometry.stroke%7Ccolor:0xc9b2a6&style=feature:administrative.land_parcel%7Cvisibility:off&style=feature:administrative.land_parcel%7Celement:geometry.stroke%7Ccolor:0xdcd2be&style=feature:administrative.land_parcel%7Celement:labels.text.fill%7Ccolor:0xae9e90&style=feature:administrative.neighborhood%7Cvisibility:off&style=feature:landscape.natural%7Celement:geometry%7Ccolor:0xdfd2ae&style=feature:poi%7Cvisibility:off&style=feature:poi%7Celement:geometry%7Ccolor:0xdfd2ae&style=feature:poi%7Celement:labels.text.fill%7Ccolor:0x93817c&style=feature:poi.park%7Celement:geometry.fill%7Ccolor:0xa5b076&style=feature:poi.park%7Celement:labels.text.fill%7Ccolor:0x447530&style=feature:road%7Celement:geometry%7Ccolor:0xf5f1e6&style=feature:road%7Celement:labels.icon%7Cvisibility:off&style=feature:road.arterial%7Celement:geometry%7Ccolor:0xfdfcf8&style=feature:road.highway%7Celement:geometry%7Ccolor:0xf8c967&style=feature:road.highway%7Celement:geometry.stroke%7Ccolor:0xe9bc62&style=feature:road.highway.controlled_access%7Celement:geometry%7Ccolor:0xe98d58&style=feature:road.highway.controlled_access%7Celement:geometry.stroke%7Ccolor:0xdb8555&style=feature:road.local%7Celement:labels.text.fill%7Ccolor:0x806b63&style=feature:transit%7Cvisibility:off&style=feature:transit.line%7Celement:geometry%7Ccolor:0xdfd2ae&style=feature:transit.line%7Celement:labels.text.fill%7Ccolor:0x8f7d77&style=feature:transit.line%7Celement:labels.text.stroke%7Ccolor:0xebe3cd&style=feature:transit.station%7Celement:geometry%7Ccolor:0xdfd2ae&style=feature:water%7Celement:geometry.fill%7Ccolor:0xb9d3c2&style=feature:water%7Celement:labels.text.fill%7Ccolor:0x92998d'
#black style='element:geometry%7Ccolor:0x4a4a4a&style=element:labels%7Cvisibility:off&style=element:labels.icon%7Cvisibility:off&style=element:labels.text.fill%7Ccolor:0x757575&style=element:labels.text.stroke%7Ccolor:0x212121&style=feature:administrative%7Celement:geometry%7Ccolor:0xffffff%7Cvisibility:off&style=feature:administrative.country%7Celement:labels.text.fill%7Ccolor:0x9e9e9e&style=feature:administrative.land_parcel%7Cvisibility:off&style=feature:administrative.locality%7Celement:labels.text.fill%7Ccolor:0xbdbdbd&style=feature:administrative.neighborhood%7Cvisibility:off&style=feature:poi%7Celement:labels.text.fill%7Ccolor:0x757575&style=feature:poi.park%7Celement:geometry%7Ccolor:0x333333&style=feature:poi.park%7Celement:labels.text.fill%7Ccolor:0x616161&style=feature:poi.park%7Celement:labels.text.stroke%7Ccolor:0x1b1b1b&style=feature:road%7Celement:labels.text.fill%7Ccolor:0x8a8a8a&style=feature:road.arterial%7Celement:geometry%7Ccolor:0xdadada%7Cvisibility:on%7Cweight:0.5&style=feature:road.highway%7Celement:geometry%7Ccolor:0xdadada%7Cvisibility:simplified%7Cweight:0.5&style=feature:road.highway.controlled_access%7Celement:geometry%7Ccolor:0x969696&style=feature:road.local%7Celement:geometry%7Ccolor:0xdadada&style=feature:road.local%7Celement:labels.text.fill%7Ccolor:0x616161&style=feature:transit%7Cvisibility:off&style=feature:transit%7Celement:labels.text.fill%7Ccolor:0x757575&style=feature:water%7Celement:geometry%7Ccolor:0x0e0e0e&style=feature:water%7Celement:labels.text.fill%7Ccolor:0x3d3d3d'
style='element:geometry%7Ccolor:0xf5f5f5&style=element:labels%7Cvisibility:off&style=element:labels.icon%7Cvisibility:off&style=element:labels.text.fill%7Ccolor:0x616161&style=element:labels.text.stroke%7Ccolor:0xf5f5f5&style=feature:administrative%7Celement:geometry%7Cvisibility:off&style=feature:administrative.land_parcel%7Cvisibility:off&style=feature:administrative.land_parcel%7Celement:labels.text.fill%7Ccolor:0xbdbdbd&style=feature:administrative.neighborhood%7Cvisibility:off&style=feature:poi%7Celement:geometry%7Ccolor:0xeeeeee&style=feature:poi%7Celement:labels.text.fill%7Ccolor:0x757575&style=feature:poi.park%7Ccolor:0xf1f1f1&style=feature:poi.park%7Celement:geometry%7Ccolor:0xe5e5e5&style=feature:poi.park%7Celement:labels.text.fill%7Ccolor:0x9e9e9e&style=feature:road%7Celement:geometry%7Ccolor:0x131313%7Cweight:0.5&style=feature:road.arterial%7Celement:geometry%7Ccolor:0x131313%7Cvisibility:simplified%7Cweight:1&style=feature:road.arterial%7Celement:geometry.stroke%7Ccolor:0x131313%7Cweight:0.5&style=feature:road.arterial%7Celement:labels.text.fill%7Ccolor:0x757575&style=feature:road.highway%7Celement:geometry%7Ccolor:0x131313%7Cvisibility:simplified%7Cweight:0.5&style=feature:road.highway%7Celement:labels.text.fill%7Ccolor:0x616161&style=feature:road.local%7Celement:geometry%7Ccolor:0x131313%7Cvisibility:simplified%7Cweight:0.5&style=feature:road.local%7Celement:labels.text.fill%7Ccolor:0x9e9e9e&style=feature:transit%7Cvisibility:off&style=feature:transit.line%7Celement:geometry%7Ccolor:0xe5e5e5&style=feature:transit.station%7Celement:geometry%7Ccolor:0xeeeeee&style=feature:water%7Celement:geometry%7Ccolor:0xe3e3e3&style=feature:water%7Celement:labels.text.fill%7Ccolor:0x9e9e9e'
style='element:geometry%7Ccolor:0xff6363&style=element:labels%7Cvisibility:off&style=element:labels.icon%7Cvisibility:off&style=element:labels.text.fill%7Ccolor:0x616161&style=element:labels.text.stroke%7Ccolor:0xf5f5f5&style=feature:administrative%7Celement:geometry%7Cvisibility:off&style=feature:administrative.land_parcel%7Cvisibility:off&style=feature:administrative.land_parcel%7Celement:labels.text.fill%7Ccolor:0xbdbdbd&style=feature:administrative.neighborhood%7Cvisibility:off&style=feature:poi%7Celement:geometry%7Ccolor:0xff6363&style=feature:poi%7Celement:labels.text.fill%7Ccolor:0x757575&style=feature:poi.park%7Ccolor:0xff4f4f&style=feature:poi.park%7Celement:geometry%7Ccolor:0xe54949&style=feature:poi.park%7Celement:labels.text.fill%7Ccolor:0x9e9e9e&style=feature:road%7Ccolor:0xffffff&style=feature:road%7Celement:geometry%7Ccolor:0xffffff%7Cweight:0.5&style=feature:road.arterial%7Ccolor:0xffffff&style=feature:road.arterial%7Celement:geometry%7Ccolor:0xffffff%7Cvisibility:simplified%7Cweight:1&style=feature:road.arterial%7Celement:geometry.stroke%7Ccolor:0x131313%7Cweight:0.5&style=feature:road.arterial%7Celement:labels.text.fill%7Ccolor:0x757575&style=feature:road.highway%7Ccolor:0xffffff&style=feature:road.highway%7Celement:geometry%7Ccolor:0xffffff%7Cvisibility:simplified%7Cweight:0.5&style=feature:road.highway%7Celement:labels.text.fill%7Ccolor:0x616161&style=feature:road.local%7Ccolor:0xffffff&style=feature:road.local%7Celement:geometry%7Ccolor:0xffffff%7Cweight:0.5&style=feature:road.local%7Celement:labels.text.fill%7Ccolor:0x9e9e9e&style=feature:transit%7Cvisibility:off&style=feature:transit.line%7Celement:geometry%7Ccolor:0xe5e5e5&style=feature:transit.station%7Celement:geometry%7Ccolor:0xeeeeee&style=feature:water%7Celement:geometry%7Ccolor:0xffffff&style=feature:water%7Celement:labels.text.fill%7Ccolor:0x9e9e9e'
style='element:labels%7Cvisibility:off&style=feature:administrative%7Cvisibility:off&style=feature:administrative%7Celement:geometry.fill%7Ccolor:0x7f2200%7Cvisibility:off&style=feature:administrative%7Celement:geometry.stroke%7Ccolor:0x87ae79%7Cvisibility:on&style=feature:administrative%7Celement:labels.text.fill%7Ccolor:0x495421&style=feature:administrative%7Celement:labels.text.stroke%7Ccolor:0xffffff%7Cvisibility:on%7Cweight:4.1&style=feature:administrative.land_parcel%7Cvisibility:off&style=feature:administrative.neighborhood%7Cvisibility:off&style=feature:administrative.neighborhood%7Celement:labels%7Cvisibility:off&style=feature:landscape%7Celement:geometry.fill%7Ccolor:0xabce83&style=feature:poi%7Celement:geometry.fill%7Ccolor:0x769E72&style=feature:poi%7Celement:labels.text.fill%7Ccolor:0x7B8758&style=feature:poi%7Celement:labels.text.stroke%7Ccolor:0xEBF4A4&style=feature:poi.park%7Celement:geometry%7Ccolor:0x8dab68%7Cvisibility:simplified&style=feature:road%7Celement:geometry.fill%7Cvisibility:simplified&style=feature:road%7Celement:labels.text.fill%7Ccolor:0x5B5B3F&style=feature:road%7Celement:labels.text.stroke%7Ccolor:0xABCE83&style=feature:road.arterial%7Celement:geometry%7Ccolor:0x9BBF72&style=feature:road.highway%7Celement:geometry%7Ccolor:0xEBF4A4&style=feature:road.local%7Celement:geometry%7Ccolor:0xA4C67D&style=feature:water%7Celement:geometry%7Ccolor:0xaee2e0%7Cvisibility:on'
generateImage(lat,lng,map_tile_width,map_tile_height,zoom,scale,apikey,format_image,maptype,style,size_tile_x,size_tile_y)

from IPython.display import Image
#Image(filename='high_resolution_image.png')
