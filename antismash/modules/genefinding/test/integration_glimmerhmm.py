# License: GNU Affero General Public License v3 or later
# A copy of GNU AGPL v3 should have been included in this software package in LICENSE.txt.

import os
from unittest import TestCase

from antismash.config.args import Config, simple_options
from antismash.common.deprecated import parse_input_sequence, pre_process_sequences
from antismash.common.path import get_full_path
import antismash.modules.genefinding as genefinding
from antismash.modules.genefinding import run_glimmerhmm as glimmerhmm

class TestGlimmerHMM(TestCase):
    def setUp(self):
        self.options = Config(simple_options(genefinding, ['--taxon', 'fungi',
                '--genefinding-tool', 'glimmerhmm']))
        self.data_location = get_full_path(__file__, "data")

    def tearDown(self):
        Config().__dict__.clear()

    def data_file(self, filename):
        return os.path.join(self.data_location, filename)

    def test_fumigatus_cluster(self):
        record = parse_input_sequence(self.data_file('fumigatus.cluster1.fna'),
                self.options)[0]
        pre_process_sequences([record], self.options, genefinding)
        assert len(record.features) == 11
        for feature in record.features:
            assert feature.type == 'CDS'
