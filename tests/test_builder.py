import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("documents",ROOT/"scripts/quotes.py")
documents=importlib.util.module_from_spec(spec)
spec.loader.exec_module(documents)

class BuilderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work = Path(self.temp.name)

    def write(self, data, name="input.json"):
        path = self.work / name
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        return path

    def quotes(self):
        return json.loads((ROOT / "assets/demo.json").read_text())

    def test_document_money_rounds_lines_then_tax(self):
        result = documents.calculate({"lines":[{"description":"A","quantity":"0.5","unit_minor":1},{"description":"B","quantity":"0.5","unit_minor":1}],"tax_bps":2500})
        self.assertEqual(result["line_minor"],[1,1])
        self.assertEqual((result["subtotal_minor"],result["tax_minor"],result["total_minor"]),(2,1,3))

    def test_document_known_quote_totals_and_client_separation(self):
        result = documents.build(self.write(self.quotes()), self.work/"out")
        self.assertEqual([i["calculated"]["total_minor"] for i in result["items"]],[275550,132000])
        first = (self.work/"out/Q-2026-001.html").read_text()
        self.assertIn("North Pier Consulting",first)
        self.assertNotIn("Common Ground Practice",first)
        self.assertIn("AUD 2,755.50",first)
        self.assertEqual(result["pdf"],"not_generated")

    def test_document_mismatched_supplied_total_blocks_whole_batch(self):
        data = self.quotes()
        data["quotes"][1]["total_minor"] = 1
        with self.assertRaises(documents.DocumentError):
            documents.build(self.write(data),self.work/"out")
        self.assertFalse((self.work/"out").exists())

    def test_document_rejects_nonfinite_or_negative_quantities(self):
        for quantity in ("NaN","Infinity","-1","0"):
            with self.subTest(quantity=quantity),self.assertRaises(documents.DocumentError):
                documents.calculate({"lines":[{"description":"A","quantity":quantity,"unit_minor":1}]})

    def test_document_does_not_infer_zero_tax(self):
        data = self.quotes()
        del data['quotes'][0]['tax_bps']
        with self.assertRaisesRegex(documents.DocumentError,'tax_bps is required'):
            documents.build(self.write(data),self.work/'out')

    def test_document_rejects_floating_price_and_unsupported_currency(self):
        data = self.quotes()
        data["quotes"][0]["lines"][0]["unit_minor"] = 12.1
        with self.assertRaises(documents.DocumentError):
            documents.build(self.write(data),self.work/"out")
        data = self.quotes()
        data["quotes"][0]["currency"] = "JPY"
        with self.assertRaises(documents.DocumentError):
            documents.build(self.write(data),self.work/"out")

    def test_nonobject_input_is_rejected(self):
        with self.assertRaises(documents.DocumentError):
            documents.build(self.write([]),self.work/"out")

if __name__=="__main__":
    unittest.main()
