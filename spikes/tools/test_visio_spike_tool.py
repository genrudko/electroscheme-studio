import json, pathlib, subprocess, sys, unittest, zipfile
ROOT=pathlib.Path(__file__).resolve().parents[1]
TOOL=ROOT/"tools"/"visio_spike_tool.py"
class VisioFixtureTests(unittest.TestCase):
 def inspect(self,kind,name):
  p=subprocess.run([sys.executable,str(TOOL),"inspect",kind,str(ROOT/"shared"/"fixtures"/"visio"/name)],text=True,capture_output=True,check=True)
  return json.loads(p.stdout)
 def test_vsdx(self):
  r=self.inspect("vsdx","controlled-minimal.vsdx"); self.assertEqual(r["status"],"ok"); self.assertIn("visio/pages/page1.xml",r["parts"]); self.assertTrue({"1","2","3"}.issubset(set(r["sourceIds"])))
 def test_vssx(self):
  r=self.inspect("vssx","controlled-master.vssx"); self.assertEqual(r["status"],"ok"); self.assertIn("visio/masters/master1.xml",r["parts"])
 def test_generated_package_structure(self):
  with zipfile.ZipFile(ROOT/"shared"/"fixtures"/"visio"/"controlled-minimal.vsdx") as z: self.assertIn("docProps/core.xml",z.namelist())
if __name__=="__main__": unittest.main()
