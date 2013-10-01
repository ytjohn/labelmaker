# Create your views here.
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch

import datetime

def current_datetime(request):
    now = datetime.datetime.now()
    width, height = letter
    startx = 0*inch
    something = 0.5*inch

    entries = "entries: "
    for x in range(0, 50):
        entries = "%s, %d" % (entries, x)

    html = "<html><body>width: %s </body></html>" % entries
    return HttpResponse(html)

def makepdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    response['Content-Disposition'] = 'filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=letter, bottomup=0)
    # move the origin up and to the left

    # OL6650 - http://www.onlinelabels.com/OL6650.htm
    # Sheet Size:	8.5" x 11"	Labels Per Sheet:	280
    # Shape:	Round Corner Rectangle	Corner Radius:	0.03125"
    # Length:	1"	Height:	0.25"
    # Top Margin:	0.5"	Bottom Margin:	0.5"
    # Left Margin:	0.375"	Right Margin:	0.375"
    # Horizontal Spacing:	0.125"	Vertical Spacing:	0"
    # Horizontal Pitch:	1.125"	Vertical Pitch:	0.25"

    total = 280.0
    labelsperrow = 7.0

    startx = 0*inch
    starty = 0*inch
    endx = 8.5*inch
    endy = 11*inch

    # setup our y axis
    ymargin = 0.5*inch
    yheight = 0.25*inch
    yspacer = 0*inch
    yfirst = starty + ymargin
    ylast = endy - ymargin


    # setup our x axis
    xmargin = 0.375*inch
    xlength = 1*inch
    xspacer = 0.125*inch
    xfirst = startx + xmargin
    xlast = endx - xmargin

    # top corner
    p.translate(startx, starty)

    # define a large font
    p.setFont("Helvetica", 9)

    # let's make a grid
    labelnumber = 1
    while (labelnumber <= total):
        if labelnumber == 1:
            y = yfirst
            x = xfirst

        y2 = y + yheight
        x2 = x + xlength

        # make the top horizontal
        p.line(x,y,x2,y)
        # make the bottom horizontal
        p.line(x,y2,x2,y2)

        # make the left vertical
        p.line(x,y,x,y2)
        # make the right vertical
        p.line(x2,y,x2,y2)

        # plop in our label

        # this is a magic math for cleanly placing text in a label (based on 1/16th of an inch)
        ydiv = yheight/inch * 16
        xdiv = xlength/inch * 16

        xtext = x + xlength/xdiv
        ytext = y2 - yheight/ydiv
        labeltext = 'sample%s-lbl' % labelnumber
        p.drawString(xtext,ytext, labeltext)

        # move our coordinates
        if (labelnumber/labelsperrow == int(labelnumber/labelsperrow)):
            x = xfirst
            y = y2 + yspacer
        else:
            x = x2 + xspacer


        # increment our completed label
        labelnumber = labelnumber + 1



    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response