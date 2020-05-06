"""
This module contains some tests for Trycycler. To run them, execute `pytest` from the root
Trycycler directory.

Copyright 2020 Ryan Wick (rrwick@gmail.com)
https://github.com/rrwick/Trycycler

This file is part of Trycycler. Trycycler is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version. Trycycler is distributed
in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details. You should have received a copy of the GNU General Public License along with Trycycler.
If not, see <http://www.gnu.org/licenses/>.
"""

import pathlib
import pytest
import tempfile

import trycycler.cluster


def test_input_assemblies_1():
    # Tests the function on two FASTAs without problems.
    total_lengths = trycycler.cluster.check_input_assemblies(['test/test_cluster/contigs_1.fasta',
                                                              'test/test_cluster/contigs_2.fasta'])
    assert total_lengths == {'A': 48, 'B': 24}


def test_input_assemblies_2():
    # Ensures that the function doesn't accept duplicate contig names.
    with pytest.raises(SystemExit) as e:
        trycycler.cluster.check_input_assemblies(['test/test_cluster/contigs_1.fasta',
                                                  'test/test_cluster/contigs_2.fasta',
                                                  'test/test_cluster/duplicate_contig_names.fasta'])
    assert 'duplicate' in str(e.value)


def test_input_assemblies_3():
    # Ensures that the function doesn't accept only one assembly.
    with pytest.raises(SystemExit) as e:
        trycycler.cluster.check_input_assemblies(['test/test_cluster/contigs_1.fasta'])
    assert 'two or more' in str(e.value)


def test_input_assemblies_4():
    # Ensures that the function doesn't accept non-FASTA files.
    with pytest.raises(SystemExit) as e:
        trycycler.cluster.check_input_assemblies(['test/test_cluster/contigs_1.fasta',
                                                  'test/test_cluster/not_a_fasta_file'])
    assert 'not in FASTA format' in str(e.value)


def test_input_assemblies_5():
    # Ensures that the function doesn't accept files which don't exist.
    with pytest.raises(SystemExit) as e:
        trycycler.cluster.check_input_assemblies(['test/test_cluster/contigs_1.fasta',
                                                  'test/test_cluster/not_a_file'])
    assert 'could not find' in str(e.value)


def get_values_for_complete_linkage_tests():
    seqs = {'A': '', 'B': '', 'C': ''}
    seq_names = ['A', 'B', 'C']
    depths = {'A': 100.0, 'B': 100.0, 'C': 100.0}
    threshold = 0.01
    return seqs, seq_names, depths, threshold


def test_complete_linkage_1():
    seqs, seq_names, depths, threshold = get_values_for_complete_linkage_tests()
    distances = {('A', 'A'): 0.0, ('A', 'B'): 0.0, ('A', 'C'): 0.0,
                 ('B', 'A'): 0.0, ('B', 'B'): 0.0, ('B', 'C'): 0.0,
                 ('C', 'A'): 0.0, ('C', 'B'): 0.0, ('C', 'C'): 0.0}
    with tempfile.TemporaryDirectory() as temp_dir:
        cluster_numbers = trycycler.cluster.complete_linkage(seqs, seq_names, depths, distances,
                                                             threshold, pathlib.Path(temp_dir))
    assert len(set(cluster_numbers.values())) == 1


def test_complete_linkage_2():
    seqs, seq_names, depths, threshold = get_values_for_complete_linkage_tests()
    distances = {('A', 'A'): 0.0, ('A', 'B'): 0.0, ('A', 'C'): 0.1,
                 ('B', 'A'): 0.0, ('B', 'B'): 0.0, ('B', 'C'): 0.1,
                 ('C', 'A'): 0.1, ('C', 'B'): 0.1, ('C', 'C'): 0.0}
    with tempfile.TemporaryDirectory() as temp_dir:
        cluster_numbers = trycycler.cluster.complete_linkage(seqs, seq_names, depths, distances,
                                                             threshold, pathlib.Path(temp_dir))
    assert len(set(cluster_numbers.values())) == 2


