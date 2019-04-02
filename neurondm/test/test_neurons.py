import os
import unittest
from pathlib import Path
from git import Repo

testing_base = f'/tmp/.neurons-testing-base-{os.getpid()}'
pyel = Path(testing_base, 'compiled')
tel = Path(testing_base)



class TestNeurons(unittest.TestCase):
    def setUp(self):
        if not pyel.exists():
            pyel.mkdir(parents=True)  # recrusive clean is called after every test
            (pyel / '__init__.py').touch()

        repo = Repo.init(testing_base)

    def tearDown(self):
        def recursive_clean(path):
            for thing in path.iterdir():
                if thing.is_dir():
                    recursive_clean(thing)
                else:
                    thing.unlink()  # will rm the file

            path.rmdir()

        path = Path(testing_base)
        if path.exists():
            recursive_clean(path)

    def test_roundtrip_ttl(self):
        from neurondm import Config, Neuron, Phenotype, NegPhenotype

        config = Config('test-ttl', ttl_export_dir=tel, py_export_dir=pyel)
        Neuron(Phenotype('TEMP:turtle-phenotype'))
        Neuron(NegPhenotype('TEMP:turtle-phenotype'))
        config.write()

        config2 = Config('test-ttl', ttl_export_dir=tel, py_export_dir=pyel)
        config2.load_existing()
        config2.write_python()

        config3 = Config('test-ttl', ttl_export_dir=tel, py_export_dir=pyel)
        config3.load_python()

        assert config.existing_pes is not config2.existing_pes is not config3.existing_pes
        assert config.neurons() == config2.neurons() == config3.neurons()

    def test_roundtrip_py(self):
        from neurondm import Config, Neuron, Phenotype, NegPhenotype

        config = Config('test-py', ttl_export_dir=tel, py_export_dir=pyel)
        n1 = Neuron(Phenotype('TEMP:python-phenotype'))
        n2 = Neuron(NegPhenotype('TEMP:python-phenotype'))
        assert n1 != n2
        config.write_python()

        config2 = Config('test-py', ttl_export_dir=tel, py_export_dir=pyel)
        config2.load_python()  # FIXME load existing python ...
        config2.write()

        config3 = Config('test-py', ttl_export_dir=tel, py_export_dir=pyel)
        config3.load_existing()

        assert config.existing_pes is not config2.existing_pes is not config3.existing_pes
        assert config.neurons() == config2.neurons() == config3.neurons()

    # TODO make sure this runs after cli test? it should ...
    # but then we need to keep the output of ndl around
    def test_load_existing(self):
        from neurondm.lang import Neuron, Config
        config = Config('neuron_data_lifted')
        config.load_existing()
        assert len(Neuron.load_graph)
        neurons = Neuron.neurons()
        assert neurons

    def test_zz_adopt(self):
        from neurondm.lang import Neuron, Phenotype, Config
        ndl_config = Config('neuron_data_lifted')
        ndl_config.load_existing()
        bn_config = Config('basic-neurons')
        bn_config.load_existing()
        ndl_neurons = ndl_config.neurons()
        bn_neurons = bn_config.neurons()
        config = Config('__test_output', ttl_export_dir=tel)
        shapeshifter = Neuron(Phenotype('TEMP:soul-stealer'))
        for n in ndl_neurons:
            shapeshifter.adopt_meta(n)

        assert list(n.synonyms)
        assert list(n.definitions)
        n.write()

        assert list(shapeshifter.synonyms)
        assert list(shapeshifter.definitions)
        shapeshifter.write()

        # it eats _all_ of them
        allsyns = set(shapeshifter.synonyms)
        alldefs = set(shapeshifter.definitions)
        assert all(s in allsyns for s in n.synonyms)
        assert all(s in alldefs for s in n.definitions)

    def test_fail(self):
        from neurondm.lang import Neuron, Phenotype, Config
        bn_config = Config('basic-neurons')
        # TODO config.activate()? context manager for config ... too ...
        Neuron(Phenotype('TEMP:test'))
        try:
            bn_config.load_existing()
            raise AssertionError('Should have failed because a neuron has been created')
        except Config.ExistingNeuronsError as e:
            pass

    def test_0_equality(self):
        """ make sure that __eq__ and __hash__ are implmented correctly """
        from neurondm import Config, Neuron, Phenotype, NegPhenotype
        from neurondm import LogicalPhenotype, AND, OR, ilxtr
        from neurondm import NeuronCUT, NeuronEBM

        config = Config('test-equality', ttl_export_dir=tel, py_export_dir=pyel)

        pp = Phenotype(ilxtr.a)
        pn = NegPhenotype(ilxtr.a)
        assert pp != pn
        assert hash(pp) != hash(pn)

        assert Phenotype(ilxtr.c) == Phenotype(ilxtr.c)
        assert NegPhenotype(ilxtr.c) == NegPhenotype(ilxtr.c)
        assert hash(Phenotype(ilxtr.c)) == hash(Phenotype(ilxtr.c))
        assert hash(NegPhenotype(ilxtr.c)) == hash(NegPhenotype(ilxtr.c))

        lppo = LogicalPhenotype(OR, pp, Phenotype(ilxtr.b))
        lppa = LogicalPhenotype(AND, pp, Phenotype(ilxtr.b))
        lpno = LogicalPhenotype(OR, pn, NegPhenotype(ilxtr.b))
        assert lppo != lppa
        assert lppo != lpno
        assert lppa != lpno
        assert hash(lppo) != hash(lppa)
        assert hash(lppo) != hash(lpno)
        assert hash(lppa) != hash(lpno)

        lpe1 = LogicalPhenotype(OR, Phenotype(ilxtr.c), Phenotype(ilxtr.d))
        lpe2 = LogicalPhenotype(OR, Phenotype(ilxtr.c), Phenotype(ilxtr.d))
        assert lpe1 == lpe2
        assert hash(lpe1) == hash(lpe2)

        # make sure that self.pes equality works
        assert (pp, pn, lppo, lppa, lpno) == (pp, pn, lppo, lppa, lpno)

        npp = Neuron(pp)
        npn = Neuron(pn)
        assert npp != npn
        assert hash(npp) != hash(npn)

        nlppo = Neuron(lppo)
        nlppa = Neuron(lppa)
        nlpno = Neuron(lpno)

        assert nlppo != nlppa
        assert nlppo != nlpno
        assert nlppa != nlpno
        assert hash(nlppo) != hash(nlppa)
        assert hash(nlppo) != hash(nlpno)
        assert hash(nlppa) != hash(nlpno)

        assert Neuron(pp) == Neuron(pp)
        assert Neuron(pn) == Neuron(pn)
        assert hash(Neuron(pp)) == hash(Neuron(pp))
        assert hash(Neuron(pn)) == hash(Neuron(pn))

        assert NeuronCUT(pp) != NeuronEBM(pp)
        assert hash(NeuronCUT(pp)) != hash(NeuronEBM(pp))