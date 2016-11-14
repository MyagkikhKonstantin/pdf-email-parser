# -*- coding: utf-8 -*-
import os
import unittest
from email_parser.parse_order import parse_document


class TestDocumentParser(unittest.TestCase):
    def setUp(self):
        self.input_dir = os.path.join(os.path.dirname(__file__), 'test_data')

    def test_1_pdf(self):
        order = parse_document(os.path.join(self.input_dir, '1.pdf'),
                               delete_input=False)
        self.assertEqual('D1656263', order['purchase_order_number'])
        self.assertEqual('08/11/2016 11:45', order['purchase_order_date'])
        self.assertEqual('11/11/2016 11:45', order['required_completion_date'])
        self.assertEqual('A1885233', order['work_order'])
        self.assertEqual('Southern River College', order['school_name'])
        self.assertEqual('PA siren very hard to hear and PA speaker very',
                         order['description'])
        self.assertEqual(2, order['priority'])

    def test_2_pdf(self):
        order = parse_document(os.path.join(self.input_dir, '2.pdf'),
                               delete_input=False)
        self.assertEqual('D1650729', order['purchase_order_number'])
        self.assertEqual('26/10/2016 13:28', order['purchase_order_date'])
        self.assertEqual('31/10/2016 13:28', order['required_completion_date'])
        self.assertEqual('A1879702', order['work_order'])
        self.assertEqual('Canning Vale College', order['school_name'])
        self.assertEqual('2x PAC lights blown located theatre',
                         order['description'])
        self.assertEqual(2, order['priority'])

    def test_3_pdf(self):
        order = parse_document(os.path.join(self.input_dir, '3.pdf'),
                               delete_input=False)
        self.assertEqual('D1652073', order['purchase_order_number'])
        self.assertEqual('28/10/2016 15:07', order['purchase_order_date'])
        self.assertEqual('08/11/2016 15:07', order['required_completion_date'])
        self.assertEqual('A1881046', order['work_order'])
        self.assertEqual('West Byford Primary School', order['school_name'])
        self.assertEqual('PA System not working located Music Room',
                         order['description'])
        self.assertEqual(3, order['priority']) 

if __name__ == '__main__':
    unittest.main()
