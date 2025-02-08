import xml.etree.ElementTree as ET

#Function to extract the data out of XML
def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    data_records = []

    # Go over all 'record' Elements
    for record in root.findall('.//record'):
        record_data = {}

        # Extract every field
        for field in record.findall('field'):
            name = field.attrib.get('name')
            value = field.text

            if name == 'Value':
                record_data['Value'] = float(value) if value else None
            elif name == 'Year':
                record_data['Year'] = int(value) if value else None
            elif name == 'Country or Area' and 'key' in field.attrib:
                record_data['Country Code'] = field.attrib['key']

        data_records.append(record_data)

    return data_records


