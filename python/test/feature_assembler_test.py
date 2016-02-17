__copyright__ = "Copyright 2016, Netflix, Inc."
__license__ = "Apache, Version 2.0"

import unittest
from asset import Asset
import config
from feature_assembler import FeatureAssembler

class FeatureAssemblerTest(unittest.TestCase):

    def tearDown(self):
        if hasattr(self, 'fassembler'):
            self.fassembler.remove_logs()
            self.fassembler.remove_results()
        pass

    def test_feature_assembler_whole_feature(self):
        print 'test on feature assembler with whole feature...'
        ref_path = config.ROOT + "/resource/yuv/src01_hrc00_576x324.yuv"
        dis_path = config.ROOT + "/resource/yuv/src01_hrc01_576x324.yuv"
        asset = Asset(dataset="test", content_id=0, asset_id=0,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=dis_path,
                      asset_dict={'width':576, 'height':324})

        asset_original = Asset(dataset="test", content_id=0, asset_id=1,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=ref_path,
                      asset_dict={'width':576, 'height':324})

        self.fassembler = FeatureAssembler(
            feature_dict = {'VMAF_feature':'all'},
            assets = [asset, asset_original],
            logger=None,
            log_file_dir=config.ROOT + "/workspace/log_file_dir",
            fifo_mode=True,
            delete_workdir=True,
            result_store=None
        )

        self.assertEquals(self.fassembler.ordered_scores_key_list,
                          ['VMAF_feature_adm_scores',
                           'VMAF_feature_ansnr_scores',
                           'VMAF_feature_motion_scores',
                           'VMAF_feature_vif_scores'])

        self.fassembler.run()

        results = self.fassembler.results

        self.assertEqual(results[0]['VMAF_feature_vif_score'], 0.44417014583333336)
        self.assertEqual(results[0]['VMAF_feature_motion_score'], 3.5916076041666667)
        self.assertEqual(results[0]['VMAF_feature_adm_score'], 0.91552422916666665)
        self.assertEqual(results[0]['VMAF_feature_ansnr_score'], 22.533456770833329)

        self.assertEqual(results[1]['VMAF_feature_vif_score'], 1.0)
        self.assertEqual(results[1]['VMAF_feature_motion_score'], 3.5916076041666667)
        self.assertEqual(results[1]['VMAF_feature_adm_score'], 1.0)
        self.assertEqual(results[1]['VMAF_feature_ansnr_score'], 30.030914145833322)

    def test_feature_assembler_selected_atom_feature(self):
        print 'test on feature assembler with selected atom features...'
        ref_path = config.ROOT + "/resource/yuv/src01_hrc00_576x324.yuv"
        dis_path = config.ROOT + "/resource/yuv/src01_hrc01_576x324.yuv"
        asset = Asset(dataset="test", content_id=0, asset_id=0,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=dis_path,
                      asset_dict={'width':576, 'height':324})

        asset_original = Asset(dataset="test", content_id=0, asset_id=1,
                      workdir_root=config.ROOT + "/workspace/workdir",
                      ref_path=ref_path,
                      dis_path=ref_path,
                      asset_dict={'width':576, 'height':324})

        self.fassembler = FeatureAssembler(
            feature_dict = {'VMAF_feature':['vif', 'motion']},
            assets = [asset, asset_original],
            logger=None,
            log_file_dir=config.ROOT + "/workspace/log_file_dir",
            fifo_mode=True,
            delete_workdir=True,
            result_store=None
        )

        self.assertEquals(self.fassembler.ordered_scores_key_list,
                          ['VMAF_feature_motion_scores',
                           'VMAF_feature_vif_scores'])

        self.fassembler.run()

        results = self.fassembler.results

        self.assertEqual(results[0]['VMAF_feature_vif_score'], 0.44417014583333336)
        self.assertEqual(results[0]['VMAF_feature_motion_score'], 3.5916076041666667)

        self.assertEqual(results[1]['VMAF_feature_vif_score'], 1.0)
        self.assertEqual(results[1]['VMAF_feature_motion_score'], 3.5916076041666667)

        self.assertTrue('VMAF_feature_ansnr_scores' not in results[0].result_dict)
        self.assertTrue('VMAF_feature_adm_scores' not in results[0].result_dict)

        self.assertTrue('VMAF_feature_ansnr_scores' not in results[1].result_dict)
        self.assertTrue('VMAF_feature_adm_scores' not in results[1].result_dict)

