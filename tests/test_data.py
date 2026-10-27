"""Dependency-free content, provenance and packaging regression checks."""
import copy
import csv
import json
import re
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from validate import validate

class ManualDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=json.loads((ROOT/'manual_data.json').read_text())
        cls.ref=cls.data['reference']
        cls.recipes={r['name']:r for r in cls.ref['recipes']}
        cls.techs={t['name']:t for t in cls.ref['technologies']}
        cls.entities={e['name']:e for e in cls.ref['entities']}

    def test_structure_and_graph(self):
        validate(self.data)
        self.assertEqual(len(self.ref['recipes']),206)
        self.assertEqual(len(self.ref['technologies']),196)
        self.assertEqual(len(self.ref['fluids']),8)
        self.assertEqual(sum(len(c['steps']) for c in self.data['chapters']),140)
        self.assertEqual({c['id'] for c in self.data['chapters']},{'setup','movement','mining','power','belts','automation','redgreen','defense','steel','trains1','trains2','fluids','oil','blue','robots','blueprints','circuits','late','nuclear','modules','rocket','qol','linux','debug'})

    def test_fail_closed_on_broken_links(self):
        damaged=copy.deepcopy(self.data);damaged['topics'][0]['recipes'].append('missing-recipe')
        with self.assertRaisesRegex(ValueError,'Missing topic recipe'):validate(damaged)
        damaged=copy.deepcopy(self.data);damaged['reference']['technologies'][0]['prerequisites'].append(damaged['reference']['technologies'][0]['name'])
        with self.assertRaisesRegex(ValueError,'cycle'):validate(damaged)

    def test_exact_science_batches(self):
        expected={'automation-science-pack':(5,1),'logistic-science-pack':(6,1),'military-science-pack':(10,2),'chemical-science-pack':(24,2),'production-science-pack':(21,3),'utility-science-pack':(21,3)}
        for name,(seconds,batch) in expected.items():
            with self.subTest(name=name):
                r=self.recipes[name];self.assertEqual(r['energy_required'],seconds);self.assertEqual(r['results'][0]['amount'],batch)

    def test_exact_rocket_and_satellite(self):
        self.assertEqual({p['name']:p['amount'] for p in self.recipes['satellite']['ingredients']},{'low-density-structure':100,'solar-panel':100,'accumulator':100,'radar':5,'processing-unit':100,'rocket-fuel':50})
        self.assertEqual({p['name']:p['amount'] for p in self.recipes['rocket-part']['ingredients']},{'processing-unit':10,'low-density-structure':10,'rocket-fuel':10})
        self.assertEqual(self.entities['rocket-silo']['rocket_parts_required'],100)
        self.assertEqual(self.techs['rocket-silo']['unit']['count'],1000)
        self.assertNotIn('military-science-pack',[x[0] for x in self.techs['rocket-silo']['unit']['ingredients']])

    def test_trigger_gates_are_explicit(self):
        self.assertEqual(self.techs['steam-power']['research_trigger']['count'],50)
        self.assertEqual(self.techs['electronics']['research_trigger']['count'],10)
        self.assertEqual(self.techs['automation-science-pack']['research_trigger']['item'],'lab')
        self.assertEqual(self.techs['automation']['unit']['count'],10)
        lessons={c['id']:c for c in self.data['chapters']}
        self.assertIn('50 iron',lessons['mining']['steps'][3])
        self.assertIn('craft a lab',lessons['automation']['steps'][0])

    def test_catalyst_and_probability_records(self):
        kov={p['name']:p for p in self.recipes['kovarex-enrichment-process']['results']}
        self.assertEqual(kov['uranium-235']['ignored_by_productivity'],40)
        self.assertEqual(kov['uranium-238']['ignored_by_productivity'],2)
        uranium=self.recipes['uranium-processing']['results']
        self.assertAlmostEqual(sum(p['shared_probability']['max']-p['shared_probability']['min'] for p in uranium),1)
        self.assertEqual(uranium[0]['shared_probability']['max'],0.007)

    def test_generated_barrel_names_and_unlocks(self):
        generated=[r for r in self.ref['recipes'] if r['source']=='base/data-updates.lua']
        self.assertEqual(len(generated),14)
        self.assertIn('water-barrel',self.recipes)
        self.assertNotIn('fill-water-barrel',self.recipes)
        self.assertEqual(self.recipes['water-barrel']['energy_required'],0.2)
        self.assertEqual(next(p['amount'] for p in self.recipes['water-barrel']['ingredients'] if p['type']=='fluid'),50)
        self.assertNotIn('steam-barrel',self.recipes)

    def test_provenance_and_charging_correction(self):
        self.assertEqual(self.ref['provenance']['commit'],'acf5a342afcb66c066b9d88d202e8622112da117')
        self.assertTrue(all(re.fullmatch('[a-f0-9]{64}',v) for v in self.ref['provenance']['sha256'].values()))
        port=self.entities['roboport']
        self.assertEqual(port['charging_energy'],'500kW')
        self.assertEqual(len(port['charging_offsets']),4)
        self.assertEqual(port['logistics_radius'],25)
        self.assertEqual(port['construction_radius'],55)

    def test_generated_data_agrees(self):
        html=(ROOT/'index.html').read_text()
        embedded=re.search(r'<script id="manualdata" type="application/json">(.*?)</script>',html,re.S)
        self.assertIsNotNone(embedded)
        self.assertEqual(json.loads(embedded[1]),self.data)
        self.assertNotRegex(html,r'<(?:script|img)[^>]+src=["\']https?://')
        self.assertNotRegex(html,r'<link[^>]+href=["\']https?://')
        with (ROOT/'controls.csv').open() as f:self.assertEqual(list(csv.DictReader(f)),self.data['controls'])

    def test_archive_rebuild(self):
        with zipfile.ZipFile(ROOT/'factorio_2_1_24_offline_manual_and_agent_pack.zip') as z:
            self.assertIsNone(z.testzip())
            for name in z.namelist():self.assertEqual(z.read(name),(ROOT/name).read_bytes(),name)
            with tempfile.TemporaryDirectory(prefix='factorio-package-test-') as temp:
                extracted=Path(temp)/'source';z.extractall(extracted)
                output=Path(temp)/'delivery'
                subprocess.run([sys.executable,str(extracted/'build.py'),'--output-dir',str(output)],check=True,capture_output=True)
                for name in ('index.html','manual_data.json','controls.csv','README.md','AGENT_HANDOFF.md','AUDIT.md'):
                    self.assertEqual((output/name).read_bytes(),(ROOT/name).read_bytes(),name)

if __name__=='__main__':unittest.main()
