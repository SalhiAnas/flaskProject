import os
from collections import defaultdict

import xmlschema
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from bs4 import BeautifulSoup,NavigableString,Tag

from Schema import Schema,Table,Column


translate = {
            'ID': 'varchar(30)',
            'string': 'text',
            'boolean': 'boolean',
            'decimal': 'numeric',
            'float': 'real',
            'double': 'double precision',
            'duration': 'interval',
            'dateTime': 'timestamp',
            'time': 'time',
            'date': 'date',
            'gYearMonth': 'timestamp',
            'gYear': 'timestamp',
            'gMonthDay': 'timestamp',
            'gDay': 'timestamp',
            'gMonth': 'timestamp',
            'hexBinary': 'bytea',
            'base64Binary': 'bytea',
            'anyURI': 'varchar',
            'normalizedString': 'varchar',
            'token': 'varchar',
            'integer': 'int',
            'nonPositiveInteger': 'int',
            'negativeInteger': 'int',
            'long': 'long',
            'int': 'int',
            'short': 'int',
            'byte': 'bit',
            'positiveInteger': 'int',
        }



app = Flask(__name__)
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

        if parseFile(f1,f2) == "valid":
            SqlSchema=extractSchema(f1)
            creatingSqlFile(SqlSchema,f2)

            return "Generating the sql file"
        elif parseFile(f1,f2) =="invalid":
            return "this document is not valid"
        else:
            return parseFile(f1,f2)







def parseFile(xmlSchema, XMlFile):
    try:
        XS = xmlschema.XMLSchema("upload/"+xmlSchema.filename)
        if(XS.is_valid("upload/"+XMlFile.filename)):
                return 'valid'
        else:
                return 'invalid'
    except Exception as e:
        error_string = str(e)
        return error_string


def extractSchema(xmlSchema):
    SqlSchema = Schema(os.path.splitext(xmlSchema.filename)[0])
    infile = open("upload/" + xmlSchema.filename, "r")
    contents = infile.read()
    soup = BeautifulSoup(contents, 'xml')
    complexTypes = soup.find("element").find("element").findAll("complexType")

    for complexType in complexTypes:
        # print("table -- ",complexType.findParent("element").get("name"))
        table = Table(complexType.findParent("element").get("name"))
        Children = complexType.find().findChildren("element", recursive=False)
        Attributes = complexType.findChildren("attribute", recursive=False)
        for Child in Children:
            if Child.get("type") is not None:
                column = Column(Child.get("name"), Child.get("type"), False,False,
                                True if Child.get("minOccurs") == "0" else False)
                table.add_column(column)
        for Attribute in Attributes:
            column = Column(Attribute.get("name"), Attribute.get("type"),
                            True if Attribute.get("type") == "xs:ID" else False,
                            False if Attribute.get("use") == "required" else True)
            table.add_column(column)
        SqlSchema.add_table(table)

    elements = soup.find("element").findAll("element")
    for element in elements:
        if element.get("type") is None:
            childElements = element.find().find().findChildren("element", recursive=False)
            ParentTable = SqlSchema.get_table(element.get("name"))
            for childElement in childElements:
                if childElement.get("type") is None:
                    print(childElement.get("name"), "-----> ", element.get("name"))
                    childTable = SqlSchema.get_table(childElement.get("name"))
                    if ParentTable.get_pk() is not None:
                        pk = ParentTable.get_pk()
                        fk = Column(pk.get_name(), pk.get_datatype(), False, True, False)
                        childTable.add_fk(fk,ParentTable.get_name())

    for t in SqlSchema.get_tables():
        print("-----", t.get_name())
        for c in t.get_columns():
            print(c.get_name(), " -- ", c.get_attributes())

    return SqlSchema


def creatingSqlFile(SqlSchema,xmlFile):
    f = open("download/"+SqlSchema.get_name()+".sql", 'w')
    for t in SqlSchema.get_tables():
        f.write("\ncreate table "+t.get_name()+" ( ")
        for c in t.get_columns():
            name = c.get_datatype().split(":")
            dataType = " NOT NULL " if c.is_nullable() else ""
            primary = " PRIMARY KEY " if c.is_primary() else ""
            f.write(c.get_name() + " " + translate[name[1]] + dataType + primary)
            if c != t.get_columns()[len(t.get_columns())-1]:
                f.write(", ")
        fk=t.get_fk()
        if fk is not None:
            parentTable = fk.get_fkParent()
            f.write(", FOREIGN KEY (" + fk.get_name() + ") REFERENCES " +parentTable+ "(" + fk.get_name() + "));")
        else:
            f.write(");")
    return 0

if __name__ == '__main__':
    app.run()










