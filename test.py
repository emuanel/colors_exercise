#!/usr/bin/python
import argparse
import re
from statistics import mean
import colorsys

class Color:
    """
    color rgba
    :attributes: R,G,B,alpha
    """
    def __init__(self, color):
        """
        :param color: string containing rgba colorin hex or decimal format.
        """
        color_valid = self.validate_color(color)
        if color_valid:
            components = color_valid.split(',')
            self.R = int(components[0])
            self.G = int(components[1])
            self.B = int(components[2])
            self.alpha = int(components[3])
        
    def validate_color(self, color):
        """
        validate color with regular expressions. two formats possible: hexadecimal format eg. ff0000ff and decimal eg. 255,0,0,255
        :param color: string containing rgba colorin hex or decimal format.
        """
        if(color == None):
            return False
                                 
        regex_hex = "^([0-9a-f]{8})$"                      #regex for hexadecimal format
        regex_dec = "^([0-9]{1,3},){3}[0-9]{1,3}$"         #regex for decimal format
        if re.match(regex_hex, color):
            return self.hex_to_dec(color)                  #convert hex to decimal format
        elif re.match(regex_dec, color):
            return color
        else:
            print("non-valid color: ", color)
        
    def hex_to_dec(self, value):
        """
        convert hexadecimal format to decimal format
        :param value: string containing rgba color in hex format.
        """
        lenght = len(value)
        dec_list = list(int(value[i:i + lenght // 3], 16) for i in range(0, lenght, lenght // 3))
        dec_list = [str(element) for element in dec_list]
        dec_str = ",".join(dec_list)
        return dec_str
    
    def dec_to_hex(self, value):
        """
        convert decimal format to hexadecimal format
        :param value: list containing rgba color in decimal format eg.[22,2,2,2].
        :return: a string hex color eg. ff00ff00.
        """
        return '%02x%02x%02x%02x' % tuple(value)
    
       
    def __str__(self):
        """
        :return: a string with essentials infos.
        """
        h,l,s = Color.rgb_to_hls([self.R/255, self.G/255, self.B/255])
        h *= 360
        s *= 100
        l *= 100

        return "red: " + str(self.R) + "\n" + \
            "green: " + str(self.G) + "\n" + \
                "blue: " + str(self.B) + "\n" +\
                    "alpha: " + str(self.alpha) + "\n" + \
                        "hex: " + self.dec_to_hex([self.R, self.G, self.B, self.alpha]) + "\n" + \
                            "hue "  + str(h) + "\n" + \
                                "saturation " + str(s) +"\n" + \
                                    "lightness " + str(l) +"\n" 

    def rgb_to_hls(rgb):
        """
        convert rgb color to hls color
        :param value: list containing rgb color in decimal format eg.[255,255,255].
        :return: a list with hls values.
        """
        return colorsys.rgb_to_hls(rgb[0], rgb[1], rgb[2])
    
    def hls_to_rgb(hls):
        """
        convert hls color to rgb color
        :param value: list containing hls color in decimal format eg.[255,255,255].
        :return: a list with rgb values.
        """
        return colorsys.hls_to_rgb(hls[0], hls[1], hls[2])
     
    def mix(Rs,Gs,Bs,alphas):
        """
        make new color created from the average from all of colors
        :param Rs: list containing red colors in decimal format eg.[0,2,255,32,213,12,12].
        :param Gs: list containing green colors in decimal format.
        :param Bs: list containing blue colors in decimal format.
        :param alphas: list containing alphas in decimal format.
        :return: a list with new rgba value.
        """
        R = int(mean(Rs))
        G = int(mean(Gs))
        B = int(mean(Bs))
        alpha = int(mean(alphas))
        return [R,G,B,alpha]
        
    def lowest(Rs,Gs,Bs,alphas):
        """
        make new color created from the lowest from all of colors
        :param Rs: list containing red colors in decimal format eg.[0,2,255,32,213,12,12].
        :param Gs: list containing green colors in decimal format.
        :param Bs: list containing blue colors in decimal format.
        :param alphas: list containing alphas in decimal format.
        :return: a list with new rgba value.
        """
        R = int(min(Rs))
        G = int(min(Gs))
        B = int(min(Bs))
        alpha = int(min(alphas))
        return [R,G,B,alpha]
    
    def highest(Rs,Gs,Bs,alphas):
        """
        make new color created from the highest from all of colors
        :param Rs: list containing red colors in decimal format eg.[0,2,255,32,213,12,12].
        :param Gs: list containing green colors in decimal format.
        :param Bs: list containing blue colors in decimal format.
        :param alphas: list containing alphas in decimal format.
        :return: a list with new rgba value.
        """
        R = int(max(Rs))
        G = int(max(Gs))
        B = int(max(Bs))
        alpha = int(max(alphas))
        return [R,G,B,alpha]
        
    def mix_saturate(Rs,Gs,Bs,alphas):
        """
        make new color from last color with new saturation equal to average of other colors 
        :param Rs: list containing red colors in decimal format eg.[0,2,255,32,213,12,12].
        :param Gs: list containing green colors in decimal format.
        :param Bs: list containing blue colors in decimal format.
        :param alphas: list containing alphas in decimal format.
        :return: a list with new rgba value.
        """
        saturations = []
        for r,g,b in zip(Rs,Gs,Bs):
            saturations.append(Color.rgb_to_hls([r,g,b])[2])
        R = Rs[-1]
        G = Gs[-1]
        B = Bs[-1]
        alpha = alphas[-1]
        h,l,s = Color.rgb_to_hls([R,G,B])
        r,g,b = Color.hls_to_rgb([h,l,s])
        
        return [int(r), int(g), int(b), int(alpha)]
    
    
def read_file(fileName="colors.txt"):
    """
    read file line by line
    :param fileName: string containing path to file.
    :return: a list with lines (non-valid colors).
    """
    colors = []
    try:
        with open(fileName) as fp:
            while True:
                line = fp.readline()
                if not line:
                    break
                colors.append(line.strip('\n'))        #without '/n'
    except:
        print("problem with file")
    return colors
    
if (__name__ == "__main__"):
    colors_nonvalid = read_file()           #colors from file (even non-valid)
    
    modes = {"mix":Color.mix, "lowest":Color.lowest, "highest":Color.highest, "mix-saturate":Color.mix_saturate}
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', default="mix")
    parser.add_argument('colors', type=str, nargs='+')
    mode = parser.parse_args().mode
    if not mode in modes:
        mode='mix'
        
    colors_nonvalid.extend(parser.parse_args().colors)  #add to list colors from CLI 
    
    colors = []                             #list with objects Color
    for i in colors_nonvalid:
        colors.append(Color(i))     
    
    R,G,B,alpha=[[],[],[],[]]               #lists of red/green/blue/alpha components from all colors
    for i in colors:
        try:
            R.append(i.R)
            G.append(i.G)
            B.append(i.B)
            alpha.append(i.alpha)
        except:
            None
    
    new_value = modes[mode](R,G,B,alpha)
    value_list = [str(element) for element in new_value]
    value_str = ",".join(value_list)
    new_color = Color(value_str)
    print(new_color)
    
    