def test_complete_linkage_3():
    seqs, seq_names, depths, threshold = get_values_for_complete_linkage_tests()
    distances = {('A', 'A'): 0.000, ('A', 'B'): 0.008, ('A', 'C'): 0.016,
                 ('B', 'A'): 0.008, ('B', 'B'): 0.000, ('B', 'C'): 0.008,
                 ('C', 'A'): 0.016, ('C', 'B'): 0.008, ('C', 'C'): 0.000}
    with tempfile.TemporaryDirectory() as temp_dir:
        cluster_numbers = trycycler.cluster.complete_linkage(seqs, seq_names, depths, distances,
                                                             threshold, pathlib.Path(temp_dir))
    assert len(set(cluster_numbers.values())) == 2


def test_complete_linkage_4():
    seqs, seq_names, depths, threshold = get_values_for_complete_linkage_tests()
    distances = {('A', 'A'): 0.000, ('A', 'B'): 0.012, ('A', 'C'): 0.024,
                 ('B', 'A'): 0.012, ('B', 'B'): 0.000, ('B', 'C'): 0.012,
                 ('C', 'A'): 0.024, ('C', 'B'): 0.012, ('C', 'C'): 0.000}
    with tempfile.TemporaryDirectory() as temp_dir:
        cluster_numbers = trycycler.cluster.complete_linkage(seqs, seq_names, depths, distances,
                                                             threshold, pathlib.Path(temp_dir))
    assert len(set(cluster_numbers.values())) == 3


def test_load_assembly_sequences_1():
    seqs, seq_names, fasta_names = \
        trycycler.cluster.load_assembly_sequences(['test/test_cluster/assembly_1.fasta'])
    assert list(seqs.keys()) == ['A_A']


def test_load_assembly_sequences_2():
    seqs, seq_names, fasta_names = \
        trycycler.cluster.load_assembly_sequences(['test/test_cluster/assembly_with_hashes.fasta'])
    assert list(seqs.keys()) == ['A_A_B_C']


def test_load_assembly_sequences_3():
    seqs, seq_names, fasta_names = \
        trycycler.cluster.load_assembly_sequences(['test/test_cluster/assembly_3.fasta'])
    assert list(seqs.keys()) == ['A_A']


def test_get_contig_depths_1():
    assemblies = ['test/test_cluster/assembly_1.fasta']
    reads = 'test/test_cluster/reads.fastq'
    assembly_lengths = {'A': 10000}
    seqs, seq_names, fasta_names = trycycler.cluster.load_assembly_sequences(assemblies)
    depths, depth_filter = \
        trycycler.cluster.get_contig_depths(assemblies, seqs, seq_names, fasta_names, reads,
                                            8, assembly_lengths, 0.1)
    assert 1.9 < depths['A_A'] < 2.1
    assert depth_filter == {'A_A': True}


def test_get_contig_depths_2():
    assemblies = ['test/test_cluster/assembly_2.fasta']
    reads = 'test/test_cluster/reads.fastq'
    assembly_lengths = {'A': 11000}
    seqs, seq_names, fasta_names = trycycler.cluster.load_assembly_sequences(assemblies)
    depths, depth_filter = \
        trycycler.cluster.get_contig_depths(assemblies, seqs, seq_names, fasta_names, reads,
                                            8, assembly_lengths, 0.1)
    assert 1.9 < depths['A_A'] < 2.1
    assert depths['A_B'] == 0.0
    assert depth_filter == {'A_A': True, 'A_B': False}


def test_get_contig_depths_3():
    assemblies = ['test/test_cluster/assembly_with_hashes.fasta']
    reads = 'test/test_cluster/reads.fastq'
    assembly_lengths = {'A': 10000}
    seqs, seq_names, fasta_names = trycycler.cluster.load_assembly_sequences(assemblies)
    depths, depth_filter = \
        trycycler.cluster.get_contig_depths(assemblies, seqs, seq_names, fasta_names, reads,
                                            8, assembly_lengths, 0.1)
    assert 1.9 < depths['A_A_B_C'] < 2.1
    assert depth_filter == {'A_A_B_C': True}
