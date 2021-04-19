import simplekml

coeff = 0.7
style_site = simplekml.Style()
style_site.iconstyle.color = 'ff0000ff'
style_site.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/donut.png'

style_linestring = simplekml.Style()
style_linestring.linestyle.width = 1*coeff
style_linestring.linestyle.color = '88ff5500'
style_linestring.polystyle.color = '88ff5500'

style_linestring_dx_dy = simplekml.Style()
style_linestring_dx_dy.linestyle.width = 4*coeff
style_linestring_dx_dy.linestyle.color = 'ff381e33'

style_site_sml_normal = simplekml.Style()
style_site_sml_normal.iconstyle.scale=0.7
style_site_sml_normal.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png'
style_site_sml_normal.labelstyle.scale = 0

style_site_sml_highlight = simplekml.Style()
style_site_sml_highlight.iconstyle.scale=1.2
style_site_sml_highlight.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png'
style_site_sml_highlight.labelstyle.scale = 1

stylemap_sml = simplekml.StyleMap()
stylemap_sml.normalstyle = style_site_sml_normal
stylemap_sml.highlightstyle = style_site_sml_highlight

style_site_normal = simplekml.Style()
style_site_normal.iconstyle.scale=0.7
style_site_normal.iconstyle.color = 'ff0000ff'
style_site_normal.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/donut.png'
style_site_normal.labelstyle.scale = 0
style_site_highlight = simplekml.Style()
style_site_highlight.iconstyle.scale=1.2
style_site_highlight.iconstyle.color = 'ff0000ff'
style_site_highlight.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/donut.png'
style_site_highlight.labelstyle.scale = 1
stylemap = simplekml.StyleMap()
stylemap.normalstyle = style_site_normal
stylemap.highlightstyle = style_site_highlight

style_site_normal_repeater = simplekml.Style()
style_site_normal_repeater.iconstyle.scale=0.7
style_site_normal_repeater.iconstyle.color = 'ff14F0F0'
style_site_normal_repeater.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/triangle.png'
style_site_normal_repeater.labelstyle.scale = 0

style_site_highlight_repeater = simplekml.Style()
style_site_highlight_repeater.iconstyle.scale=1.2
style_site_highlight_repeater.iconstyle.color = 'ff14F0F0'
style_site_highlight_repeater.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/triangle.png'
style_site_highlight_repeater.labelstyle.scale = 1

stylemap_repeater = simplekml.StyleMap()
stylemap_repeater.normalstyle = style_site_normal_repeater
stylemap_repeater.highlightstyle = style_site_highlight_repeater

style_band_3 = simplekml.Style()
style_band_3.linestyle.color = '85ff5500'
style_band_3.polystyle.color = '85ff5500'

style_band_5 = simplekml.Style()
style_band_5.linestyle.color = '85f69b45'
style_band_5.polystyle.color = '85f69b45'

style_band_7 = simplekml.Style()
style_band_7.linestyle.color = '85ff00aa'
style_band_7.polystyle.color = '85ff00aa'

style_band_8 = simplekml.Style()
style_band_8.linestyle.color = '850095e5'
style_band_8.polystyle.color = '850095e5'

style_band_1 = simplekml.Style()
style_band_1.linestyle.color = '85381e33'
style_band_1.polystyle.color = '85381e33'

band_dict = {'3': style_band_3, '5': style_band_5, '7': style_band_7, '8': style_band_8, '1': style_band_1,
             '2': style_band_1, '4': style_band_1, '6': style_band_1, '9': style_band_1}

style_umts = simplekml.Style()
style_gsm = simplekml.Style()

style_umts.linestyle.color = "851f03a4"
style_umts.polystyle.color = "851f03a4"
style_gsm.linestyle.color = "9864b736"
style_gsm.polystyle.color = "9864b736"# -*- coding: utf-8 -*-

