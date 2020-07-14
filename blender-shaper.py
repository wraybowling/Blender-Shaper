import bpy
import os

unitLibrary = {
    "MILLIMETERS": {
        "unit": "mm",
        "multiplier": 1000
    },
    "CENTIMETERS": {
        "unit": "cm",
        "multiplier": 100
    },
    "METERS": {
        "unit": "cm",
        "multiplier": 100
    },
    "KILOMETERS": {
        "unit": "cm",
        "multiplier": 100
    },
    "INCHES": {
        "unit": "in",
        "multiplier": 39.37008
    },
    "FEET": {
        "unit": "in",
        "multiplier": 39.37008
    }
}

sceneUnit = bpy.context.scene.unit_settings.length_unit
svgUnit = unitLibrary[sceneUnit]['unit']
unitMult = unitLibrary[sceneUnit]['multiplier']

for curve in bpy.data.curves:
    
    print(curve.name)
    
    # start an svg path
    svg = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg
    xmlns="http://www.w3.org/2000/svg"
    xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"
    xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"
    width="100%s" height="100%s"
    viewBox="0 0 100 100">''' % (svgUnit, svgUnit)
    svg += '<sodipodi:namedview inkscape:document-units="%s" units="%s" />' % (svgUnit, svgUnit)
    svg += '<path fill-rule="evenodd" d="'
    for spline in curve.splines:
        index = 0
        for point in spline.bezier_points:
            if index == 0:
                svg += "\nM "
                svg += "%f,%f " % (point.co.x * unitMult, -point.co.y * unitMult)

            else:
                svg += "\nC "
                svg += "%f,%f " % (spline.bezier_points[index-1].handle_right.x * unitMult, -spline.bezier_points[index-1].handle_right.y * unitMult)
                svg += "%f,%f " % (point.handle_left.x * unitMult, -point.handle_left.y * unitMult)
                svg += "%f,%f " % (point.co.x * unitMult, -point.co.y * unitMult)
                
            index += 1

        if(spline.use_cyclic_u):
            svg += "C "
            svg += "%f,%f " % (spline.bezier_points[index-1].handle_right.x * unitMult, -spline.bezier_points[index-1].handle_right.y * unitMult)
            svg += "%f,%f " % (spline.bezier_points[0].handle_left.x * unitMult, -spline.bezier_points[0].handle_left.y * unitMult)
            svg += "%f,%f " % (spline.bezier_points[0].co.x * unitMult, -spline.bezier_points[0].co.y * unitMult)
            svg += 'Z'
    svg += '"/>'
    svg += '</svg>'

    # write it to a file
    filePath = os.path.dirname(bpy.data.filepath) + "/"
    filePath += "%s (%d).svg" % (curve.name, curve.users)
    file = open(filePath, "w")
    file.write(svg)
    file.close()
