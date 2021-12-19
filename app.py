import os
from pprint import pprint
from xml.etree import ElementTree as ET
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from glob import glob
import sys
from bs4 import BeautifulSoup
import xmlschema
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from xmlschema.namespaces import NamespaceView
from xmlschema.validators import XsdComplexType

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
app.config['XML_UPLOAD_EXTENSIONS'] = ['.xml', '.XML']
app.config['XSD_UPLOAD_EXTENSIONS'] = ['.xsd', '.XSD','.XSLT','xslt']

app.config['UPLOAD_PATH'] = 'upload'


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f1 = request.files['xmlSchema']
        f2 = request.files['xmlFile']

        xmlSchemaname = secure_filename(f1.filename)
        xmlfilename = secure_filename(f2.filename)
        if xmlfilename != '' and xmlSchemaname!= '':
            file_ext = os.path.splitext(xmlfilename)[1]
            if file_ext not in app.config['XML_UPLOAD_EXTENSIONS']:
                return 'the file uploaded is not an xml!'
            file_ext = os.path.splitext(xmlSchemaname)[1]
            if file_ext not in app.config['XSD_UPLOAD_EXTENSIONS']:
                return 'the file uploaded is not an xmlSchema!'
        else:
            return 'please upload both files !'
        f1.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(f1.filename)))
        f2.save(os.path.join(app.config['UPLOAD_PATH'], secure_filename(f2.filename)))

        return parsefile(f1,f2)



def parsefile(xmlSchema, XMlFile):
    if request.method == 'GET':
        try:
            tree = ET.parse("upload/"+xmlSchema.filename)
                # print(tree.)

            XS = xmlschema.XMLSchema("upload/"+xmlSchema.filename)
                # schema.types
                # NamespaceView({'vehicleType': XsdComplexType(name='vehicleType')})
                # pprint(dict(XS.elem))

                # NamespaceView({'vehicleType': XsdComplexType(name='vehicleType')})
            f = open("upload/"+xmlSchema.filename, "r")
            soup = BeautifulSoup(f.read())

            for element in soup.find_all('xs:element'):
                    print(element['name'],element['name'])  # prints name attribute value
            if(XS.is_valid("upload/"+XMlFile.filename)):
                    return render_template("success.html")
            else:
                    return 'This is not a well-formed XML document'
        except Exception as e:
            error_string = str(e)
            error="Error \n "+error_string
            return error



if __name__ == '__main__':
    app.run()
