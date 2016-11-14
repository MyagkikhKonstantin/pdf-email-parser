import os
import pdfquery
from collections import defaultdict

import settings

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
handler = logging.FileHandler(settings.log_name)
formatter = logging.Formatter('%(asctime)s - %(name)s - \
                               %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def parse_purchase_order_date(doc):
    label = doc.pq('LTTextLineHorizontal:contains("PO Date")')
    x0 = float(label.attr('x0'))
    x1 = float(label.attr('x1'))
    y0 = float(label.attr('y0'))
    y1 = float(label.attr('y1'))
    height = y1 - y0
    purchase_order_date = doc.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x0-50, y0-2*height, x1+50, y0)).text()
    logger.info('Purchase order date: %s' % purchase_order_date)
    return purchase_order_date


def parse_purchase_order_number(doc):
    label = doc.pq('LTTextLineHorizontal:contains("Purchase Order")')
    x0 = float(label.attr('x0'))
    x1 = float(label.attr('x1'))
    y0 = float(label.attr('y0'))
    y1 = float(label.attr('y1'))
    height = y1 - y0
    purchase_order_number = doc.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x0-50, y0-2*height, x1+50, y0)).text()
    logger.info('Purchase order number: %s' % purchase_order_number)
    return purchase_order_number


def parse_work_order(doc):
    #
    # finding column "Description" in table
    label = doc.pq('LTTextLineHorizontal:contains("Description")')
    x0 = float(label.attr('x0'))
    y_header_0 = float(label.attr('y0'))
    y_header_1 = float(label.attr('y1'))
    #
    # finding column "Work order"
    work_order_column = doc.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s"):contains("Work")' % (0, y_header_0-10, x0, y_header_1+10))
    step = 20
    x_column_1 = float(work_order_column.attr('x1')) + step
    #
    # finding work end of table
    label = doc.pq('LTTextLineHorizontal:contains("Please read")')
    y_table_end = float(label.attr('y1'))
    #
    # finding work order in table
    lines = defaultdict(list)
    for id, obj in enumerate(doc.get_tree().iter()):
        items = dict(obj.items())
        if items.get('bbox', None) is not None:
            (x0, y0, x1, y1) = eval(items['bbox'])
            if y1 < y_header_0 and y0 > y_table_end and x0 < x_column_1:
                if obj.text:
                    lines[y0].append([x0, obj.text])
    y = sorted(lines.keys(), key=lambda y: -y)[2]
    objects = lines[y]
    work_order = ' '.join([str(x[1]) for x in objects]).split()[1]
    logger.info('Work order: %s' % work_order)
    return work_order


def parse_required_completion_date(doc):
    #
    # finding column "Required completion date"
    label = doc.pq('LTTextLineHorizontal:contains("Required")')
    x_column_0 = float(label.attr('x0'))
    x_column_1 = float(label.attr('x1'))
    y_column_1 = float(label.attr('y1'))
    #
    # finding work end of table
    label = doc.pq('LTTextLineHorizontal:contains("Please read")')
    y_table_end = float(label.attr('y1'))
    #
    # finding required completion date in table
    lines = defaultdict(list)
    for id, obj in enumerate(doc.get_tree().iter()):
        items = dict(obj.items())
        if items.get('bbox', None) is not None:
            (x0, y0, x1, y1) = eval(items['bbox'])
            if y1 < y_column_1 - 50 and y0 > y_table_end and x1 < x_column_1 + 10 and x1 > x_column_0 - 10:
                if obj.text:
                    lines[y0].append(obj.text)
    sorted_keys = sorted(lines.keys(), key=lambda y: -y)[:2]
    required_completion_date = ' '.join([lines[y][0].strip() for y in sorted_keys])
    return required_completion_date


def parse_school_name(doc):
    #
    # finding column "Site" in table
    label = doc.pq('LTTextLineHorizontal:contains("Site")')
    x_column_0 = float(label.attr('x0'))
    x_column_1 = float(label.attr('x1'))
    y_column_1 = float(label.attr('y1'))
    #
    # finding work end of table
    label = doc.pq('LTTextLineHorizontal:contains("Please read")')
    y_table_end = float(label.attr('y1'))
    #
    # finding school name in table
    lines = defaultdict(list)
    for id, obj in enumerate(doc.get_tree().iter()):
        items = dict(obj.items())
        if items.get('bbox', None) is not None:
            (x0, y0, x1, y1) = eval(items['bbox'])
            if x1 < x_column_1 + 100 and x1 > x_column_0 and y1 < y_column_1 and y0 > y_table_end:
                if obj.text:
                    lines[y0].append(obj.text)
    sorted_keys = sorted(lines.keys(), key=lambda y: -y)[:2]
    school_attrs = lines[sorted_keys[0]][0].split()[2:]
    school_attrs.extend(lines[sorted_keys[1]])
    school_name = ' '.join([x.strip() for x in school_attrs])
    logger.info('School name: %s' % school_name)
    return school_name


def parse_description(doc):
    #
    # finding column "Description" in table
    label = doc.pq('LTTextLineHorizontal:contains("Description")')
    x_column_0 = float(label.attr('x0'))
    x_column_1 = float(label.attr('x1'))
    y_column_0 = float(label.attr('y0'))
    y_column_1 = float(label.attr('y1'))
    #
    # finding work end of table
    label = doc.pq('LTTextLineHorizontal:contains("Please read")')
    y_table_end = float(label.attr('y1'))
    #
    # finding description in table
    lines = defaultdict(list)
    for id, obj in enumerate(doc.get_tree().iter()):
        items = dict(obj.items())
        if items.get('bbox', None) is not None:
            (x0, y0, x1, y1) = eval(items['bbox'])
            if y1 < y_column_1-50 and y0 > y_table_end and x1 < x_column_1 + 100 and x1 > x_column_0 - 100:
                if obj.text:
                    lines[y0].append([obj.text, x0])
    sorted_keys = sorted(lines.keys(), key=lambda y: -y)
    #
    # Get description first line
    desc_items = sorted(lines[sorted_keys[0]], key=lambda x: x[1])
    description = ' '.join([item[0].strip() for item in desc_items])
    #
    # Get priority
    prioiry_line_idx = len(sorted_keys) - 4
    priority_items = sorted(lines[sorted_keys[prioiry_line_idx]], key=lambda x: x[1])
    priority = ' '.join([x[0].strip() for x in priority_items])
    
    priority = int(priority.split(':')[1].strip())
    #
    logger.info('Description: %s' % description)
    logger.info('Priority: %d' % priority)
    return description, priority


def parse_document(input_file, delete_input=True):
    logger.info('Start parsing: %s' % input_file)
    doc = pdfquery.PDFQuery(input_file)
    doc.load()
    #
    # parsing fields
    purchase_order_date = parse_purchase_order_date(doc)
    purchase_order_number = parse_purchase_order_number(doc)
    work_order = parse_work_order(doc)
    school_name = parse_school_name(doc)
    required_completion_date = parse_required_completion_date(doc)
    description, priority = parse_description(doc)
    logger.info('Stop parsing')
    #
    # remove pdf file
    if delete_input:
        os.unlink(input_file)
    order = {
             'purchase_order_number':    purchase_order_number,
             'purchase_order_date':      purchase_order_date,
             'required_completion_date': required_completion_date,
             'work_order':               work_order,
             'school_name':              school_name,
             'description':              description,
             'priority':                 priority
            }
    return order


def main():
    pass
if __name__ == '__main__':
    main()
