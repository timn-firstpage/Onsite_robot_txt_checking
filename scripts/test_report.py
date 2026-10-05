"""Offline contract checks using synthetic data, not customer crawl results."""
import copy
import tempfile
import unittest
from pathlib import Path
from openpyxl import load_workbook
from build_report import build, normalize, report_filename


def fixture():
    return {'checklist':[
        {'id':'10.1','check':'10.1 Does robots.txt exist?','result':'No','findings':'Empty robots.txt observed.','coverage':'One synthetic response.'},
        {'id':'10.4','check':'10.4 CSS/JS access','result':'','findings':'No resource export.','unresolved_reason':'Missing SF evidence.','coverage':'Not checked.'},
        {'id':'10.5','check':'10.5 Special pages','result':'NA','findings':'No verifiable objects.','na_reason':'15 candidate paths tested; none verifiable; no transaction performed.','coverage':'Synthetic candidates.'}],
        'issues':[{'check_ids':['10.1'],'issue':'Empty robots.txt','description':'=untrusted description','how_to_fix':'Configure appropriate directives.','addresses':['https://example.com/robots.txt?x=1&y=2']}]}


class ReportTests(unittest.TestCase):
    def test_filename(self):
        self.assertEqual(report_filename('Example','2026-10-05'),'Example_robots_audit_2026-10-05.xlsx')
        self.assertEqual(report_filename('品牌/香港','2026-10-05'),'品牌_香港_robots_audit_2026-10-05.xlsx')
        with self.assertRaises(ValueError): report_filename('Example','2026-02-30')

    def test_export_schema_reasons_urls_and_no_overwrite(self):
        data=fixture(); data['issues'].append(copy.deepcopy(data['issues'][0]))
        data['issues'][0]['addresses'].append(data['issues'][0]['addresses'][0])
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as directory:
            output=Path(directory)/'audit.xlsx'; result=build(data,output)
            self.assertEqual(result['issues'],1)
            wb=load_workbook(output)
            self.assertEqual(wb.sheetnames,['Checklist','Issues'])
            self.assertEqual([c.value for c in wb['Checklist'][1]],['Check','Result','Findings','Coverage'])
            self.assertEqual([c.value for c in wb['Issues'][1]],['Issue','Issue Description','How to Fix','Address'])
            self.assertIn(data['checklist'][2]['na_reason'],wb['Checklist']['C4'].value)
            self.assertIn('Missing SF evidence.',wb['Checklist']['C3'].value)
            self.assertEqual(wb['Checklist']['B3'].value,'Needs Review')
            self.assertEqual(wb['Issues']['D2'].value,data['issues'][0]['addresses'][0])
            self.assertEqual(wb['Issues']['B2'].data_type,'s')
            self.assertEqual(len(wb['Checklist'].data_validations.dataValidation),1)
            wb.close()
            with self.assertRaises(FileExistsError): build(data,output)

    def test_rejects_na_without_reason_and_unknown_without_reason(self):
        for idx,key in [(2,'na_reason'),(1,'unresolved_reason')]:
            data=fixture(); del data['checklist'][idx][key]
            with self.assertRaises(ValueError): normalize(data)

    def test_rejects_false_yes_missing_issue_and_invalid_links(self):
        data=fixture(); data['checklist'][0]['result']='Yes'
        with self.assertRaises(ValueError): normalize(data)
        data=fixture(); data['issues']=[]
        with self.assertRaises(ValueError): normalize(data)
        data=fixture(); data['issues'][0]['check_ids']=['10.7']
        with self.assertRaises(ValueError): normalize(data)

    def test_explicit_review_requires_reason_and_cannot_create_issue(self):
        data=fixture(); data['checklist'][1]['result']='Needs Review'
        checks,_=normalize(data)
        self.assertEqual(checks[1]['result'],'Needs Review')
        del data['checklist'][1]['unresolved_reason']
        with self.assertRaises(ValueError): normalize(data)
        data=fixture(); data['issues'][0]['check_ids']=['10.4']
        with self.assertRaises(ValueError): normalize(data)

    def test_duplicate_check_and_legacy_schema(self):
        data=fixture(); data['checklist'].append(copy.deepcopy(data['checklist'][0]))
        with self.assertRaises(ValueError): normalize(data)
        with self.assertRaises(ValueError): normalize({'overview':[]})

    def test_empty_issue_sheet_and_shared_resource_addresses(self):
        data={'checklist':[{'id':'10.4','check':'10.4 CSS/JS','result':'Yes','findings':'None detected in complete export.','coverage':'2 synthetic pages.'}],'issues':[]}
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as directory:
            build(data,Path(directory)/'audit.xlsx')
            wb=load_workbook(Path(directory)/'audit.xlsx'); self.assertEqual(wb['Issues'].max_row,1); wb.close()
        data=fixture(); data['issues'][0]['addresses']=['https://example.com/a','https://example.com/b','http://example.com/logo.png']
        _,issues=normalize(data)
        self.assertEqual(issues[0]['address'].splitlines(),data['issues'][0]['addresses'])


if __name__=='__main__': unittest.main()
