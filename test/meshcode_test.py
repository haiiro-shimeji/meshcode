# coding:utf-8

import unittest
import meshcode
from meshcode import Level

class TestMeshCode(unittest.TestCase):

    def setUp(self):
        pass

    def testFromPoint(self):

        for f in [
            [35.68823693, 139.70974445, Level.L1, "5339"],
            [4.30259108, 104.19433594, Level.L1, "0604"], # Zero padding for first mesh code
            [35.68823693, 139.70974445, Level.L2, "533945"],
            [35.35097596, 139.01000977, Level.L2, "533900"],  # Zero padding for second mesh code
            [35.68823693, 139.70974445, Level.L3, "53394526"],
            [35.68539612, 139.70335007, Level.HALF, "533945261"],
            [35.68536126, 139.70935822, Level.HALF, "533945262"],
            [35.68961373, 139.70315695, Level.HALF, "533945263"],
            [35.68823693, 139.70974445, Level.HALF, "533945264"],
            [35.68855064, 139.70156908, Level.QUARTER, "5339452631"],
            [35.68853321, 139.70468581, Level.QUARTER, "5339452632"],
            [35.69062889, 139.70156372, Level.QUARTER, "5339452633"],
            [35.69070295, 139.70476627, Level.QUARTER, "5339452634"],
            [35.69009299, 139.70078588, Level.EIGHTH, "53394526331"],
            [35.69006685, 139.70235229, Level.EIGHTH, "53394526332"],
            [35.69112993, 139.7007966, Level.EIGHTH, "53394526333"],
            [35.69112993, 139.70234156, Level.EIGHTH, "53394526334"],
            [35.68539612, 139.70335007, Level.TWENTYTH, "53394526145"],
        ]:

            lat = f[0]
            lon = f[1]
            level = f[2]
            code = f[3]
            self.assertEqual( code, meshcode.code(lat, lon, level));

    def testBasePointFromCode(self):

        for f in [
            ["5237", Level.L1, 34.666666666666664, 137],
            ["523744", Level.L2, 35.0, 137.5],
            ["52374410", Level.L3, 35.00833333333333,137.5],
            ["523744104", Level.HALF, 35.012499999999996, 137.50625],
            ["5237441044", Level.QUARTER, 35.014583333333334, 137.509375],
            ["52374410443", Level.EIGHTH, 35.015625, 137.509375],
            ["52374410496", Level.TWENTYTH, 35.01625, 137.51],
        ]:
            code = f[0]
            level = f[1]
            p = meshcode.basePointFromCode(code, level);
            self.assertAlmostEqual( f[3], p[0], delta=0.001 );
            self.assertAlmostEqual( f[2], p[1], delta=0.001 );

    def testPolygon(self):

        for f in [
            ["5237", Level.L1, 137, 34.666666666666664, 138, 35.33333333333333],
            ["523744", Level.L2, 137.5, 35, 137.625, 35.083333333333336],
            ["52374410", Level.L3, 137.5, 35.00833333333333, 137.5125, 35.016666666666666],
            ["523744104", Level.HALF, 137.50625, 35.012499999999996, 137.5125, 35.016666666666666],
            ["5237441044", Level.QUARTER, 137.509375, 35.014583333333334, 137.51250000000002, 35.016666666666666],
            ["52374410443", Level.EIGHTH, 137.509375, 35.015625, 137.5109375, 35.016666666666666],
            ["52374410496", Level.TWENTYTH, 137.51, 35.01625, 137.510625, 35.016666666666666],
        ]:

            code = f[0]
            level = f[1]
            l = f[2]
            b = f[3]
            r = f[4]
            t = f[5]
            p = meshcode.polygon(code, level);
            lb = p[0];
            rt = p[2];
            self.assertAlmostEqual(l, lb[0], delta=0.00001);
            self.assertAlmostEqual(b, lb[1], delta=0.00001);
            self.assertAlmostEqual(r, rt[0], delta=0.00001);
            self.assertAlmostEqual(t, rt[1], delta=0.00001);
