import unittest
import textwrap
import os
import sys
sys.path.append('../')
import app



class TestMailPartsCsvLineLoader(unittest.TestCase):
    def test_create_by_factory(self):
        loader = app.MailPartsLoaderFactory.create(app.LoadType.CSV_LINE)
        self.assertTrue(isinstance(loader, app.mailpartsloader.MailPartsCsvLineLoader))

    def test_csv_indexes_max_value(self):
        csv_indexes = app.mailpartsloader.CsvIndexes(**dict(
            test_idx1 = 1,
            test_idx2 = 2,
            test_idx3 = 3
        ))
        self.assertEqual(csv_indexes.max_value(), 3)

    def test_csv_indexes_value_of(self):
        csv_indexes = app.mailpartsloader.CsvIndexes(**dict(
            test_idx1 = 1,
            test_idx2 = 2,
            test_idx3 = 3
        ))
        self.assertEqual(csv_indexes.value_of('test_idx2'), 2)
        self.assertEqual(csv_indexes.value_of('non_exists'), -1)
        self.assertEqual(csv_indexes.value_of('non_exists', default=99), 99)

    def test_load_line_counts(self):
        csv_lines = [
            'mailfrom@example1.com,mailto@example1.com,subject,contents',
            'mailfrom@example2.com,mailto@example2.com,subject,contents',
            'mailfrom@example3.com,mailto@example3.com,subject,contents',
        ]
        loader = app.mailpartsloader.MailPartsCsvLineLoader(settings = dict(
            mailfrom_idx = 0,
            mailto_idx   = 1,
            subject_idx  = 2,
            contents_idx = 3
        ))
        mailpartslist = loader.load(csv_lines)
        self.assertEqual(len(mailpartslist.all()), 3)

    def test_load_line_counts_sames(self):
        csv_lines = [
            'mailfrom@example1.com,mailto@example1.com,subject,contents',
            'mailfrom@example1.com,mailto@example1.com,subject,contents',
            'mailfrom@example1.com,mailto@example1.com,subject,contents',
        ]
        loader = app.mailpartsloader.MailPartsCsvLineLoader(settings = dict(
            mailfrom_idx = 0,
            mailto_idx   = 1,
            subject_idx  = 2,
            contents_idx = 3
        ))
        mailpartslist = loader.load(csv_lines)
        self.assertEqual(len(mailpartslist.all()), 3)

    def test_skip_broken_line(self):
        csv_lines = [
            '',
            'mailfrom@example1.com,mailto@example1.com'
        ]
        loader = app.mailpartsloader.MailPartsCsvLineLoader(settings = dict(
            mailfrom_idx = 0,
            mailto_idx   = 1,
            subject_idx  = 2,
            contents_idx = 3
        ))
        mailpartslist = loader.load(csv_lines)
        self.assertEqual(len(mailpartslist.all()), 0)

class TestMailPartsJsonFileLoader(unittest.TestCase):
    def test_load(self):
        loader = app.mailpartsloader.MailPartsJsonFileLoader(**dict(
            mailto_prop_name   = 'mailto',
            mailfrom_prop_name = 'mailfrom',
            subject_prop_name  = 'subject',
            contents_prop_name = 'contents'
        ))
        test_file_path = f'{os.path.dirname(__file__)}/test_json.json'
        mailpartslist = loader.load(test_file_path)
        all_mailpartslist = mailpartslist.all()
        self.assertEqual(len(all_mailpartslist), 3)
        self.assertEqual(all_mailpartslist[0].mail_from, 'example1@example1.com')
        self.assertEqual(all_mailpartslist[0].mail_to  , 'example1@example1.com')
        self.assertEqual(all_mailpartslist[0].subject  , 'test_subject1')
        self.assertEqual(all_mailpartslist[0].contents , 'test_contents1')

        self.assertEqual(all_mailpartslist[1].mail_from, 'example2@example2.com')
        self.assertEqual(all_mailpartslist[1].mail_to  , 'example2@example2.com')
        self.assertEqual(all_mailpartslist[1].subject  , 'test_subject2')
        self.assertEqual(all_mailpartslist[1].contents , 'test_contents2')

        self.assertEqual(all_mailpartslist[2].mail_from, 'example3@example3.com')
        self.assertEqual(all_mailpartslist[2].mail_to  , 'example3@example3.com')
        self.assertEqual(all_mailpartslist[2].subject  , 'test_subject3')
        self.assertEqual(all_mailpartslist[2].contents , 'test_contents3')

