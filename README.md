# colors_exercise
MODEs:

        - "mix" - New color is average of values from given values (default mode if invalid or empty)
        
        - "lowest" - New color is created from the lowest from all of colors (independently r,g,b,a)
        
        - "highest" - New color is created from the highest from all of colors (independently r,g,b,a)
        
        - "mix-saturate" - last color has new saturation equal to average of other colors
        
example of CLI:

        python test.py 21,2,2,2 wa, 0,0,0,0

        python test.py -m lowest 
        
        python test.py --mode highest 255,255,255,255 11,11,11
        
        
