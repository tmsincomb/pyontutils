from rdflib import URIRef, Literal, BNode
from pyontutils.core import qname, simpleOnt, displayGraph, flattenTriples, OntCuries, OntId, OntTerm, makeNamespaces
from pyontutils.core import oc, oc_, oop, odp, olit, oec
from pyontutils.core import restrictions, annotation, restriction, restrictionN
from pyontutils.core import NIFTTL, NIFRID, ilxtr, ilx, BFO
from pyontutils.core import definition, realizes, hasParticipant, hasPart, hasInput, hasOutput, TEMP
from pyontutils.core import partOf, hasRole, locatedIn
from pyontutils.core import hasAspectChangeCombinator, unionOf, intersectionOf, Restriction, EquivalentClass
from pyontutils.core import Restriction2, POCombinator, disjointUnionOf, oneOf
from pyontutils.core import owl, rdf, rdfs, oboInOwl
from pyontutils.methods_core import asp, tech, prot, methods_core, _t, restN, oECN

blankc = POCombinator
restHasValue = Restriction(None, owl.hasValue)
#restSomeValuesFrom = Restriction(owl.someValuesFrom)
restMinCardValue = Restriction2(rdfs.subClassOf, owl.onProperty, owl.someValuesFrom, owl.minCardinality)
restMaxCardValue = Restriction2(rdfs.subClassOf, owl.onProperty, owl.someValuesFrom, owl.maxCardinality)
restN = Restriction2(None, owl.onProperty, owl.someValuesFrom)
restrictionS = Restriction(owl.someValuesFrom)
oECU = EquivalentClass(owl.unionOf)

def t(subject, label, def_, *synonyms):
    yield from oc(subject, ilxtr.technique)
    yield from olit(subject, rdfs.label, label)
    if def_:
        yield from olit(subject, definition, def_)

    if synonyms:
        yield from olit(subject, NIFRID.synonyms, *synonyms)

class I:
    counter = iter(range(999999))
    @property
    def d(self):
        current = TEMP[str(next(self.counter))]
        self.current = current
        return current

    @property
    def b(self):
        """ blank node """
        current = next(self.counter)
        return TEMP[str(current)]

    @property
    def p(self):
        return self.current

i = I()

#from IPython import embed
#embed()

###
#   methods helper (subset of the larger ontology to speed up development)
###

filename = 'methods-helper'
prefixes = ('BFO', 'ilxtr', 'NIFRID', 'RO', 'IAO', 'definition', 'hasParticipant', 'TEMP')
prefixes += ('TEMP', 'ilxtr', 'NIFRID', 'definition', 'realizes', 'hasRole',
            'hasParticipant', 'hasPart', 'hasInput', 'hasOutput', 'BFO',
            'CHEBI', 'GO', 'SO', 'NCBITaxon', 'UBERON', 'SAO', 'BIRNLEX',
            'NLX',
)
OntCuries['HBP_MEM'] = 'http://www.hbp.FIXME.org/hbp_measurement_methods/'
#OntCuries['HBP_MEM'] = 'http://www.hbp.FIXME.org/hbp_measurement_methods/'
#imports = NIFTTL['nif_backend.ttl'],
imports = methods_core.iri,
comment = 'helper for methods development'
_repo = True
debug = True

triples = (
    (tech.injection, owl.equivalentClass, OntTerm('BIRNLEX:2135')),
          )

triples += ( # protocols
            oc(prot.CLARITY, ilxtr.protocol),
            oc(prot.deepSequencing, ilxtr.protocol),
            oc(prot.sangerSequencing, ilxtr.protocol),
            oc(prot.shotgunSequencing, ilxtr.protocol),
            oc(prot.fMRI, ilxtr.protocol),
            oc(prot.dwMRI, ilxtr.protocol),
            oc(prot.DTI, ilxtr.protocol),
           )

triples += ( # information entity

    # information entities
    oc(ilxtr.informationEntity),
    olit(ilxtr.informationEntity, rdfs.label, 'information entity'),
    olit(ilxtr.informationEntity, definition, 'Any physically encoded information.'),

    oc(ilxtr.informationArtifact, ilxtr.informationEntity),
    oc(ilxtr.informationArtifact, BFO['0000031']),
    olit(ilxtr.informationArtifact, rdfs.label, 'information artifact'),
    olit(ilxtr.informationArtifact, definition,
         ('An information entity that has an explicit symbolic encoding '
          'which is distinct from the existence or being that it encodes.')),
    (ilxtr.informationArtifact, owl.equivalentClass, OntTerm('IAO:0000030', label='information content entity')),

    oc(ilxtr.protocol, ilxtr.informationEntity),
    olit(ilxtr.protocol, rdfs.label, 'protocol'),
    olit(ilxtr.protocol, NIFRID.synonym, 'technique specification'),

    oc(ilxtr.protocolArtifact, ilxtr.informationArtifact),
    (ilxtr.protocolArtifact, rdfs.subClassOf, ilxtr.protocol),
    olit(ilxtr.protocolArtifact, rdfs.label, 'protocol artifact'),

    oc_(ilxtr.protocolExecution,
       oec(ilxtr.technique,
           *restrictions((ilxtr.isConstrainedBy, ilxtr.protocol),)),),
    olit(ilxtr.protocolExecution, rdfs.label, 'protocol execution'),

    oc(ilxtr.stereotaxiCoordinateSystem, ilxtr.informationEntity),

    # information artifacts
    oc(ilxtr.informationArtifact),  # FIXME entity vs artifact, i think clearly artifact by my def
    oc(ilxtr.image, ilxtr.informationArtifact),
    olit(ilxtr.image, rdfs.label, 'image (ilxtr)'),  # bloody iao
    olit(ilxtr.image,
         definition,
         ('A symbolic representation of some spatial or spatial-temporal '
          'aspect of a participant. Often takes the form of a 2d or 3d matrix '
          'that has some mapping to sensor space and may also be collected at '
          'multiple timepoints. Regardless of the ultimate format has some '
          'part that can be reduced to a two dimensional matrix.'  # TODO
         )),

    oc(ilxtr.photograph, ilxtr.image),
    oc(ilxtr.spatialFrequencyImageStack, ilxtr.image),

    oc(ilxtr.timeSeries, ilxtr.informationArtifact),
    olit(ilxtr.timeSeries, definition,
         'a series of numbers with a total order defined by sequential collection in time'),

    # TODO have parcellation-artifacts import methods-core?
    oc(ilxtr.parcellationArtifact, ilxtr.informationArtifact),
    oc(ilxtr.parcellationCoordinateSystem, ilxtr.parcellationArtifact),
    oc(ilxtr.parcellationCoordinateSystem, ilxtr.parcellationArtifact),
    oc(ilxtr.commonCoordinateFramework, ilxtr.parcellationCoordinateSystem),
    olit(ilxtr.commonCoordinateFramework, rdfs.label, 'common coordinate framework'),
    olit(ilxtr.commonCoordinateFramework, NIFRID.synonym, 'CCF', 'atlas coordinate framework'),
    oc(ilxtr.parcellationAtlas, ilxtr.informationArtifact),

    oc(ilxtr.axiom, ilxtr.informationEntity),
    oc(ilxtr.algorithem, ilxtr.informationEntity),
    oc(ilxtr.spikeSortingAlgorithem, ilxtr.informationEntity),
    oc(ilxtr.superResolutionAlgorithem, ilxtr.algorithem),
    oc(ilxtr.statisticalAlgorithem, ilxtr.algorithem),  # the old what counts as statistics question
    oc(ilxtr.inverseProblemAlgorithem, ilxtr.algorithem),
    oc(ilxtr.radonTransform, ilxtr.inverseProblemAlgorithem),

    oc(ilxtr.classificationCriteria, ilxtr.informationEntity),
    oc(ilxtr.identificationCriteria, ilxtr.informationEntity),

)

triples += (  # material entities

    ## material entity
    (ilxtr.materialEntity, owl.equivalentClass, BFO['0000040']),
    oc_(ilxtr.materialEntity,
        restriction(ilxtr.hasAspect, asp.livingness),
        restriction(ilxtr.hasAspect, asp['is'])),

    oc(ilxtr.compositeMaterialEntity, ilxtr.materialEntity),

    # more real than real
    oc(ilxtr.electricalField, ilxtr.materialEntity),
    oc(ilxtr.magneticField, ilxtr.materialEntity),

    #oc_(OntTerm('NCBITaxon:1', label='ncbitaxon'), restriction(ilxtr.hasAspect, asp.livingness)),
    # this is technically correct, but misleading, because rocks also have asp.livingness
    # which evaluates to false, aspects are qualities, but they are not in and of themselves meaningful
    # because I can measure the livingness of a star, or define it, basically all material entities
    # have all aspects

    oc(ilxtr.thingWithSequence, OntTerm('CHEBI:25367', term='molecule')),
    olit(ilxtr.thingWithSequence, rdfs.label, 'thing with molecular sequence'),

    oc(OntTerm('CHEBI:33696', label='nucleic acid'), ilxtr.thingWithSequence),  # FIXME should not have to put oc here, but byto[ito] becomes unhappy
    oc(ilxtr.nucleicAcid, ilxtr.materialEntity),
    (ilxtr.nucleicAcid, owl.equivalentClass, OntTerm('CHEBI:33696', label='nucleic acid')),
    oc(ilxtr.methylatedDNA, OntTerm('CHEBI:16991', term='DNA')),
    (ilxtr.DNA, owl.equivalentClass, OntTerm('CHEBI:16991', term='DNA')),
    oc(ilxtr.DNA, ilxtr.nucleicAcid),

    (ilxtr.molecule, owl.equivalentClass, OntTerm('CHEBI:25367', label='molecule')),
    oc(ilxtr.plasmidDNA, ilxtr.molecule),  # FIXME how do we model the physical manifestation of a sequence? 'SO:0000155'
    oc(ilxtr.primaryHeritableGeneticMaterial, ilxtr.molecule),
    oc(ilxtr.hybridizationProbe, ilxtr.molecule),

    # FIXME should probably be to a higher level go?
    # FIXME redundant when we import all of go
    (OntTerm('GO:0005615'), rdfs.subClassOf, OntTerm('GO:0005575', label='cellular_component')),
    (OntTerm('GO:0005622'), rdfs.subClassOf, OntTerm('GO:0005575', label='cellular_component')),
    oc(OntTerm('SAO:1813327414', label='Cell'), ilxtr.materialEntity),
    (ilxtr.cell, owl.equivalentClass, OntTerm('SAO:1813327414', label='Cell')),
    oc_(OntTerm('SAO:1813327414', label='Cell'),
        restriction(hasPart, OntTerm('GO:0005575', label='cellular_component'))),  # inputs also need to input all their parts
    oc(ilxtr.cellSoma, OntTerm('GO:0005575')),
    oc(ilxtr.synapse, OntTerm('GO:0005575')),
    oc(OntTerm('GO:0044464'), OntTerm('GO:0005575')),
    oc(OntTerm('CHEBI:33697', label='RNA'), OntTerm('CHEBI:33696', label='nucleic acid')),
    (ilxtr.RNA, owl.equivalentClass, OntTerm('CHEBI:33697', term='RNA')),
    (ilxtr.RNA, rdfs.subClassOf, ilxtr.nucleicAcid),
    #oc(ilxtr.mRNA, OntTerm('CHEBI:33697', label='RNA')),
    oc(OntTerm('SO:0000234', label='mRNA'), OntTerm('CHEBI:33697', label='RNA')),
    (ilxtr.mRNA, owl.equivalentClass, OntTerm('SO:0000234', label='mRNA')),  # FIXME role?

    (OntTerm('GO:0005575', label='cellular_component'), rdfs.subClassOf, ilxtr.physiologicalSystem),
    # FIXME owl:sameAs is NOT for generic iris >_<
    #oc(ilxtr.physiologicalSystem, ilxtr.materialEntity),
    # FIXME what about things that were synthesized entirely?
    # how about... constrainedBy _information_ derived from some organism?
    # a protein is indeed constrained by that information regardless of
    # whether it was synthesized or not...
    #oc(OntTerm('NCBITaxon:1'), ilxtr.materialEntity),  # needed to accomodate deadness?
    oc(OntTerm('NCBITaxon:1'), ilxtr.physiologicalSystem),  # needed to accomodate deadness?
    oc_(ilxtr.physiologicalSystem,
        oneOf(OntTerm('NCBITaxon:1'),
              restN(partOf, OntTerm('NCBITaxon:1')))),
        #oec(ilxtr.materialEntity,  # FIXME in vitro...
            #restN(partOf, OntTerm('NCBITaxon:1'))
           #)),

    #oc_(ilxtr.physiologicalSystemDisjointWithOrganism,
        #oec(ilxtr.physiologicalSystem)
       #),
    #(ilxtr.physiologicalSystemDisjointWithOrganism, owl.disjointWith, OntTerm('NCBITaxon:1')),
    oc(ilxtr.viralParticle, ilxtr.physiologicalSystem),

    oc(OntTerm('UBERON:0000465'), ilxtr.materialEntity),
    oc(OntTerm('UBERON:0000955'), OntTerm('UBERON:0000465')),
    oc(OntTerm('UBERON:0007798'), OntTerm('UBERON:0000465')),
    oc(OntTerm('UBERON:0001049', label='neural tube'), OntTerm('UBERON:0000465')),
    oc(OntTerm('UBERON:0000479', label='tissue'), OntTerm('UBERON:0000465')),

    oc(ilxtr.section, ilxtr.materialEntity),
    oc_(ilxtr.section,
        intersectionOf(ilxtr.partOfSomePrimaryInput,
                       restN(partOf, ilxtr.primaryInputOfThisInstanceOfTechnique), # FIXME
                       restN(ilxtr.hasAspect, asp.flatness),  # FIXME has aspect needs more love
                      )),
    oc(ilxtr.thinSection, ilxtr.section),
    oc_(ilxtr.thinSection,
        # has value 'small'
        restriction(ilxtr.hasAspect, asp.thickness)),
    oc(ilxtr.veryThinSection, ilxtr.section),
    oc(ilxtr.brainSlice, ilxtr.section),
    oc(ilxtr.acuteBrainSlice, ilxtr.physiologicalSystem),
    oc(ilxtr.food_and_water, ilxtr.materialEntity),
    oc(ilxtr.food, ilxtr.food_and_water),  # TODO edible organic matter with variable nutritional value depending on the organism
    oc(ilxtr.highFatDiet, ilxtr.food),
    oc(ilxtr.DIODiet, ilxtr.highFatDiet),
    oc(ilx['researchdiets/uris/productnumber/D12492'], ilxtr.DIODiet),

    oc(ilxtr.water, ilxtr.materialEntity),
    olit(ilxtr.water, rdfs.label, 'water (bulk)'),
    olit(ilxtr.water, definition,
         'A bulk volume of water, as opposed to molecular water.'),
    oc_(ilxtr.water,
        intersectionOf(restN(hasPart, OntTerm('CHEBI:15377', label='water')),
                       restN(hasPart, ilxtr.electrolytes),  # FIXME and other impurities...
                       restN(ilxtr.hasAspect, asp.volume),
                       restN(ilxtr.hasAspectValue, ilxtr.notBottom))),
    oc(ilxtr.electricalGround, ilxtr.materialEntity),
    oc(ilxtr.microscope, ilxtr.materialEntity),
    oc(ilxtr.lightMicroscope, ilxtr.microscope),
    (ilxtr.lightMicroscope, owl.equivalentClass, OntTerm('BIRNLEX:2112', label='Optical microscope')),
    oc(OntTerm('BIRNLEX:2041', label='Electron microscope', synonyms=[]), ilxtr.microscope),
    (OntTerm('BIRNLEX:2029', label='Confocal microscope'), rdfs.subClassOf, ilxtr.lightMicroscope),
    oc(ilxtr.DICmicroscope, ilxtr.lightMicroscope),
    oc(ilxtr.microtome, ilxtr.materialEntity),
    oc(ilxtr.serialBlockfaceMicrotome, ilxtr.microtome),
    oc(ilxtr.ultramicrotome, ilxtr.microtome),
    oc(ilxtr.serialBlockfaceUltraMicrotome, ilxtr.ultramicrotome),
    oc(ilxtr.stereotax, ilxtr.materialEntity),
    oc(ilxtr.centrifuge, ilxtr.materialEntity),
    oc(ilxtr.ultracentrifuge, ilxtr.centrifuge),
    oc(ilxtr.cuttingTool, ilxtr.materialEntity),
    oc(ilxtr.IRCamera, ilxtr.materialEntity),
    oc(ilxtr.recordingElectrode, ilxtr.materialEntity),
    oc(ilxtr.singleElectrode, ilxtr.recordingElectrode),
    oc(ilxtr.multiElectrode, ilxtr.recordingElectrode),
    oc(ilxtr.laminarProbe, ilxtr.multiElectrode),
    oc(ilxtr.multiElectrodeArray, ilxtr.multiElectrode),
    oc(ilxtr.ephysRig, ilxtr.materialEntity), 
    oc(ilxtr.inVitroEphysRig, ilxtr.ephysRig), 

    oc(ilxtr.microPipette, ilxtr.materialEntity),
    oc(ilxtr.patchPipette, ilxtr.microPipette),

    oc(ilxtr.patchElectrode, ilxtr.recordingElectrode),
    (ilxtr.patchElectrode, hasPart, ilxtr.singleElectrode),
    (ilxtr.patchElectrode, hasPart, ilxtr.patchPipette),

    oc(ilxtr.sharpMicroPipette, ilxtr.microPipette),
    oc(ilxtr.sharpElectrode, ilxtr.recordingElectrode),
    (ilxtr.sharpElectrode, hasPart, ilxtr.singleElectrode),
    (ilxtr.sharpElectrode, hasPart, ilxtr.sharpMicroPipette),

    oc(ilxtr.contrastAgen, ilxtr.materialEntity),

    oc(ilxtr.inductionFactor, ilxtr.materialEntity),

    oc(ilxtr.bathSolution, ilxtr.materialEntity),

    oc(ilxtr.photons, ilxtr.materialEntity),
    oc_(ilxtr.photons,
        disjointUnionOf(ilxtr.radiowaves,
                        ilxtr.microwaves,
                        ilxtr.infaredLight,
                        ilxtr.visibleLight,
                        ilxtr.ultravioletLight,
                        ilxtr.xrays,
                        ilxtr.gammarays)
       ),
    oc(ilxtr.radiowaves, ilxtr.photons),
    oc(ilxtr.microwaves, ilxtr.photons),
    oc(ilxtr.infaredLight, ilxtr.photons),
    oc(ilxtr.visibleLight, ilxtr.photons),
    oc(ilxtr.ultravioletLight, ilxtr.photons),
    oc(ilxtr.xrays, ilxtr.photons),
    oc(ilxtr.gammarays, ilxtr.photons),
    #oc(ilxtr.infaredLight, ilxtr.photons),
    #oc(ilxtr.visibleLight, ilxtr.photons),
    #oc(ilxtr.xrays, ilxtr.photons),
    (ilxtr.positron, owl.equivalentClass, OntTerm('CHEBI:30225')),

    oc(ilxtr.tissue, ilxtr.materialEntity),
    oc(ilxtr.axon, ilxtr.materialEntity),
    oc(ilxtr.cellMembrane, ilxtr.materialEntity),
    oc(ilxtr.building, ilxtr.materialEntity),
    oc(ilxtr.electrolytes, ilxtr.materialEntity),

    oc(ilxtr.contrastAgent, ilxtr.materialEntity),
    oc_(ilxtr.contrastAgent, restriction(ilxtr.hasAspect, asp.contrast)),
    oc(ilxtr.detectedPhenomena, ilxtr.materialEntity),  # ie a phenomena that we know how to detect

)

triples += (  # changes
    oc(ilxtr.positive, ilxtr.changeType),
    oc(ilxtr.negative, ilxtr.changeType),
    (ilxtr.negative, owl.disjointWith, ilxtr.positive),
    oc(ilxtr.nonZero, ilxtr.changeType),
    oc(ilxtr.zero, ilxtr.changeType),
    (ilxtr.zero, owl.disjointWith, ilxtr.nonZero),
)

triples += (  # aspects

    # aspect value

    oc(ilxtr.aspectBottom),  # TODO disjointness etc.
    olit(ilxtr.aspectBottom, rdfs.label, 'aspect bottom'),
    olit(ilxtr.aspectBottom, definition,
         ('The result of attempting to measurement or actualize '
          'an aspect bound to a being for which the operational '
          'definition of the aspect makes it impossible to evaluate '
          '(as in function evaluation). For examples '
          '(*: angles-on-head-of-pin count) -> aspectBottom '
          'or even (: angels-on-head-of-pin count) -> aspectBottom '
          'since one cannot even bind the notion of numbers to the '
          'non-being much less actually attempt to make such a measurement.')),

    # isness
    oc(asp['is'], asp.Local),
    olit(asp['is'], rdfs.label, 'is'),
    olit(asp['is'], NIFRID.synonym,
         'isness',
         'being aspect',
         'beingness',),
    olit(asp['is'], definition,
         ('The aspect of beingness. Should be true or false, value in {0,1}.'
          "Not to be confused with the 'is a' reltionship which deals with categories/types/classes."
          "For now should not be used for 'partial' beingness, so a partially completed building is not"
          'a building for the purposes of this aspect. This is open to discussion, and if there are'
          'good examples where partial beingness is a useful concept, use as a [0,1] aspect would be '
          'encouraged.')),
    olit(asp['is'], rdfs.comment,
         ('There are cases where the value could be ? depending on how one '
          'operationalizes certain concepts from quantum physics. Note also that '
          'isness will be directly affected by the choice of the operational defintion. '
          'Because of the scope of this ontology, there are implicit decisions about the nature '
          'of certain operational definitions, such as livingness, which imply that our '
          'operational definition for isness is invariant to dead.'
         )),

    oc(asp.amount, asp['is']),  # this implies that asp.mass is asp.is
    oc(asp['count'], asp.amount),
    # instantaneous vs over a time interval
    # interestingly if you ignore time then the idea of
    # 'counting' similar events is entirely consistent
    # so hasPrimaryAspect_dAdT xsd.NonNegativeInteger
    # is valid

    # location/allocation
    # NOTE allocation is an aspect, location is NOT an aspect
    # allocation is an aspect of a composite being where the
    # location of each of its parts can be considered to be
    # something directly measurable about the composite being
    # for example a pile of sand or a set of grains of sand
    # can have an allocation based only by counting the members
    oc(asp.spatial, asp.nonLocal),
    oc(asp.location, asp.spatial),
    # you cannot measure the location of something
    # you can only measure the location of something relative to something else
    # our model assumes that there is no privilidged reference frame in this universe
    oc(asp.direction, asp.spatial),
    oc(asp.locationInAtlas, asp.location),
    oc_(asp.locationInAtlas, restN(ilxtr.hasContext, ilxtr.atlasLandmarks)),  # morphology matching atlas?

    oc(asp.name, asp.nonLocal),
    oc(asp.identity, asp.Local),
    (asp.name, ilxtr.hasLocalEquivalent, asp.identity),

    oc(asp.category, asp.Local),
    oc(asp.categoryAssigned, asp.nonLocal),
    (asp.categoryAssigned, ilxtr.hasLocalEquivalent, asp.category),

    oc(asp.allocation, asp.location),  # FIXME not clear whether this is local or nonlocal
    olit(asp.allocation, definition,
         ('Allocation is the amount of something in a given place '
          'rather than the total universal amount of a thing. '
          'For example if I move 100 grains of salt from a container '
          'to a scale, I have changed the allocation of the salt (solid). '
          'If I dissolve the salt in water then I have negatively impacted '
          'the amount of total salt (solid) in the universe since that salt '
          'is now ionized in solution.')),

    oc(asp.proportion, asp.allocation),

    #oc(asp.isClassifiedAs, asp['is']),  # FIXME not quite right, renaming is different then identity
    # this is only an isness in the case where there are a finite and fixed number of types
    #olit(asp.isClassifiedAs, rdfs.label, 'is classified as'),
    #olit(asp.isClassifiedAs, NIFRID.synonym,
         #'is named as', 'has operational definition with inclusion criteria that names thing as'),

    oc(asp.flatness, asp.Local),
    olit(asp.flatness, rdfs.label, 'flatness'),
    olit(asp.flatness, NIFRID.synonym, 'flatness aspect'),
    olit(asp.flatness, definition,
         ('How flat a thing is. There are a huge variety of operational '
          'definitions depending on the type of thing in question.')),

    oc(asp.weight, asp.nonLocal),  # TODO 'PATO:0000128'
    olit(asp.weight, rdfs.label, 'weight'),
    olit(asp.weight, NIFRID.synonym, 'weight aspect'),

    oc(asp.livingness, asp.Local),
    oc(asp.aliveness, asp.Local),  # PATO:0001421
    oc(asp.deadness, asp.Local),  # PATO:0001422
    (asp.aliveness, owl.disjointWith, asp.deadness),  # this holds for any single operational definition
    #((hasAspect some livingness) and (hasAspectValue value true)) DisjointWith: ((hasAspect some livingness) and (hasAspectValue value false))

    # functional/stateful (the conflation here is amusing)
    oc(asp.boundFunctionalAspect, asp.nonLocal),
    olit(asp.boundFunctionalAspect, rdfs.label, 'bound functional aspect'),
    # TODO
    # the 'functionality' of the aspect is going to be qualified by the
    # subject to which it is bound...
    # this is equivalentClass intersectionOf material entity 
    # restriction
    # onProperty isFunctional
    # has qualified role?
    # 
    oc(asp.behavioral, asp.Local),

    oc(asp.physiological, asp.Local),  # FIXME vs ilxtr.physiologicalSystem?

    oc(asp.sequence, asp.Local),
    #(OntTerm('SO:0000001', label='region', synonyms=['sequence']), rdfs.subClassOf, asp.sequence), this very much does not work...

    oc(asp.sensory, asp.Local),
    oc(asp.vision, asp.sensory),  # FIXME asp.canSee

    oc(asp.anySpatioTemporalMeasure, ilxtr.aspect),  # FIXME
    oc(asp.electromagnetic, ilxtr.aspect),
    oc(asp.electrical, asp.electromagnetic),
    oc(asp.voltage, asp.electrical),
    oc(asp.voltage, asp.nonLocal),
    oc_(asp.voltage, restriction(ilxtr.hasContext, ilxtr.electricalGround)),
    oc(asp.current, asp.electrical),
    oc(asp.current, asp.nonLocal),
    oc(asp.charge, asp.electrical),
    oc(asp.resistance, asp.electrical),
    oc(asp.resistance, asp.Local),
    oc(asp.magnetic, asp.electromagnetic),
    olit(asp.magnetic, rdfs.label, 'magnetic (ilxtr)'),

    oc(asp.mass, asp.Local),
    olit(asp.mass, rdfs.label, 'mass'),
    olit(asp.mass, NIFRID.synonym, 'rest mass'),
    oc(asp.massRelitavisitc, asp.nonLocal),
    oc(asp.energy, asp.nonLocal),
    oc(asp.velocity, asp.nonLocal),
    oc(asp.momentum, asp.nonLocal),
    oc(asp.acceleration, asp.nonLocal),
    oc(asp.force, asp.nonLocal),

    oc(asp.informationEntropy, asp.Local),
    oc(asp.mechanicalRigidity, asp.Local),
    oc(asp.spectrum, asp.Local),
    oc(asp.spontaneousChangeInStructure, asp.Local),
    oc(asp.connectivity, asp.Local),
    oc(asp.physicalOrderedness, asp.Local),
    oc(asp.latticePeriodicity, asp.physicalOrderedness),  # physical order

    #oc(asp.functional, ilxtr.aspect),  # asp.functional is not the right way to model this
    #olit(ilxtr.functionalAspectRole, definition,
         #('A functional aspect is any aspect that can be used to define ')),
    oc(asp.biologicalActivity, asp.Local),  # TODO very broad from enyme activity to calories burned
    #oc(asp.circadianPhase, asp.biologicalActivity),
    oc(asp.circadianPhase, asp.Local),  # FIXME hrm... time as a proxy for biological state?

    oc(asp.sensitvity, asp.nonLocal),
    # FIXME issue with sensitivity and the 'towards' relation

    #oc(asp.functionalDefinition, asp['is']),  # TODO not quite right?
    oc(asp.functionalDefinition, asp.nonLocal),
    oc(asp.permeability, asp.functionalDefinition),  # changes some functional property so is thus an isness?

    oc(asp.contrast, asp.nonLocal),  # TODO what is this more specifically? this is derived ...
    # contrast is always qualified by some detecting phenomena
    oc_(asp.contrast, restN(ilxtr.hasContext, ilxtr.detectedPhenomena)),

    oc(asp.density, asp.Local),  # not directly measurable

    oc(asp.direct, asp.Local),
    olit(asp.direct, definition,
         'An aspect that can be measured directly in a single instant in time. '
         'Note that these are in principle direct, the operational definition '
         'may mean that in reality they were not measured directly.'
         'Anything with time units is not direct. '
         'In theory a count/amount of a complex entity can be direct. Whether it '
         'is possible in reality to actually accomplish such a thing is another '
         'question altogether.'),

    # FIXME need a better way to model the 'in principle direct'
    # or more accurately 'can never be measured directly'
    oc(asp.mass, asp.direct),
    oc(asp['count'], asp.direct),
    oc(asp.volume, asp.direct),  # NOTE these are all _rest_ values ignoring relativity
    oc(asp.length, asp.direct),  # distance is the non-direct version of
    oc(asp.distance, asp.nonLocal),
    oc(asp.distanceFromSoma, asp.distance),
    oc_(asp.distanceFromSoma, restriction(ilxtr.hasContext, ilxtr.cellSoma)),

    # all of these are questionable because they depend on some
    # measurement process which has a tau
    oc(asp.temperature, asp.Local),

    oc(asp.boilingPoint, asp.nonLocal),  # tripple point!
    oc_(asp.boilingPoint, restN(ilxtr.hasContextAspect, asp.pressure)),
    #oc_(asp.boilingPoint, restN(ilxtr.hasContext, asp.pressure)) FIXME

    oc(asp.epitopePresent, asp.Local),  # true predicates are always local by definition
    oc(asp.condensationPoint, asp.nonLocal),

    oc(asp.lumenance, asp.Local),

    oc(asp.shape, asp.Local),
    # TODO also need the constants...

)

methods_helper = simpleOnt(filename=filename,
                         prefixes=prefixes,
                         imports=imports,
                         triples=triples,
                         comment=comment,
                         _repo=_repo)

methods_helper._graph.add_namespace('asp', str(asp))
methods_helper._graph.add_namespace('ilxtr', str(ilxtr))  # FIXME why is this now showing up...
methods_helper._graph.add_namespace('prot', str(prot))
methods_helper._graph.add_namespace('tech', str(tech))
methods_helper._graph.add_namespace('HBP_MEM', OntCuries['HBP_MEM'])
methods_helper._graph.write()  # note to self, simpleOnt calls write as well

###
#   Methods
###

filename = 'methods'
prefixes = ('TEMP', 'ilxtr', 'NIFRID', 'definition', 'realizes', 'hasRole',
            'hasParticipant', 'hasPart', 'hasInput', 'hasOutput', 'BFO',
            'CHEBI', 'GO', 'SO', 'NCBITaxon', 'UBERON', 'SAO', 'BIRNLEX',
            'NLX',
)
OntCuries['HBP_MEM'] = 'http://www.hbp.FIXME.org/hbp_measurement_methods/'
imports = methods_core.iri, methods_helper.iri, NIFTTL['bridge/chebi-bridge.ttl'], NIFTTL['bridge/tax-bridge.ttl']
#imports = methods_core.iri, methods_helper.iri
comment = 'The ontology of techniques and methods.'
_repo = True
debug = False

triples = (
    # biccn

    (ilxtr.hasSomething, owl.inverseOf, ilxtr.isSomething),

    _t(i.d, 'atlas registration technique',
       # ilxtr.hasPrimaryParticipant, restriction(partOf, some animalia)
       # TODO this falls into an extrinsic classification technique...
       # or a context classification/naming technique...
       (ilxtr.isConstrainedBy, ilxtr.parcellationArtifact),
       #(ilxtr.assigns, asp.location),  # FIXME ilxtr.assigns needs to imply naming...
       #(ilxtr.asserts, asp.location),  # FIXME ilxtr.asserts needs to imply naming...
       (ilxtr.hasPrimaryAspect, asp.locationInAtlas),
       # (ilxtr.hasPrimaryAspect, asp.location),
       synonyms=('registration technique',
                 'atlas registration',
                 'registration')),

    # 'spatial transcriptomics'

    # 'anatomy registration'
    # feducial points
    # '3d atlas registration'
    # '2d atlas registration'
    # 'image registration'
    # fresh frozen ventricles are smaller
    # 4% pfa non perfused

    # 'ROI based atlas registration technique'

    # biccn
    oc(ilxtr.analysisRole, OntTerm('BFO:0000023', label='role')
    ),

    _t(i.d, 'randomization technique',  # FIXME this is not defined correctly
       (ilxtr.hasPrimaryAspect, asp.informationEntropy),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.positive),
    ),

    # FIXME see if we really want these?
    _t(i.d, 'techniques classified by inputs',
       (hasInput, ilxtr.materialEntity)),

    _t(i.d, 'techniques classified by aspects',
       (ilxtr.processHasAspect, ilxtr.aspect)),

    _t(i.d, 'techniques classified by primary aspects',
       (ilxtr.hasPrimaryAspect, ilxtr.aspect)),

    _t(i.d, 'techniques classified by constraining aspects',
       (ilxtr.hasConstrainingAspect, ilxtr.aspect),
       synonyms=('has constraining aspect',
                 'technique defined by constraint')),

    _t(i.d, 'composite techniques',
       (hasPart, ilxtr.technique)),

    _t(i.d, 'chemical technique',  # FIXME but not molecular? or are molecular subset?
       (hasParticipant,  # FIXME hasParticipant is incorrect? too broad?
        OntTerm('CHEBI:24431', label='chemical entity')
       ),),

    _t(i.d, 'molecular technique',  # FIXME help I have no idea how to model this same with chemical technique
       # TODO FIXME I think it is clear that there are certain techniques which are
       # named in a way that is assertional, not definitional
       # it seems appropriate for those arbitrarily named techniques to use subClassOf?
       (hasInput,
        OntTerm('CHEBI:25367', label='molecule')
       ),),

    _t(i.d, 'cellular technique',
       intersectionOf(ilxtr.technique,
                      restN(hasInput, OntTerm('SAO:1813327414', label='Cell'))),
       intersectionOf(ilxtr.technique,
                      restN(hasInput,
                            restN(partOf,
                                  OntTerm('SAO:1813327414', label='Cell')))),
       # indeed the equivalence of these two statements is factually correct
       # if I have a technique that inputs something, it also inputs all of the parts of it
       # including the ones that we have named
       equivalentClass=oECN),

    _t(i.d, 'cell type induction technique',
       (ilxtr.hasPrimaryInput, OntTerm('SAO:1813327414', label='Cell')),
       (hasInput, ilxtr.inductionFactor),
    ),

    _t(i.d, 'molecular cloning technique',

       (ilxtr.hasPrimaryInput,
        OntTerm('CHEBI:33696', label='nucleic acid')
        #OntTerm('CHEBI:16991', label='deoxyribonucleic acid')
        # FIXME other options are OntTerm('SAO:454034570') or OntTerm('SO:0000352')
        ),
       # the objective is to isolate a _specific_ sequence of DNA/RNA
       # amplification is the next step
       (ilxtr.hasPrimaryAspect, asp['count']),  # the general objective being to increase the DNA
       synonyms=('cloning technique', 'molecular cloning')
    ),

    _t(i.d, 'microarray technique',
       (hasInput,
        # TODO leverage EFO here
        # OntTerm(search='microarray', limit=20, prefix='NIFSTD')  # nice trick
        OntTerm('BIRNLEX:11031', label='Microarray platform')
        ),
    ),

    # sequencing TODO

    _t(tech.sequencing, 'sequencing technique',
       intersectionOf(ilxtr.technique,
                      restrictionN(ilxtr.knownDetectedPhenomena, ilxtr.thingWithSequence),
                      restrictionN(ilxtr.hasPrimaryAspect, asp.sequence,),
                      restrictionN(ilxtr.hasInformationOutput, ilxtr.informationArtifact)),
       intersectionOf(ilxtr.technique,
                      restrictionN(hasPart, tech.sequencing)),
       equivalentClass=oECN),


    _t(tech._naSeq, 'nucleic acid sequencing technique',
       intersectionOf(ilxtr.technique,
                      restrictionN(ilxtr.knownDetectedPhenomena,
                        # hasParticipant molecule or chemical?
                        #OntTerm(term='nucleic acid')
                                   OntTerm('CHEBI:33696', label='nucleic acid')),
                      restrictionN(ilxtr.hasPrimaryAspect,
                                   #OntTerm(term='sequence')
                                   #OntTerm('SO:0000001', label='region', synonyms=['sequence'])  # label='region'
                                   asp.sequence,  # pretty sure that SO:0000001 is not really an aspect...
       ),
                      restrictionN(ilxtr.hasInformationOutput,
                                   ilxtr.informationArtifact),  # note use of artifact
       ),
       intersectionOf(ilxtr.technique,
                      restrictionN(hasPart, tech._naSeq)),
       equivalentClass=oECN),

    _t(i.d, 'deep sequencing technique',
       (hasPart, tech._naSeq),
       (ilxtr.isConstrainedBy, prot.deepSequencing),  # FIXME circular
       synonyms=('deep sequencing',)
    ),

    _t(i.d, 'sanger sequencing technique',
       (hasPart, tech._naSeq),
       (ilxtr.isConstrainedBy, prot.sangerSequencing),
       # we want these to differentiate based on the nature of the technqiue
       synonyms=('sanger sequencing',)
    ),

    _t(i.d, 'shotgun sequencing technique',
       (hasPart, tech._naSeq),
       (ilxtr.isConstrainedBy, prot.shotgunSequencing),
       synonyms=('shotgun sequencing',)
    ),

    _t(tech.scSeq, 'single cell sequencing technique',
       # FIXME vs pp -> *NA from a single cell
       #ilxtr.technique,
       (hasPart, tech.sequencing),
       #(hasInput, OntTerm('CHEBI:33696', label='nucleic acid')),  # not much protein in a single cell
       # hasInput o hasPart some owl:Thing TODO
       #(hasInput, OntTerm('SAO:1813327414', label='Cell')),  # inputs also need to input all their parts
       # this will continue to work if we use hasPart NucleicAcidExtractionIsolationTechnique
       # (ilxtr.hasPrimaryParticipantCardinality, 1)  # FIXME need this...
       #restMaxCardValue(),
        restMaxCardValue(ilxtr.hasPrimaryInput, OntTerm('SAO:1813327414', label='Cell'), Literal(1)),
       #(ilxtr.hasInformationOutput, ilxtr.informationArtifact),  # note use of artifact
       synonyms=('single cell sequencing',)
    ),

    _t(tech.snSeq, 'single nucleus sequencing technique',
       (hasPart, tech.sequencing),
       #(hasInput, OntTerm('CHEBI:33696', label='nucleic acid')),  # not much protein in the nucleus...
       #(ilxtr.hasPrimaryInput, OntTerm('GO:0005634', label='nucleus')),
        restMaxCardValue(ilxtr.hasPrimaryInput, OntTerm('GO:0005634', label='nucleus'), Literal(1)),
       # or rather does NOT have input some CytoPlasm
       # (ilxtr.hasPrimaryParticipantCardinality, 1)  # FIXME need this...
       synonyms=('single nucleus sequencing',)
    ),
    (tech.snSeq, owl.disjointWith, tech.scSeq),

    _t(tech.rnaSeq, 'RNAseq',
       intersectionOf(
       ilxtr.technique,
       restrictionN(ilxtr.knownDetectedPhenomena, OntTerm('CHEBI:33697', label='RNA')),
       restrictionN(ilxtr.hasPrimaryAspect, asp.sequence,),
       restrictionN(ilxtr.hasInformationOutput, ilxtr.informationArtifact)),
       intersectionOf(ilxtr.technique,
                      restrictionN(hasPart, tech.rnaSeq)),
       synonyms=('RNA-seq',),
       equivalentClass=oECN),

    # Split-seq single cell single nuclei
    # SPLiT-seq

    _t(i.d, 'mRNA-seq',
       (hasPart, tech.rnaSeq),
       (ilxtr.knownDetectedPhenomena, OntTerm('SO:0000234')
       #(ilxtr.hasPrimaryInput, ilxtr.mRNA
        #OntTerm(term='mRNA')
        # FIXME wow... needed a rerun on this fellow OntTerm('SAO:116515730', label='MRNA', synonyms=[])
       ),
       #(ilxtr.hasPrimaryAspect, asp.sequence),
       #(ilxtr.hasInformationOutput, ilxtr.informationArtifact),  # note use of artifact
    ),

    _t(i.d, 'snRNAseq',
       #(ilxtr.hasPrimaryParticipant, OntTerm('CHEBI:33697', label='RNA')),
       (hasPart, tech.rnaSeq),
       #(hasParticipant, OntTerm('GO:0005634', label='nucleus')),
        restMaxCardValue(ilxtr.hasPrimaryInput, OntTerm('GO:0005634', label='nucleus'), Literal(1)),
       synonyms=('snRNA-Seq',
                 'single nucleus RNAseq',)),

    _t(i.d, 'scRNAseq',
       #(ilxtr.hasPrimaryParticipant, OntTerm('CHEBI:33697', label='RNA')),
       (hasPart, tech.rnaSeq),
       #(ilxtr.hasPrimaryInput, OntTerm('SAO:1813327414', label='Cell')),
        restMaxCardValue(ilxtr.hasPrimaryInput, OntTerm('SAO:1813327414', label='Cell'), Literal(1)),
       synonyms=('scRNA-Seq',
                 'scRNA-seq',
                 'single cell RNAseq',)),
        # 'deep-dive scRNA-Seq'  # deep-dive vs wide-shallow I think is what this is


    _t(i.d, 'Patch-seq',
       (hasPart, tech.rnaSeq),
       (ilxtr.knownDetectedPhenomena, OntTerm('CHEBI:33697', label='RNA')),
       (hasParticipant, ilxtr.microPipette),  # FIXME TODO
       synonyms=('Patch-Seq',
                 'patch seq',)),

    _t(tech.mcSeq, 'mC-seq',
       #(ilxtr.hasPrimaryInput, ilxtr.openChromatin),  # nucleus has part?
       #(ilxtr.hasPrimaryInput, ilxtr.methylatedDNA),
       (ilxtr.hasPrimaryAspect, asp.sequence),
       (ilxtr.knownDetectedPhenomena, ilxtr.DNA),
       (ilxtr.knownDetectedPhenomena, OntTerm('GO:0010424', label='DNA methylation on cytosine within a CG sequence')),
       (ilxtr.hasInformationOutput, ilxtr.informationArtifact),  # note use of artifact
       def_='non CG methylation',
    ),

    _t(i.d, 'snmC-seq',
       (hasPart, tech.mcSeq),
       #(ilxtr.hasPrimaryInput, OntTerm('GO:0005634', label='nucleus')),
        restMaxCardValue(ilxtr.hasPrimaryInput, OntTerm('GO:0005634', label='nucleus'), Literal(1)),
       synonyms=('snmC-Seq',)),

    # mCH

    _t(tech.ATACseq, 'ATAC-seq',
       (ilxtr.hasSomething, i.d),
       (hasPart, tech.sequencing),  # TODO
       #(ilxtr.hasInformationOutput, ilxtr.informationArtifact),  # note use of artifact
    ),

    _t(i.d, 'snATAC-seq',
       (hasPart, tech.ATACseq),
       #(ilxtr.hasPrimaryInput, OntTerm('GO:0005634', label='nucleus')),
        restMaxCardValue(ilxtr.hasPrimaryInput, OntTerm('GO:0005634', label='nucleus'), Literal(1)),
       synonyms=('single-nucleus ATAC-seq',
                 'single nucleus ATAC-seq',)),

    _t(i.d, 'scATAC-seq',
       (hasPart, tech.ATACseq),
       #(ilxtr.hasPrimaryInput, OntTerm('SAO:1813327414', label='Cell')),
        restMaxCardValue(ilxtr.hasPrimaryInput, OntTerm('SAO:1813327414', label='Cell'), Literal(1)),
       def_='enriched for open chromatin',
       synonyms=('single-cell ATAC-seq',
                 'single cell ATAC-seq',)),

    _t(i.d, 'Bulk-ATAC-seq',
       (hasPart, tech.ATACseq),
       (ilxtr.hasSomething, i.d),
    ),

    #'scranseq'  # IS THIS FOR REAL!?
    #'ssranseq'  # oh boy, this is just me being bad at spelling scrnaseq?

    _t(i.d, 'Drop-seq',
       (ilxtr.hasSomething, i.d),
       (hasPart, tech.rnaSeq),  # TODO
       #(ilxtr.hasInformationOutput, ilxtr.informationArtifact),  # note use of artifact
       synonyms=('droplet sequencing',
                 'Droplet-Sequencing')
    ),

    _t(i.d, 'DroNc-seq',
       (ilxtr.hasSomething, i.d),
       (hasPart, tech.rnaSeq),  # TODO
      ),

    _t(i.d, '10x Genomics sequencing',
       (ilxtr.hasSomething, i.d),
       (hasPart, tech.rnaSeq),  # TODO
       #(ilxtr.hasInformationOutput, ilxtr.informationArtifact),  # note use of artifact
       def_='commercialized drop seq',
       # snRNA-seq 10x Genomics Chromium v2
       # 10x Genomics Chromium V2 scRNA-seq
       # 10X (sigh)
       synonyms=('10x Genomics', '10x sequencing', '10x',)),

    _t(i.d, 'MAP seq',
       (ilxtr.hasSomething, i.d),
       (hasPart, tech.sequencing),
       #(ilxtr.hasInformationOutput, ilxtr.informationArtifact),  # note use of artifact
       synonyms=('MAPseq',
                 'Multiplexed Analysis of Projections by Sequencing',)),

    _t(i.d, 'SMART-seq',
       (hasPart, tech.rnaSeq),
       (hasInput, ilxtr.SMARTSeqKit),
       (ilxtr.isConstrainedBy, prot.SMARTSeq),
       # Clontech / Takara
       synonyms=('Switching Mechanism at 5\' End of RNA Template sequencing',
                 'Smart-seq2',
                 'SMART-seq',
                 'SMART-Seq v4',
                 'SMART-seq v4',)),

    # 'deep smart seq',

    _t(tech.anestheticAdministration, 'anesthetic adminstration technique',
       # TODO delivered to partOf primaryparticipant
       # parent partof primary participant deliver or something
      (ilxtr.hasPrimaryParticipant, OntTerm('CHEBI:38867', label='anaesthetic')),),

    _t(i.d, 'anaesthesia technique',
       # anaesthesia is an excellent example of a case where
       # just the use of an anaesthetic is not sufficient
       # and should not be part of the definition
       #(ilxtr.hasPrimaryParticipant,
        #oc_(restriction(partOf, OntTerm('UBERON:0001016', label='nervous system')))),
       #(hasParticipant, ilxtr.anesthetic),  # FIXME has role?
       (ilxtr.hasPrimaryAspect, asp.nervousResponsiveness),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.negative),
       (hasPart, tech.anestheticAdministration),
       (hasParticipant, OntTerm('NCBITaxon:33208', label='Metazoa')),
    ),
    # local anaesthesia technique
    # global anaesthesia technique

    _t(tech.ISH, 'in situ hybridization technique',  # TODO
       intersectionOf(tech.inSitu,  # FIXME
                      restN(hasInput, ilxtr.hybridizationProbe),
                      restN(ilxtr.knownDetectedPhenomena, ilxtr.RNA)),
       restN(hasPart, tech.ISH),
       synonyms=('in situ hybridization', 'ISH'),
       equivalentClass=oECN),
    #(tech.ISH, owl.equivalentClass, OntTerm('NLXINV:20090610')),  # TODO

    _t(tech.FISH, 'fluorescence in situ hybridization technique',
       (ilxtr.hasSomething, i.d),
       (hasPart, tech.ISH),
       (ilxtr.knownDetectedPhenomena, ilxtr.RNA),
       synonyms=('fluorescence in situ hybridization', 'FISH'),
    ),

    _t(tech.smFISH, 'single-molecule fluorescence in situ hybridization technique',
       (ilxtr.hasSomething, i.d),
       (hasPart, tech.ISH),
       (ilxtr.knownDetectedPhenomena, ilxtr.RNA),
       synonyms=('single-molecule fluorescence in situ hybridization',
                 'single molecule fluorescence in situ hybridization',
                 'single-molecule FISH',
                 'single molecule FISH',
                 'smFISH'),
    ),

    _t(tech.MERFISH, 'multiplexed error-robust fluorescence in situ hybridization technique',
       (ilxtr.hasSomething, i.d),
       (hasPart, tech.ISH),
       (ilxtr.knownDetectedPhenomena, ilxtr.RNA),
       synonyms=('multiplexed error-robust fluorescence in situ hybridization',
                 'multiplexed error robust fluorescence in situ hybridization',
                 'multiplexed error-robust FISH',
                 'multiplexed error robust FISH',
                 'MERFISH'),
    ),

    _t(i.d, 'genetic technique',
       (hasParticipant,
        # the participant is really some DNA that corresponds to a gene
        OntTerm('SO:0000704', label='gene')  # prefer SO for this case?
        #OntTerm(term='gene', prefix='obo')  # representing a gene
        ),
       # FIXME OR has participant some nucleic acid...
    ),

    _t(tech.enrichment, 'enrichment technique',
       #(ilxtr.hasSomething, i.d),
       (ilxtr.hasPrimaryAspect, asp.proportion),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.positive),
       def_='increase proporation',  # the count stays the same
       # this is a purification technique
       # amplification is a creating technique
    ),

    _t(tech.amplification, 'amplification technique',
       (ilxtr.hasPrimaryAspect, asp['count']),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.positive),
       def_='increase number',
    ),

    _t(i.d, 'nucleic acid amplification technique',
       (ilxtr.hasPrimaryParticipant, OntTerm('CHEBI:33696', label='nucleic acid')),
       (ilxtr.hasPrimaryAspect, asp['count']),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.positive),
      ),
    _t(i.d, 'expression manipulation technique',
       (ilxtr.hasSomething, i.d)),
    _t(i.d, 'conditional expression manipulation technique',
       (ilxtr.hasSomething, i.d)),

    _t(i.d, 'knock in technique',
       (ilxtr.hasSomething, i.b),
    ),
    (i.p, ilxtr.hasTempId, OntTerm('HBP_MEM:0000121')),

    _t(i.d, 'knock down technique',
       (ilxtr.hasSomething, i.d),
       synonyms=('underexpression technique',),
    ),

    # endogenous genetic manipulation   HRM 'HBP_MEM:0000119'
    # conditional knockout 'HBP_MEM:0000122'
    # morpholino 'HBP_MEM:0000124'
    # RNA interference 'HBP_MEM:0000123'
    # dominant-negative inhibition   sigh 'HBP_MEM:0000125'

    _t(i.d, 'knock out technique',
       (ilxtr.hasSomething, i.b),
    ),
    (i.p, ilxtr.hasTempId, OntTerm('HBP_MEM:0000120')),

    _t(i.d, 'mutagenesis technique',
       (ilxtr.hasSomething, i.d)
    ),

    _t(i.d, 'overexpression technique',
       (ilxtr.hasSomething, i.d)
    ),

    _t(tech.delivery, 'delivery technique',
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),  # email delivery? fun...
       (ilxtr.hasPrimaryAspectActualized, asp.location),
       #(ilxtr.hasSomething, i.d),
       def_='A technique for moving something from point a to point b.',),

    _t(i.d, 'physical delivery technique',
       # i.e. distinct from energy released by chemical means?
       # gravity not ATP hydrolysis?
       (ilxtr.hasPrimaryAspectActualized, asp.location),
       # FIXME
       (ilxtr.hasMotiveForce, ilxtr.physical)),

    _t(i.d, 'diffusion based delivery technique',
       (ilxtr.hasPrimaryAspectActualized, asp.location),
       # FIXME
       (ilxtr.hasMotiveForce, ilxtr.brownianMotion)),

    _t(i.d, 'bath application technique',
       (ilxtr.hasPrimaryAspectActualized, asp.location),
       # FIXME
       (hasParticipant, ilxtr.bathSolution)),

    _t(i.d, 'topical application technique',
       (ilxtr.hasPrimaryAspectActualized, asp.location),
       # FIXME
       (ilxtr.hasTarget, ilxtr.externalSurfaceOfOrganism)),

    _t(i.d, 'mechanical delivery technique',
       (ilxtr.hasPrimaryAspectActualized, asp.location),
       # FIXME
       (ilxtr.hasMotiveForce, ilxtr.mechanical)),
    _t(i.d, 'rocket delivery technique',
       (ilxtr.hasPrimaryAspectActualized, asp.location),
       (hasInput, ilxtr.rocket)),

    _t(OntTerm('BIRNLEX:2135'), 'injection technique',
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasSomething, ilxtr.intoSomething),  # FIXME
                      restN(ilxtr.hasPrimaryAspectActualized, asp.location)),
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasPrimaryParticipant, ilxtr.somethingThatCanBeInjected)),  # FIXME
       synonyms=('injection',),
       equivalentClass=oECN),

    _t(i.d, 'ballistic injection technique',
       # makes use of phenomena?
       (ilxtr.hasSomething, ilxtr.intoSomething),  # FIXME
       (ilxtr.hasPrimaryAspectActualized, asp.location),
       (ilxtr.hasSomething, i.d)),

    _t(i.d, 'pressure injection technique',
       # makes use of phenomena?
       (ilxtr.hasSomething, ilxtr.intoSomething),  # FIXME
       (ilxtr.hasPrimaryAspectActualized, asp.location),
       (ilxtr.hasSomething, i.d)),

    _t(i.d, 'brain injection technique',
       (hasPart, tech.injection),  # FIXME we need a way to have primary aspect + target? what is a target?
       # in other similar cases we have used hasPart, but then we have to have the
       # non-transitive hasPart because 
       (ilxtr.hasPrimaryParticipant, OntTerm('UBERON:0000955')),
       synonyms=('brain injection', 'injection into the brain')),

    _t(OntTerm('BIRNLEX:2136'), 'intracellular injection technique',
       ilxtr.technique,
       (hasPart, ilxtr.injection),
       unionOf(restN(hasPart, tech.cellPatching),  # vs oneOf? which fails to load?
               restN(hasPart, tech.sharpElectrodeTechnique)),
       (ilxtr.hasPrimaryParticipant, OntTerm('GO:0005622', label='intracellular')),
       #(ilxtr.hasPrimaryParticipant, OntTerm()),
       #(ilxtr.hasPrimaryParticipant, OntTerm('SAO:1289190043', label='Cellular Space')),  # TODO add intracellular as synonym
       synonyms=('intracellular injection',)),

    _t(i.d, 'electrical delivery technique',
       # FIXME electroporation doesn't actually work this way
       (ilxtr.hasPrimaryAspectActualized, asp.location),
       (ilxtr.hasConstrainingAspect, asp.electrical),
       (ilxtr.hasSomething, i.d)),
    _t(tech.electroporation, 'electroporation technique',
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasPrimaryParticipant, ilxtr.cellMembrane),
                      restN(ilxtr.hasPrimaryAspectActualized, asp.permeability),
                      restN(hasParticipant, ilxtr.electricalField)),  # FIXME ?
       intersectionOf(ilxtr.technique,
                      restN(hasPart, tech.electroporation)),
       # TODO can we add a check that the partOf hasParticipant cell?
       equivalentClass=oECN),
    _t(i.d, 'in utero electroporation technique',
       (hasPart, tech.electroporation),
       (ilxtr.hasPrimaryParticipant, restN(locatedIn, ilxtr.uterus))),
    _t(i.d, 'single cell electroporation technique',
       (hasPart, tech.electroporation),
       (hasPart, tech.cellPatching),
       # FIXME the target of permeability is not the cell but rather the cell membrane :/
       restMaxCardValue(ilxtr.hasPrimaryInput, OntTerm('SAO:1813327414', label='Cell'), Literal(1))),
    #_t(i.d, 'chemical delivery technique',  # not obvious how to define this or if it is used
       #(ilxtr.hasSomething, i.d)),

    _t(i.d, 'DNA delivery technique',
       (ilxtr.hasPrimaryInput, OntTerm('CHEBI:16991', term='DNA')),
       # isConstrainedBy information content of the dna?
       (ilxtr.hasPrimaryAspectActualized, asp.location),
      ),
    _t(i.d, 'transfection technique',
       (ilxtr.hasPrimaryInput, OntTerm('CHEBI:16991', term='DNA')),
       (ilxtr.hasPrimaryAspectActualized, asp.location),
       (ilxtr.hasSomething, i.d)),
    _t(i.d, 'DNA delivery exploiting some pre-existing mechanism technique',
       (ilxtr.hasPrimaryInput, OntTerm('CHEBI:16991', term='DNA')),
       (ilxtr.hasPrimaryAspectActualized, asp.location),
       (ilxtr.hasSomething, i.d)),
    _t(i.d, 'DNA delivery via primary genetic code technique',
       (ilxtr.hasPrimaryInput, OntTerm('CHEBI:16991', term='DNA')),
       (ilxtr.hasPrimaryAspectActualized, asp.location),
       (hasParticipant, ilxtr.primaryHeritableGeneticMaterial)),
    _t(i.d, 'DNA delivery via germ line technique',
       (ilxtr.hasPrimaryInput, OntTerm('CHEBI:16991', term='DNA')),
       (ilxtr.hasPrimaryAspectActualized, asp.location),
       (ilxtr.hasSomething, i.d)),
    _t(i.d, 'DNA delivery via plasmid technique',
       (ilxtr.hasPrimaryInput, OntTerm('CHEBI:16991', term='DNA')),
       (ilxtr.hasPrimaryAspectActualized, asp.location),
       (hasParticipant, ilxtr.plasmidDNA)),
    _t(i.d, 'DNA delivery via viral particle technique',
       (ilxtr.hasPrimaryInput, OntTerm('CHEBI:16991', term='DNA')),
       (ilxtr.hasPrimaryAspectActualized, asp.location),
       # notion of failure due to inadequate titer...
       (hasParticipant, ilxtr.viralParticle)),

    _t(i.d, 'tracing technique',
       (hasParticipant, ilxtr.axon),
       (ilxtr.hasPrimaryAspect, asp.connectivity),
       synonyms=('axon tracing technique',
                 'axonal tracing technique',
                 'axon tracing',
                 'axonal tracing',)),

    _t(ilxtr.anterogradeMovement, 'anterograde movement',
       BFO['0000015'],
       (hasParticipant, ilxtr.materialEntity),
       #(ilxtr.processActualizesAspect, asp.distanceFromSoma),  # asp and has hasContext
       # FIXME aspects for processes
       (ilxtr.hasPrimaryAspect, asp.distanceFromSoma),  # asp and has hasContext
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.positive),
      ),

    _t(ilxtr.retrogradeMovement, 'retrograde movement',
       BFO['0000015'],
       (hasParticipant, ilxtr.materialEntity),
       #(ilxtr.processActualizesAspect, asp.distanceFromSoma),  # asp and has hasContext
       # FIXME aspects for processes
       (ilxtr.hasPrimaryAspect, asp.distanceFromSoma),  # asp and has hasContext
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.negative),
      ),

    _t(i.d, 'anterograde tracing technique',
       (hasPart, tech.delivery),
       (hasParticipant, ilxtr.axon),
       (hasPart, ilxtr.anterogradeMovement),
       (ilxtr.hasPrimaryAspect, asp.connectivity),
       #(ilxtr.hasConstrainingAspect, asp.direction),  # need a value... also hasParticipantPartConstrainingAspect?
       #(ilxtr.hasConstrainingAspect_value, ilxtr.awayFromSoma),  # FIXME actual binding requiress subprocess
       # has subprocess (anterograte transport/movement)
       # hasPrimaryParticipant ilxtr.materialEntity
       # hasPrimaryAspect distanceFromSoma
       # hasPrimaryAspect_dAdT ilxtr.negative
       synonyms=( 'anterograde tracing',)
    ),
    _t(i.d, 'retrograde tracing technique',
       (hasPart, tech.delivery),
       (hasParticipant, ilxtr.axon),
       (hasPart, ilxtr.retrogradeMovement),
       (ilxtr.hasPrimaryAspect, asp.connectivity),
       #(ilxtr.hasConstrainingAspect, asp.direction),  # need a value... also hasParticipantPartConstrainingAspect?
       #(ilxtr.hasConstrainingAspect_value, ilxtr.towardSoma),  # FIXME actual binding requiress subprocess
       # has subprocess
       # hasPrimaryParticipant ilxtr.materialEntity
       # hasPrimaryAspect distanceFromSoma
       # hasPrimaryAspect_dAdT ilxtr.positive
       synonyms=('retrograde tracing',)
    ),
    _t(i.d, 'diffusion tracing technique',
       (hasParticipant, ilxtr.axon),
       (hasPart, tech.delivery),
       (ilxtr.hasPrimaryAspect, asp.connectivity),
       (ilxtr.hasSomething, i.d),
       synonyms=('diffusion tracing',)
    ),
    _t(i.d, 'transsynaptic tracing technique',
       (hasPart, tech.delivery),  # agentous delivery mechanism...
       (hasParticipant, ilxtr.axon),
       (ilxtr.hasPrimaryAspect, asp.connectivity),
       (ilxtr.hasParticipant, ilxtr.synapse),
       # more than one cell body
       synonyms=( 'transsynaptic tracing',)
    ),
    _t(i.d, 'multisynapse transsynaptic tracing technique',
       (hasParticipant, ilxtr.axon),
       (hasPart, tech.delivery),
       (ilxtr.hasPrimaryAspect, asp.connectivity),
       # more than cell body and more than one nerve
       (ilxtr.hasParticipant, ilxtr.synapse),  # synapses between at least 2 pairs of cells
       (ilxtr.hasSomething, i.d),
       synonyms=('multisynaptic transsynaptic tracing technique',
                 'multisynaptic transsynaptic tracing')),

    # 'TRIO'
    # 'tracing the relationship between input and output'

    _t(i.d, 'computational technique',  # these seem inherantly circulat... they use computation...
       ilxtr.technique,
       restMinCardValue(ilxtr.isConstrainedBy, ilxtr.algorithem, Literal(1)),  # axioms??
       (ilxtr.hasDirectInformationInput, ilxtr.informationEntity),
       (ilxtr.hasInformationOutput, ilxtr.informationEntity),
       # different from?
      ),

    #_t(i.d, 'mathematical technique',
       #(ilxtr.hasSomething, i.d),
       #(ilxtr.isConstrainedBy, ilxtr.algorithem),
      #),

    _t(tech.statistics, 'statistical technique',
       (ilxtr.hasInformationInput, ilxtr.informationEntity),
       (ilxtr.hasInformationOutput, ilxtr.informationEntity),
       (ilxtr.isConstrainedBy, ilxtr.statisticalAlgorithem),
      ),

    _t(i.d, 'simulation technique',
       (ilxtr.isConstrainedBy, ilxtr.algorithem),
       (ilxtr.hasInformationInput, ilxtr.informationEntity),
       (ilxtr.hasInformationOutput, ilxtr.informationEntity),
       (ilxtr.hasSomething, i.d)),

    _t(i.d, 'storage technique',
       (ilxtr.hasPrimaryAspectActualized, asp.location),
       # to put away for future use?
       # not for immediate use
       # sir no longer appearing in this protocol
       # leaves the scope of the technique's black box
       # put something in a consistent and known location
       # so that it can be retrieved again later when needed
       #(ilxtr.hasFutureTechique, tech.unstorage)
       # changing the primary aspect to a _known_ location
       #ilxtr.hasPrimaryAspect_dAdT
       (ilxtr.hasIntention, ilxtr.saveForTheFuture),
       ),

    _t(i.d, 'preservation technique',
       (ilxtr.hasPrimaryAspect, asp.spontaneousChangeInStructure),
       # FIXME change in change in some aspect
       # expected change in black box if this is not done?
       # asp.unbecoming
       # FIXME InContents? in anything inside the black box?
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.negative),
      ),

    _t(i.d, 'tissue preservation technique',
       (ilxtr.hasPrimaryParticipant, ilxtr.tissue),
       (ilxtr.hasPrimaryAspect, asp.spontaneousChangeInStructure),
      ),

    _t(i.d, 'localization technique',
       (ilxtr.hasSomething, i.d)),

    _t(i.d, 'colocalization technique',
       # FIXME measurement vs putting them together?
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),
       restMinCardValue(hasPart, tech.localization, Literal(2)),
       (ilxtr.hasPrimaryAspect, asp.location),
       (ilxtr.hasInformationOutput, ilxtr.informationEntity),
       # the localtion of the primary participants of eac
      ),

    _t(i.d, 'image reconstruction technique',
       (ilxtr.hasDirectInformationInput, ilxtr.image),
       (ilxtr.hasInformationOutput, ilxtr.image),
       (ilxtr.isConstrainedBy, ilxtr.inverseProblemAlgorithem)),

    _t(tech.tomography, 'tomographic technique',
       (ilxtr.hasDirectInformationInput, ilxtr.image),  # more than one...
       (ilxtr.hasInformationOutput, ilxtr.image),
       (ilxtr.isConstrainedBy, ilxtr.radonTransform),
       synonyms=('tomography',)),

    _t(i.d, 'positron emission tomography',
       (hasPart, tech.positronEmissionImaging),
       (hasPart, tech.tomography),
       synonyms=('PET', 'PET scan')),
    (i.p, ilxtr.hasTempId, OntTerm('HBP_MEM:0000009')),

    # "Single-Proton emission computerized tomography"
    # "HBP_MEM:0000010"  # TODO

    _t(i.d, 'stereology technique',
       (hasPart, tech.statistics),
       (ilxtr.hasSomething, i.d),
       synonyms=('stereology',)),

    _t(i.d, 'design based stereology technique',
       (ilxtr.hasSomething, i.d),
       synonyms=('design based stereology',)),

    _t(i.d, 'spike sorting technique',
       (ilxtr.hasDirectInformationInput, ilxtr.timeSeries),  # TODO more specific
       (ilxtr.hasInformationOutput, ilxtr.timeSeries),  # TODO MUCH more specific
       #(ilxtr.detects, ilxtr['informationPattern/spikes'])  # TODO?
       #(ilxtr.hasSomething, i.d),
       (ilxtr.isConstrainedBy, ilxtr.spikeSortingAlgorithem),
       synonyms=('spike sorting',)),

    _t(i.d, 'detection technique',
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),
       (ilxtr.hasInformationOutput, ilxtr.informationEntity),
       (ilxtr.detects, ilxtr.materialEntity)),
    _t(i.d, 'identification technique',
       (ilxtr.isConstrainedBy, ilxtr.identificationCriteria),  # FIXME circular and not what actually differentiates
       ),
    _t(i.d, 'characterization technique',
       (ilxtr.hasSomething, i.d)),
    _t(i.d, 'classification technique',
       (ilxtr.isConstrainedBy, ilxtr.classificationCriteria),  # FIXME circular and not what actually differentiates
       ),
    _t(i.d, 'curation technique',
       # ilxtr.isConstrainedBy, curation workflow specification... not helful and not correct
       (hasParticipant, OntTerm('NCBITaxon:9606')),
       (ilxtr.hasDirectInformationInput, ilxtr.informationArtifact),
       (ilxtr.hasInformationOutput, ilxtr.informationArtifact),
       (ilxtr.hasSomething, i.d)),

    _t(i.d, 'angiographic technique',
       (hasPart, ilxtr.xrayImaging),
       (ilxtr.knownDetectedPhenomena, restN(partOf, OntTerm('UBERON:0007798'))),
       synonyms=('angiography',)),

    _t(i.d, 'ex vivo technique',
       # (hasParticipant, ilxtr.somethingThatUsedToBeAlive),
       # more like 'was' a cellular organism
       # ah time... 
       ilxtr.technique,
       (ilxtr.hasPrimaryParticipant, OntTerm('NCBITaxon:131567', label='cellular organisms')),
       # has part some technique destroying primary participant
       # we really really need dead organisms to still have that type
       # which restricts our operational definitions a bit, but that is probably a good thing
       # 'dead but can still sequence its dna to confirm that -presently- its dna is that of a mouse'
       # the technique needs to have killed the exact member otherwise you can kill one mouse and study
       # a living one
       # (ilxtr.hasPriorTechnique, tech.killing),  # FIXME HRMMMMMM with same primary participant...
       (ilxtr.hasConstrainingAspect, asp.livingness),  # FIXME aliveness?
       restHasValue(ilxtr.hasConstrainingAspect_value, Literal(False)), # Literal(False)),  # FIXME dataProperty???
       #(ilxtr.hasConstrainingAspect, asp.livingness),  # FIXME aliveness?
       # (ilxtr.hasConstrainingAspect, ilxtr['is']),
       synonyms=('ex vivo',),),

    _t(tech.inSitu, 'in situ technique',  # TODO FIXME
       # detecting something in the location that it was originally in
       # not in the dissociated remains thereof...
       # hasPrimaryParticipantLocatedIn
       # and the primary participant is located in / still part of its original part of
       # part of the thing that it was part of before the start of _any_ technique
       #(ilxtr.hasConstrainingAspect, asp.location),

       # the pimary participant is still part of the part of the primary participant of the
       # preceeding technique where the input was living
       (ilxtr.hasConstrainingAspect, asp.location),
       #(ilxtr.hasConstrainingAspect_value, ilxtr.unchanged),  # FIXME
       (ilxtr.hasSomething, i.d),
       # primary participant partOf theSameContainingEntity
       synonyms=('in situ',),),
    (tech.inSitu, owl.disjointWith, tech.inVitro),

    _t(i.d, 'in vivo technique',
       # (hasParticipant, ilxtr.somethingThatIsAlive),
       ilxtr.technique,
       (ilxtr.hasPrimaryParticipant, OntTerm('NCBITaxon:131567', label='cellular organisms')),
       (ilxtr.hasConstrainingAspect, asp.livingness),  # FIXME rocks can have aspect aliveness,
       # aspects don't tell you about the universality of a result in the way that a quality might
       # because right now we only care about the details of the process and what we are measuring
       # that is what the value is included explicitly, because some day we might find out that our
       # supposedly universal axiom is not, and then we are cooked
       restHasValue(ilxtr.hasConstrainingAspect_value, Literal(True)), #  FIXME data property  Literal(True)),
       synonyms=('in vivo',),),

    _t(i.d, 'in utero technique',
       # has something in 
       #(hasParticipant, ilxtr.somethingThatIsAliveAndIsInAUterus),
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasConstrainingAspect, asp.location),
                      restN(ilxtr.hasConstrainingAspect_value, ilxtr.uterus)),
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasPrimaryParticipant, restN(locatedIn, ilxtr.uterus))),
       synonyms=('in utero',),
       equivalentClass=oECN),

    _t(tech.inVitro, 'in vitro technique',
       (ilxtr.hasPrimaryParticipant, ilxtr.physiologicalSystemDisjointWithLivingOrganism),
       #(ilxtr.hasPrimaryParticipant, thing that was derived from living organsim? no? pure synthesis...),
       (hasParticipant, ilxtr.somethingThatIsAliveAndIsInAGlassContainer),
       # this is more complicated than it seems,
       # the idea that you can have a physiological system
       # that is not either derived from some organism ...
       synonyms=('in vitro',),),

    _t(i.d, 'high throughput technique',
       (ilxtr.hasSomething, i.d),
       # TODO has minimum cardinality 'large' on the primary participant
       synonyms=('high throughput',),),

    _t(i.d, 'fourier analysis technique',
       (realizes, ilxtr.analysisRole),  # FIXME needs to be subClassOf role...
       (ilxtr.isConstrainedBy, ilxtr.fourierTransform),
       synonyms=('fourier analysis',),),

    _t(i.d, 'sample preparation technique',
       (ilxtr.hasSomething, i.d),
       # TODO
       # (ilxtr.hasIntention, ???)
       # to get the thing in the right state so that it can be measured
       (ilxtr.hasPrimaryAspect, intersectionOf(asp.nonLocal,
                                               restN(ilxtr.hasContext,
                                                     # FIXME again we see that hasContext
                                                     # is much broader
                                                     ilxtr.constraintImposedByNextStep))),
       synonyms=('preparation technique',
                 'specimine preparation technique',
                 'sample preparation',
                 'specimine preparation',),),

    _t(i.d, 'dissection technique',
       (ilxtr.hasPrimaryOutput, ilxtr.partOfSomePrimaryInput),  #FIXME
       synonyms=('dissection',),),

    _t(i.d, 'atlas guided microdissection technique',
       (ilxtr.isConstrainedBy, ilxtr.parcellationAtlas),
       (ilxtr.hasPrimaryOutput, ilxtr.partOfSomePrimaryInput),  #FIXME
       synonyms=('atlas guided microdissection',),),

    _t(i.d, 'crystallization technique',
       (ilxtr.hasPrimaryAspect, asp.latticePeriodicity),  # physical order
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.positive),
       # cyrstallized vs amorphous
       # xray diffraction can tell you what proportion of the whole samle is crystallized (S. Manna)
       def_=('A technique for enducing a regular crystal patterning '
             'on a set of non-patterend components'),
       synonyms=('crystallization',)),

    _t(i.d, 'crystal quality evalulation technique',
       (ilxtr.hasPrimaryAspect, asp.physicalOrderedness),
       # (ilxtr.hasPrimaryAspect, asp.percentCrystallinity),
       # there are many other metrics that can be used that are subclasses
      ),

    _t(i.d, 'tissue clearing technique',
       (ilxtr.hasPrimaryParticipant, ilxtr.tissue),
       (ilxtr.hasPrimaryAspect, asp.transparency),  # FIXME
      ),

    _t(i.d, 'CLARITY technique',
       (ilxtr.hasPrimaryParticipant, ilxtr.tissue),
       (ilxtr.isConstrainedBy, prot.CLARITY),
       (ilxtr.hasPrimaryAspect, asp.transparency),  # FIXME
       def_='A tissue clearing technique',
       synonyms=('CLARITY',)),

    _t(tech.fixation, 'fixation technique',
       # prevent decay, decomposition
       # modify the mechanical properties to prevent disintegration
       # usually crosslinks proteins?
       # cyrofixation also for improving the mechanical properties
       # literally "fix" something so that it doesn't move or changed, it is "fixed" in time
       #(ilxtr.hasSomething, i.d),
       #(ilxtr.hasPrimaryAspect, asp.spontaneousChangeInStructure),
       #(ilxtr.hasPrimaryAspect_dAdT, ilxtr.negative),
       #(ilxtr.hasPrimaryAspect, asp.likelinessToDecompose),
       #(ilxtr.hasPrimaryAspect, asp.mechanicalRigidity),
       #(ilxtr.hasPrimaryAspect_dAdT, ilxtr.positive),
       ilxtr.technique,
       unionOf(restN(ilxtr.hasPrimaryAspectActualized, asp.mechanicalRigidity),
               restN(ilxtr.hasPrimaryAspectActualized, asp.spontaneousChangeInStructure)),
       #unionOf(hasAspectChangeCombinator(asp.mechanicalRigidity, ilxtr.positive),
               # this approach was simply too verbose and didn't help with classification at all
               #hasAspectChangeCombinator(asp.spontaneousChangeInStructure, ilxtr.negative)),
       synonyms=('fixation',)),

    #oc_(tech.fixation,
       #),

    _t(i.d, 'tissue fixation technique',
       tech.fixation,
       (ilxtr.hasPrimaryParticipant, ilxtr.tissue),
       synonyms=('tissue fixation',)),

    _t(i.d, 'sensitization technique',
       # If we were to try to model this fully in the ontology
       # then we would have a giant hiearchy of sensitivities to X
       # when in fact sensitivity is a defined measure/aspect not
       # a fundamental aspect. It is fair to say that there could be
       # an aspect for every different way there is to measure sensitivity
       # to sunlight since the term is so broad
       (ilxtr.hasPrimaryAspectActualized, asp.sensitivity),
    ),

    _t(i.d, 'permeabilization technique',
       # TODO how to model 'the permeability of a membrane to X'
       #  check go
       (ilxtr.hasPrimaryAspectActualized, asp.permeability),
    ),

    _t(i.d, 'chemical synthesis technique',
       # involves some chemical reaction ...
       # is ioniziation a chemical reaction? e.g. NaCl -> Na+ Cl-??
       (ilxtr.hasPrimaryOutput,  OntTerm('CHEBI:24431', label='chemical entity')),
      ),
    #_t(i.d, 'physical synthesis technique',  # this term isn't used very widely
       # e.g. making a microchip, doesn't just use chemistry, though it uses some chemistry
       # the output is not chemical...
       #(ilxtr.hasPrimaryOutput, ilxtr.materialEntity),
      #),

    _t(i.d, 'construction technique',
       # build something, or assemble something that cannot be removed
       # deconstruction vs destruction, deconstruction usually suggests
       # can't be reconstructed? but then we reconstructive surgery
       (ilxtr.hasPrimaryOutput, ilxtr.building),  # TODO
       (ilxtr.hasSomething, i.d),
      ),

    _t(i.d, 'assembly technique',
       # put something together
       # suggests that disassembly is possible
       (ilxtr.hasPrimaryOutput, ilxtr.thing),  # TODO
       (ilxtr.hasSomething, i.d),
      ),

    _t(i.d, 'mixing technique',
       #tech.creating,  # not entirely clear that this is the case...
       #ilxtr.mixedness is circular
       (ilxtr.hasSomething, i.d),
       synonyms=('mixing',),),

    _t(i.d, 'agitating technique',
       #tech.mixing,
       # allocation on failure?
       # classification depends exactly on the goal
       (ilxtr.hasSomething, i.d),
       synonyms=('agitating',),),

    _t(i.d, 'stirring technique',
       #tech.mixing,  # not clear, the intended outcome may be that the thing is 'mixed'...
       (ilxtr.hasSomething, i.d),
       synonyms=('stirring',),),

    _t(i.d, 'dissolving technique',
       (ilxtr.hasSomething, i.d),
       synonyms=('dissolve',),),

    _t(i.d, 'husbandry technique',
       # FIXME maintenance vs growth
       # also how about associated techniques?? like feeding
       # include in the oec or 'part of some husbandry technique'??
       # alternately we can change it to hasParticipant ilxtr.livingOrganism
       # to allow them to include techniques where locally the
       # primary participant is something like food, instead of the organism HRM
       tech.maintaining,
       (hasParticipant,  # vs primary participant
        OntTerm('NCBITaxon:1', label='ncbitaxon')
       ),
       synonyms=('culture technique', 'husbandry', 'culture'),),

    _t(i.d, 'feeding technique',
       # metabolism required so no viruses
       # TODO how to get this to classify as a maintenance technique
       #  without having to include the entailment explicitly
       #  i.e. how do we deal side effects of processes

       (hasParticipant, OntTerm('NCBITaxon:131567', label='cellular organisms')),
       (hasInput, ilxtr.food),
       synonyms=('feeding',)),

       (i.p, rdfs.subClassOf, tech.maintaining),
       # this is a legitimate case where there is no easy
       # way to communicate a side effect of feeding
       # I will thing a bit more on this but I think it is the easiest way
       # maybe a general class axiom or something like that could do it
       # FIXME the issue is that the primary aspects will then start to fight...
       #  there might be a way to create a class that will work using
       #  ilxtr.hasSideEffectTechnique or ilxtr.hasSideEffect?

    _t(i.d, 'high-fat diet feeding technique',
       (hasParticipant, OntTerm('NCBITaxon:131567', label='cellular organisms')),
       (ilxtr.hasPrimaryAspect, asp.weight),
       (hasInput, ilxtr.highFatDiet),
    ),

    _t(i.d, 'mouse circadian based high-fat diet feeding technique',
       (ilxtr.hasPrimaryParticipant, OntTerm('NCBITaxon:10090', label='Mus musculus')),
       # ie that if one were to measure rather than specify
       # the mouse should be in in the same phase during the activity
       (ilxtr.hasConstrainingAspect, asp.circadianPhase),  # TODO? 'NBO:0000169'
       (ilxtr.hasPrimaryAspect, asp.weight),
       (hasInput, ilxtr.highFatDiet),
       ),

    _t(i.d, 'mouse age based high-fat diet feeding technique',
       # TODO there are a whole bunch of other high fat diet feeding techniques
       # 'MmusDv:0000050'
       # as opposed to the primary aspect being the current point in the cyrcadian cycle
       (ilxtr.hasPrimaryParticipant, OntTerm('NCBITaxon:10090', label='Mus musculus')),
       (ilxtr.hasConstrainingAspect, OntTerm('PATO:0000011', label='age')),  # FIXME not quite right
       (ilxtr.hasPrimaryAspect, asp.weight),  # FIXME not quite right
       (hasInput, ilxtr.highFatDiet),
       # (hasInput, ilx['researchdiets/uris/productnumber/D12492']),  # too specific
       ),

    _t(i.d, 'bacterial culture technique',
       tech.maintaining,
       #(hasParticipant, OntTerm('NCBITaxon:2', label='Bacteria <prokaryote>')),
       (hasParticipant, OntTerm('NCBITaxon:2')),  # FIXME > 1 label
       synonyms=('bacterial culture',),),

    _t(i.d, 'cell culture technique',
       tech.maintaining,
       (hasParticipant, OntTerm('SAO:1813327414', label='Cell')),
       synonyms=('cell culture',),),

    _t(i.d, 'yeast culture technique',
       tech.maintaining,
       (hasParticipant, OntTerm('NCBITaxon:4932', label='Saccharomyces cerevisiae')),
       synonyms=('yeast culture',),),

    _t(i.d, 'tissue culture technique',
       tech.maintaining,
       (hasParticipant, ilxtr.tissue),
       synonyms=('tissue culture',),),

    _t(i.d, 'slice culture technique',
       tech.maintaining,
       (hasParticipant, ilxtr.brainSlice),  # FIXME
       synonyms=('slice culture',),),

    _t(i.d, 'open book preparation technique',
       tech.maintaining,
       (hasInput,
        OntTerm('UBERON:0001049', label='neural tube')
        #OntTerm(term='neural tube', prefix='UBERON')  # FIXME dissected out neural tube...
       ),
       synonyms=('open book culture', 'open book preparation'),),

    _t(i.d, 'fly culture technique',
       tech.maintaining,
       (hasParticipant,
        OntTerm('NCBITaxon:7215', label='Drosophila <fruit fly, genus>')
        #OntTerm(term='drosophila')
       ),
       synonyms=('fly culture',),),

    _t(i.d, 'rodent husbandry technique',
       tech.maintaining,
       (ilxtr.hasPrimaryParticipant,
        OntTerm('NCBITaxon:9989', label='Rodentia')  # FIXME population vs individual?
       ),
       synonyms=('rodent husbandry', 'rodent culture technique'),),

    _t(i.d, 'enclosure design technique',  # FIXME design technique? produces some information artifact?
       (ilxtr.hasSomething, i.d)),

    _t(i.d, 'housing technique',
       (ilxtr.hasSomething, i.d),
       synonyms=('housing',),
    ),
    _t(i.d, 'mating technique',
       ilxtr.technique,
       restMinCardValue(hasParticipant, ilxtr.sexuallyReproducingOrgansim, Literal(2)),
       synonyms=('mating',),
    ),
    _t(i.d, 'watering technique',
       (hasParticipant, OntTerm('NCBITaxon:131567', label='cellular organisms')),
       (ilxtr.hasPrimaryInput, ilxtr.water),
       synonyms=('watering',),
    ),

    _t(tech.contrastEnhancement, 'contrast enhancement technique',
       #restMinCardValue(ilxtr.hasParticipantPartConstrainingAspect, ilxtr.aspect, Literal(1)),
       #restMinCardValue(ilxtr.hasConstrainingAspect, ilxtr.aspect, Literal(1)),
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasParticipantPartPrimaryAspect, ilxtr.aspect),
                      restN(ilxtr.hasPartNotPart,
                            intersectionOf(restN(ilxtr.hasPrimaryAspectActualized, asp.location),
                                           # FIXME need to be able to say that pp part primary aspect and
                                           # part pp constraining aspect are the same
                                           restMinCardValue(ilxtr.hasConstrainingAspect,
                                                            ilxtr.aspect,
                                                            Literal(1))))),
       #intersectionOf(ilxtr.technique,
                      #restN(ilxtr.hasPrimaryAspect, asp.contrast),
                      #restN(ilxtr.hasPrimaryAspect_dAdT, ilxtr.positive)),
       #intersectionOf(ilxtr.technique,
                      # FIXME vs contrast detection
                      #restN(ilxtr.hasProbe, ilxtr.materialEntity)),
       synonyms=('contrast enhancement',
                 'material contrast enhancement technique',),
       equivalentClass=oECN),

    _t(i.d, 'tagging technique',
       (ilxtr.hasSomething, i.d)),

    _t(tech.histology, 'histological technique',
       # is this the assertional/definitional part where we include everything?
       (ilxtr.hasPrimaryParticipant, ilxtr.tissue),
       #(ilxtr.hasSomething, i.d),
       synonyms=('hisology',)),

    _t(OntTerm('BIRNLEX:2107'), 'staining technique',  # TODO integration
       (ilxtr.hasSomething, i.d)),

    _t(i.d, 'immunochemical technique',
       (ilxtr.hasSomething, i.d)),

    _t(i.d,'immunocytochemical technique',
       (ilxtr.hasSomething, i.d),
       (hasInput, ilxtr.cell),
       synonyms=('immunocytochemistry technique',
                 'immunocytochemistry')),

    _t(OntTerm('NLXINV:20090609'), 'immunohistochemical technique',  # TODO
       (ilxtr.hasSomething, i.d),
       (hasInput, ilxtr.tissue),
       synonyms=('immunohistochemistry technique',
                 'immunohistochemistry')),
    (OntTerm('NLXINV:20090609'), ilxtr.hasTempId, OntTerm("HBP_MEM:0000115")),
    
    # TODO "HBP_MEM:0000116"
    # "Immunoelectron microscopy"

    _t(i.d, 'direct immunohistochemical technique',
       (ilxtr.hasSomething, i.d),
       synonyms=('direct immunohistochemistry technique',
                 'direct immunohistochemistry')),
    _t(i.d, 'indirect immunohistochemical technique',
       (ilxtr.hasSomething, i.d),
       synonyms=('indirect immunohistochemistry technique',
                 'indirect immunohistochemistry')),

    _t(tech.stateBasedContrastEnhancement, 'state based contrast enhancement technique',
       #tech.contrastEnhancement,  # FIXME compare this to how we modelled fMRI below? is BOLD and _enhancement_?
       (ilxtr.hasSomething, i.d),

    ),

    _t(i.d, 'separation technique',
       # the aspect of each part is to separate it by class
       # the location of each of its parts
       # the rule for transforming an aspect of the _parts_ into
       # the location aspect is the key differentiator
       #(ilxtr.knownDifferentiatingPhenomena, ),
       #restN(hasPart, )
       #(ilxtr.hasPrimaryAspectActualized, asp.location),  # TODO we need a clearer subclass for this
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasPartPart,
                            intersectionOf(restN(ilxtr.hasPrimaryAspectActualized, asp.location),
                                           #ilxtr.primaryParticipantPartOfPrimaryParticipantOfParent,
                                           # intentionally not requiring this to be a technique
                                           restMinCardValue(ilxtr.hasConstrainingAspect,
                                                            ilxtr.aspect,
                                                            Literal(1))))),
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasParticipantPartPrimaryAspectActualized, asp.location),
                      restMinCardValue(ilxtr.hasParticipantPartConstrainingAspect,
                                       ilxtr.aspect,
                                       Literal(1))),
       #restMinCardValue(ilxtr.hasParentPrimaryAspect, ilxtr.aspect, Literal(1)),
       # primary input has parts that can all actualize on the same set of aspects
       # hasConstrainingAspect maybe??
       #(ilxtr.hasConstrainingAspect, ilxtr.aspect),
       # VS FIXME TODO does the cardinality restriction work for auto subclassing?
       # FIXME hasConstrainingAspect is implicitly on the primary participant, these are on its parts...
       #restMinCardValue(ilxtr.hasConstrainingAspect, ilxtr.aspect, Literal(1)),
       #(ilxtr.hasSomething, i.d),
       equivalentClass=oECN),
    _t(i.d, 'sorting technique',
       ilxtr.technique,
       # FIXME named => there is a larger black box where the name _can_ be measured
       # hasPrimaryParticipant partOf (hasAspect ilxtr.aspect)
       # or is it partOf (hasPrimaryAspect ilxtr.aspect)?
       # note that for this approach axioms appear automatically as
       # the unresolved names
       (ilxtr.hasParticipantPartPrimaryAspectActualized, asp.category),
       (ilxtr.hasParticipantPartConstrainingAspect, ilxtr.aspect)),

    _t(i.d, 'extraction technique',
       (hasParticipant, ilxtr.extract),  # FIXME circular
       ),
    _t(tech.precipitation, 'precipitation technique',
       (hasParticipant, ilxtr.precipitate),  # FIXME circular
      ),
    _t(i.d, 'pull-down technique',
       (hasPart, tech.precipitation),
       # allocation enrichement
       (ilxtr.hasSomething, i.d),),
    _t(i.d, 'isolation technique',
       # enrichment
       (ilxtr.hasSomething, i.d),),
    _t(i.d, 'purification technique',
       # enrichment
       (ilxtr.hasSomething, i.d),),

    _t(i.d, 'fractionation technique',
       (ilxtr.hasSomething, i.d),),
    _t(i.d, 'chromatography technique',
       (ilxtr.hasParticipantPartPrimaryAspectActualized, asp.location),
       (ilxtr.hasParticipantPartConstrainingAspect, asp.partitionCoefficient),
       synonyms=('chromatography',),),
    _t(i.d, 'distillation technique',
       (ilxtr.hasParticipantPartConstrainingAspect, asp.boilingPoint),
       (ilxtr.hasParticipantPartConstrainingAspect, asp.condensationPoint),
       #(ilxtr.knownDifferentiatingPhenomena, asp.boilingPoint),
       #(ilxtr.knownDifferentiatingPhenomena, asp.condensationPoint),
       synonyms=('distillation',),),
    _t(tech.electrophoresis, 'electrophoresis technique',
       #(ilxtr.hasSomething, i.d),
       (ilxtr.hasParticipantPartPrimaryAspectActualized, asp.location),
       (ilxtr.hasParticipantPartConstrainingAspect, asp.size),
       (ilxtr.hasParticipantPartConstrainingAspect, asp.charge),
       (ilxtr.hasParticipantPartConstrainingAspect, asp.bindingAffinity),  # FIXME ... this is qualified...
       synonyms=('electrophoresis',),),
    _t(i.d, 'centrifugation technique',
       intersectionOf(ilxtr.technique,
                      restN(hasInput, ilxtr.centrifuge)),
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasParticipantPartPrimaryAspectActualized, asp.location),
                      restN(ilxtr.hasParticipantPartConstrainingAspect, asp.size),  # TODO hasImplicitMeasurement
                      restN(ilxtr.hasParticipantPartConstrainingAspect, asp.shape),
                      restN(ilxtr.hasParticipantPartConstrainingAspect, asp.density)),
       #(ilxtr.knownDifferentiatingPhenomena, asp.size),  # TODO hasImplicitMeasurement
       #(ilxtr.knownDifferentiatingPhenomena, asp.shape),
       #(ilxtr.knownDifferentiatingPhenomena, asp.density),
       synonyms=('centrifugation',),
       equivalentClass=oECN),
    _t(i.d, 'ultracentrifugation technique',
       (hasInput, ilxtr.ultracentrifuge),
       synonyms=('ultracentrifugation',),),

    _t(i.d, 'sampling technique',
       # selection technqiue, not a separation technique
       # it has to do with picking
       (ilxtr.hasSomething, i.d),),
    _t(i.d, 'selection technique',
       (ilxtr.hasSomething, i.d),),
    _t(i.d, 'blind selection technique',
       (ilxtr.hasSomething, i.d),),
    _t(i.d, 'random selection technique',
       (ilxtr.hasSomething, i.d),),
    _t(i.d, 'targeted selection technique',
       (ilxtr.hasSomething, i.d),),

    _t(i.d, 'biological activity measurement technique',
       (ilxtr.hasPrimaryParticipant, ilxtr.physiologicalSystem),
       (ilxtr.hasPrimaryAspect, asp.biologicalActivity),  # TODO
       (ilxtr.hasInformationOutput, ilxtr.informationEntity),
       synonyms=('activity measurement technique', 'bioassay')),

    _t(i.d, 'observational technique',
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),
       (ilxtr.hasInformationOutput, ilxtr.informationEntity),
       # non numerical? interpretational?
       (ilxtr.hasSomething, i.d),
       synonyms=('observation', 'observation technique'),),

    _t(i.d, 'procurement technique',
       (ilxtr.hasPrimaryAspect, asp.location),
       (ilxtr.hasPrimaryParticipant,
        OntTerm('BFO:0000040', label='material entity')
        #OntTerm(term='material entity', prefix='BFO')
       ),
       (ilxtr.hasPrimaryOutput,
        OntTerm('BFO:0000040', label='material entity')
        #OntTerm(term='material entity', prefix='BFO')
       ),
       def_='A technique for getting or retrieving something.',
       synonyms=('acquisition technique', 'procurement', 'acquistion', 'get')
    ),

    # naming
    oc(tech.naming, ilxtr.technique),
    olit(tech.naming, rdfs.label, 'naming'),
    olit(tech.naming, definition ,
         ('Naming is an assertional process that is orthogonal to measuring.'
          'Names may be assigned as a product of measurements, but the assignment '
          'of a name can only be based on aspects of the thing, the name can never be '
          'an aspect of the thing. Names may also be assigned based on aspects of the '
          'process that produced the thing, or the prvious state of the thing. '
          'For example a protein dissociated from its original cell/tissue no longer '
          'contains sufficient information to reconsturct where it came from based on '
          'any measurements that can be made on it beyond the species that it came from '
          'and maybe where the individual lived if there are enough atoms to do an isotope test.'
          'A cell on the other hand may very well have enough information in its RNA and DNA to '
          'allow for a bottom up assignment of a name based on its gene expression pattern.')),

    _t(tech.ising, 'ising technique',
       (ilxtr.hasPrimaryAspect, asp['is']),
       def_=('Ising techniques are techniques that affect whether a thing \'is\' or not. '
             'Whether they primary participant \'is\' in this context must shall be determined '
             'by whether measurements made on the putative primary particiant '
             'provide data that meet the necessary and sufficient criteria for the putative primary '
             'participant to be assigned the categorical name as defined by the '
             'primary particiant\'s owl:Class. For example if the primary particiant of a technique '
             'is 100ml of liquid water, then a boiling technique which produces gaseous water from '
             'liquid water negatively affects the isness of the 100ml of liquid water because we can '
             'no longer assign the name liquid water to the steam that is produced by boiling.')),

    olit(tech.ising, rdfs.comment,
         ('Because \'isness\' or \'being\' is modelled as an aspect it is implied that '
          '\'being\' in this context depends entirely on some measurement process and some '
          'additional process for classifying or categorizing the object based on that measurement, '
          'so that it can be assigned a name. The objective here is to demistify the process of '
          'assigning a name to a thing so that it will be possible to provide exact provenance '
          'for how the assignment of the name was determined.')),

    # allocating
    _t(tech.allocating, 'allocating technique',
       (ilxtr.hasPrimaryAspectActualized, asp.location),  # FIXME intrinsic extrinsic issue :/
       # FIXME no information output
       def_=('Allocating techniques move things around without changing how their participants '
             'are named. More accurately they move them around without changing any part of their '
             'functional defintions which are invariant as a function of their location.'),
      ),
    (tech.allocating, owl.disjointWith, tech.measuring),  # i am an idiot
    # measured does not imply actualized
    # FIXME what about tech.actualizing? i think it is ising or allocating
    # FIXME this causes issues
    # we may need to split hasPrimaryAspect into hasPrimaryAspectMeasure hasPrimaryAspectActualized
    # better to just add hasPrimaryAspectActualized for allocation and friends since pretty much all
    # aspects end up being measured one way or another, they have to be
    #oc_(tech.allocating,
        #blankc(owl.disjointWith,  # overkill using oec but it works
               #oc_.full_combinator(oec(
                   #ilxtr.technique,
                   #restrictionN(ilxtr.hasInformationOutput,
                                #ilxtr.informationEntity))))),

    # measuring
    _t(tech.measuring, 'measuring technique',
       # TODO is detection distinct from measurement if there is no explicit symbolization?
       (ilxtr.hasInformationOutput, ilxtr.informationEntity),  # observe that this not information artifact
       # FIXME has primary input?
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity #OntTerm('BFO:0000001', label='entity')
        # FIXME vs hasPrimaryParticipant
        # go with material entity since seeing data processing under measurement seems off
       ),
       synonyms=('measure', 'measurment technique'),
    ),

    # actualizing
    _t(tech.actualizing, 'actualizing technique',
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasPrimaryAspectActualized, ilxtr.aspect)),
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasParticipantPartPrimaryAspectActualized, ilxtr.aspect)),
       # taking action to make the value 
       #unionOf(tech.ising, tech.allocating),
       def_='a technique that realizes a value of some aspect',
       equivalentClass=oECN),

    # probing
    _t(tech.probing, 'probing technique',  # manipulating, poking, purturbing, changing state
       (ilxtr.hasProbe, owl.Thing),
       #(ilxtr.hasProbe, OntTerm('BFO:0000040', label='material entity')),
       # FIXME technically could be an informational entity?
       # if I probe someone by speaking latin but they do not respond
       # vs if they do it is not the physical content of the sounds
       # it is how they interact with the state of the other person's brain
       def_=('Probing techniques attempt (intende) to change the state of a thing without changing '
            'how it is named. Hitting something with just enough light to excite but not to '
            'bleach would be one example, as would poking something with a non-pointy stick.'
           ),
     ),

    _t(tech.creating, 'creating technique',   # FIXME mightent we want to subclass off of these directly?
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasPrimaryOutput, ilxtr.materialEntity)),
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasPrimaryAspect, asp['is']),
                      restN(ilxtr.hasPrimaryAspect_dAdT, ilxtr.positive)),
       synonyms=('synthesis technique',),
       equivalentClass=oECN),
    (tech.creating, owl.disjointWith, tech.destroying),
    # NOTE ! creating and destroying are only with respect to the primary participant
    # it is entirely possible to have a composite technique that has two parts
    # one of which is destroying and the other of which is creating
    # and to link those two parts in such as way as to assert the symmetry

    # attempt to create a class that explicitly does not have relationships to the same other class
    #oc(ilxtr._helper0),
    #olit(ilxtr._helper0, 'that have classes that are primary participants and outputs of the same technique'),
    #disjointwith(oec(None, ilxtr.technique,
                  #*restrictions((ilxtr.hasPrimaryParticipant,
                                  #OntTerm('continuant', prefix='BFO'))))),
    #obnode(object_predicate_combinator(rdf.type, owl.Class),
           #oec_combinator(ilxtr.technique,
                     #(ilxtr.hasPrimaryParticipant,)
                     #(hasOutput,))),

    _t(tech.destroying, 'destroying technique',
       # owl.unionOf with not ilxtr.disjointWithOutput of? not this will not work
       (ilxtr.hasPrimaryAspect, asp['is']),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.negative),),

    _t(tech.maintaining, 'maintaining technique',
       # if these were not qualified by the primary participant
       # then this would be both a creating and a destroying technique
       (ilxtr.hasPrimaryAspect, asp['is']),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.zero),  # FIXME value?
       synonyms=('maintenance technique',),
    ),

    _t(i.d, 'analysis technique',
       (realizes, ilxtr.analysisRole),
       synonyms=('analysis',),),

    _t(i.d, 'data processing technique',
       (ilxtr.hasDirectInformationInput, ilxtr.informationEntity),
       (ilxtr.hasInformationOutput, ilxtr.informationEntity),
       synonyms=('data processing', 'data transformation technique'),),

    _t(i.d, 'image processing technique',
       (ilxtr.hasDirectInformationInput, ilxtr.image),
       (ilxtr.hasInformationOutput, ilxtr.image),
       # some subpart may have the explicit output it just requires the direct input
       synonyms=('image processing',),),

    _t(tech.sigproc, 'signal processing technique',
       (ilxtr.hasDirectInformationInput, ilxtr.timeSeries),
       (ilxtr.hasInformationOutput, ilxtr.timeSeries),
       synonyms=('signal processing',),),

    _t(i.d, 'signal filtering technique',
       # FIXME aspects of information entities...
       # lots of stuff going on here...
       tech.sigproc,
       (ilxtr.hasInformationPrimaryAspect, asp.spectrum),
       (ilxtr.hasInformationPrimaryAspect_dAdT, ilxtr.negative),
       (ilxtr.hasInformationPrimaryParticipant, ilxtr.timeSeries),  # FIXME
       synonyms=('signal filtering',),
    ),

    _t(tech.ephys, 'electrophysiology technique',
       # TODO is this one of the cases where partonomy implies techniqueness?
       # note ephys is not itself a measurement technique? stimulation can occur without measurement
       # technique and (hasPart some i.p)
       intersectionOf(ilxtr.technique,
                      restN(hasInput, ilxtr.ephysRig)),
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasPrimaryAspect, asp.electromagnetic),  # FIXME...
                      restN(ilxtr.hasPrimaryParticipant, ilxtr.physiologicalSystem)),
       synonyms=('electrophysiology', 'electrophysiological technique'),
       equivalentClass=oECN),
    (tech.ephys, ilxtr.hasTempId, OntTerm('HBP_MEM:0000014')),

    _t(tech.IRDIC, 'IR DIC video microscopy',
       (hasInput, ilxtr.IRCamera),
       (ilxtr.detects, ilxtr.infaredLight),
       (hasInput, ilxtr.DICmicroscope),
       (ilxtr.hasInformationOutput, ilxtr.image),
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),  # how to deal with the parts of a primary input?
       # TODO
      ),

    _t(i.d, 'modern in vitro slice electrophysiology',
       (hasPart, tech.IRDIC),
       (ilxtr.hasPrimaryInput, ilxtr.acuteBrainSlice),  # how to deal with the parts of a primary input?
       (ilxtr.hasPrimaryAspect, asp.electrical),
       (hasPart, ilxtr.cellPatching),
       (hasPart, ilxtr.eClamp),
       (ilxtr.hasInformationOutput, ilxtr.timeSeries),
      ), 

    _t(i.d, 'electrophysiology recording technique',
       ilxtr.technique,
       (ilxtr.hasPrimaryParticipant, ilxtr.physiologicalSystem),
       #oneOf((hasInput, ilxtr.physiologicalSystem),
             #(hasInput, OntTerm('NCBITaxon:1'))),
       (ilxtr.hasPrimaryAspect, asp.electrical),  # FIXME...
       #(ilxtr.hasPrimaryParticipant, ilxtr.physiologicalSystem),
       #(hasPart, tech.ephys),
       (ilxtr.hasInformationOutput, ilxtr.timeSeries),
      ),

    _t(tech.contrastDetection, 'contrast detection technique',
       # a subclass could be differential contrast to electron scattering or something...
       #(ilxtr.hasPrimaryAspect_dAdPartOfPrimaryParticipant, ilxtr.nonZero),  # TODO FIXME this is MUCH better
       (ilxtr.hasPrimaryAspect, asp.contrast),  # contrast to something? FIXME this seems a bit off...
       (ilxtr.hasPrimaryAspect_dAdS, ilxtr.nonZero),
       synonyms=('contrast detection',),
    ),

    _t(tech.microscopy, 'microscopy technique',
       (hasInput, ilxtr.microscope),  # electrophysiology microscopy techinque?
       # can't use hasParticipant because we need it to be distinct from 'microscope production technique'
       (ilxtr.hasInformationOutput, ilxtr.image),
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),
       synonyms=('microscopy',),
    ),

    _t(i.d, 'microscope production technique',
       (ilxtr.hasPrimaryOutput, ilxtr.microscope),
      ),

    _t(i.d, 'recording electrode production technique',
       (ilxtr.hasPrimaryOutput, ilxtr.recordingElectrode),
      ),

    _t(i.d, 'micropipette production technique',
       (ilxtr.hasPrimaryOutput, ilxtr.microPipette)),

    _t(tech.lightMicroscopy, 'light microscopy technique',
       (hasInput, OntTerm('BIRNLEX:2112', label='Optical microscope')),  # FIXME light microscope !
       (ilxtr.detects, ilxtr.visibleLight),  # TODO photos?
       (ilxtr.hasInformationOutput, ilxtr.image),
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),
       #(ilxtr.detects, OntTerm(search='visible light', prefix='obo')),
       #(ilxtr.detects, OntTerm(search='photon', prefix='NIFSTD')),
       #(hasParticipant, OntTerm(term='visible light')),  # FIXME !!! detects vs participant ???
       synonyms=('light microscopy',)),

    _t(i.d, 'confocal microscopy technique',
       (hasInput, OntTerm('BIRNLEX:2029', label='Confocal microscope')),
       (ilxtr.isConstrainedBy, OntTerm('BIRNLEX:2258', label='Confocal imaging protocol')),
       (ilxtr.hasInformationOutput, ilxtr.image),
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),
       synonyms=('confocal microscopy',)),

    _t(tech.imaging, 'imaging technique',
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),  # the thing to be imaged
       (ilxtr.hasInformationOutput, ilxtr.image),
       def_='Imaging is the process of forming an image.',
       synonyms=('imaging',),
    ),

    _t(i.d, 'functional brain imaging',
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasPrimaryAspect, asp.boundFunctionalAspect),
                      restN(ilxtr.hasInformationOutput, ilxtr.image),
                      restN(ilxtr.hasPrimaryParticipant,
                            OntTerm('UBERON:0000955', label='brain'))),
       # FIXME this is very verbose...
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasPrimaryAspect, asp.boundFunctionalAspect),
                      restN(ilxtr.hasInformationOutput, ilxtr.image),
                      restN(ilxtr.hasPrimaryParticipant,
                            restN(partOf,
                                  OntTerm('UBERON:0000955', label='brain')))),

       #restN(ilxtr.hasPrimaryParticipant,
             #unionOf(OntTerm('UBERON:0000955', label='brain'),
                     #restN(partOf,
                           #OntTerm('UBERON:0000955', label='brain')))),
       #(ilxtr.hasPrimaryAspect, asp.anySpatioTemporalMeasure),  # FIXME and thus we see that 'functional' is a buzzword!
       #(ilxtr.hasPrimaryAspect_dAdS, ilxtr.nonZero),
       synonyms=('imaging that relies on contrast provided by differential aspects of some biological process',),
       equivalentClass=oECN),
    (i.p, ilxtr.hasTempId, OntTerm('HBP_MEM:0000007')),

    _t(i.d, 'photographic technique',
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),  # the scene
       (ilxtr.hasInformationOutput, ilxtr.photograph),
       synonyms=('photography',),
    ),

    _t(tech.positronEmissionImaging, 'positron emission imaging',
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),
       (ilxtr.detects, ilxtr.positron),
       (ilxtr.hasInformationOutput, ilxtr.image),
       (ilxtr.detects, ilxtr.positron)),

    _t(tech.opticalImaging, 'optical imaging',
       # FIXME TODO what is the difference between optical imaging and light microscopy?
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),
       (ilxtr.detects, ilxtr.visibleLight),  # owl:Class photon and hasWavelenght range ...
       (ilxtr.hasInformationOutput, ilxtr.image),
       synonyms=('light imaging', 'visible light imaging'),
    ),
    (tech.opticalImaging, ilxtr.hasTempId, OntTerm("HBP_MEM:0000013")),

    _t(i.d, 'intrinsic optical imaging',
       #tech.opticalImaging,
       #tech.contrastDetection,
       # this is a good counter example to x-ray imaging concernts
       # because it shows clearly how
       # "the reflectance to infared light by the brain"
       # that is not a thing that is a derived thing I think...
       # it is an aspect of the black box, it is not a _part_ of the back box
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),
       (ilxtr.hasProbe, ilxtr.visibleLight),  # FIXME
       (ilxtr.detects, ilxtr.visibleLight),  # FIXME
       #(ilxtr.hasPrimaryAspect, ilxtr.intrinsicSignal),  # this is a 'known phenomena'
       (ilxtr.knownDetectedPhenomena, ilxtr.intrinsicSignal),
       (ilxtr.hasInformationOutput, ilxtr.image),
       synonyms=('intrinsic signal optical imaging',),
    ),

    _t(ilxtr.xrayImaging, 'x-ray imaging',
       #tech.imaging,
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),
       (ilxtr.hasInformationOutput, ilxtr.image),
       # VS contrast in the primary aspect being the signal created by the xrays...
       # can probably expand detects in cases where there are non-aspects...
       # still not entirely sure these shouldn't all be aspects too...

       # TODO need a way to deal with the fact that what we really care about here
       # is the connection to the fact that there is some pheonmena that has
       # differential contrast to the pheonmena
       (ilxtr.detects, ilxtr.xrays),
    ),  # owl:Class photon and hasWavelenght range ...

    _t(tech.MRI_ImageProcessing, 'magnetic resonance image processing',
       # the stuff that goes on inside the scanner
       # or afterward to produce the 'classic' output data
       # this way we can create as many subclasses of contrast as we need
       (ilxtr.hasDirectInformationInput, ilxtr.image),  # TODO raw mri image
       (ilxtr.hasPrimaryAspect, asp.contrast),  # contrast to something? FIXME this seems a bit off...
       (ilxtr.hasPrimaryAspect_dAdS, ilxtr.nonZero),
       (ilxtr.hasInformationOutput, ilxtr.spatialFrequencyImageStack),  # TODO FIXME
       (ilxtr.hasSomething, i.d),
      ),

    _t(tech.MRI, 'magnetic resonance imaging',
       #tech.imaging,
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),
                      restN(hasInput, ilxtr.MRIScanner),
                      # NRM is an aspect not one of the mediators FIXME
                      restN(ilxtr.hasPrimaryAspect, ilxtr.nuclearMagneticResonance),
                      restN(hasPart, tech.MRI_ImageProcessing)),
       intersectionOf(ilxtr.technique,
                      restN(hasPart, tech.MRI)),
       # as long as the primaryAspect is subClassOf ilxtr.nuclearMagneticResonance then we are ok
       # and we won't get duplication of primary aspects
       synonyms=('MRI', 'nuclear magnetic resonance imaging'),
       equivalentClass=oECN),

    _t(tech.fMRI, 'functional magnetic resonance imaging',
       (ilxtr.isConstrainedBy, prot.fMRI),
       (hasPart, tech.MRI),
       (hasPart, tech.fMRI_ImageProcessing),
      ),

    _t(tech.fMRI_ImageProcessing, 'fMRI image processing',
       # FIXME hasPart MRI image processing?
       (ilxtr.hasDirectInformationInput, ilxtr.image),
       (ilxtr.hasInformationOutput, ilxtr.image),
       (ilxtr.hasSomething, i.d),
      ),

    olit(tech.fMRI, rdfs.comment,
         ('In contrast to previous definitions of fMRI technqiues, here we try to '
          'remain agnostic as possible about the actual phenomena that is being detected '
          'since it is still a matter of scientific exploration. The key is that the process '
          'follows a protocol that sets the proper parameters on the scanner (and uses the '
          'proper scanner).')),

    _t(tech.dwMRI, 'diffusion weighted magnetic resonance imaging',
       # FIXME the primary participant isn't really water so much as it is
       #  the water that is part of the primary participant...

       intersectionOf(ilxtr.technique,
                      restrictionN(hasPart, tech.MRI),
                      # TODO 'knownProbedPhenomena' or something similar
                      # TODO 
                      #restrictionN(ilxtr.hasPrimaryParticipant, OntTerm('CHEBI:15377', label='water')),
                      restrictionN(hasPart, tech.dwMRI_ImageProcessing)),
       intersectionOf(ilxtr.technique,
                      restrictionN(ilxtr.isConstrainedBy, prot.dwMRI)),
       synonyms=('dwMRI', 'diffusion weighted nuclear magnetic resonance imaging'),
       equivalentClass=oECN),

    _t(tech.dwMRI_ImageProcessing, 'diffusion weighted MRI image processing',
       (ilxtr.hasDirectInformationInput, ilxtr.image),
       (ilxtr.hasInformationOutput, ilxtr.image),
       (ilxtr.hasSomething, i.d),
      ),

    _t(tech.DTI, 'diffusion tensor imaging',  # FIXME very much
       intersectionOf(ilxtr.technique,
                      restrictionN(hasPart, tech.dwMRI),
                      restrictionN(hasPart, tech.DTI_ImageProcessing)),
       intersectionOf(ilxtr.technique,
                      restrictionN(ilxtr.isConstrainedBy, prot.DTI)),
           # FIXME not clear that this should be in the intersection...
           # it seems like it may make more sense to do these as unions?
           # TODO kpp kdp
       intersectionOf(ilxtr.technique,
                      restrictionN(hasInput, ilxtr.MRIScanner),
                      restrictionN(ilxtr.knownProbedPhenomena, OntTerm('CHEBI:15377', label='water')),
                      restrictionN(ilxtr.knownDetectedPhenomena, OntTerm('CHEBI:15377', label='water'))),
       synonyms=('DTI',),
       equivalentClass=oECN),

    _t(tech.DTI_ImageProcessing, 'diffusion tensor image processing',
       (ilxtr.hasDirectInformationInput, ilxtr.image),
       (ilxtr.hasInformationOutput, ilxtr.image),
       (ilxtr.hasSomething, i.d),
      ),

    _t(i.d, 'electroencephalography',
       (ilxtr.hasSomething, i.b),
       (ilxtr.hasPrimaryAspect, asp.electrical),
       (ilxtr.hasPrimaryParticipant, ilxtr.physiologicalSystem),  # FIXME uberon part of should work for this?
       (ilxtr.hasInformationOutput, ilxtr.timeSeries),
       synonyms=('EEG',)),
    (i.p, ilxtr.hasTempId, OntTerm("HBP_MEM:0000011")),

    _t(i.d, 'magnetoencephalography',
       (ilxtr.hasSomething, i.b),
       (ilxtr.hasPrimaryParticipant, OntTerm('NCBITaxon:40674', 'Mammalia')),
       (ilxtr.hasPrimaryAspect, asp.magnetic),
       (ilxtr.hasInformationOutput, ilxtr.timeSeries),
       synonyms=('MEG',)),
    (i.p, ilxtr.hasTempId, OntTerm("HBP_MEM:0000012")),
       
    # modification techniques
    _t(i.d, 'modification technique',
       # FIXME TODO
       (ilxtr.hasPrimaryAspect, asp.isClassifiedAs),
       # is classified as
       synonyms=('state creation technique', 'state induction technique')
    ),

    _t(i.d, 'activation technique',
       (ilxtr.hasProbe, ilxtr.materialEntity),  # FIXME some pheonmena... very often light...
       (ilxtr.hasPrimaryAspect, asp.boundFunctionalAspect),
       # hasPrimaryAspect some aspect of the primary participant which FOR THAT PARTICIPANT
       # has been defined as functional owl.hasSelf?
       # hasSelf asp.functional !??! no, not really what we want
       #(hasPart, ilxtr.),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.positive),
    ),

    _t(i.d, 'deactivation technique',
       (ilxtr.hasProbe, ilxtr.materialEntity),  # FIXME some pheonmena... very often light...
       (ilxtr.hasPrimaryAspect, asp.boundFunctionalAspect),  # FIXME this is more state?
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.negative),
    ),

    _t(tech.killing, 'killing technique',
       (ilxtr.hasPrimaryAspect, asp.aliveness),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.negative),
      ),

    _t(i.d, 'euthanasia technique',
       (ilxtr.hasPrimaryAspect, asp.aliveness),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.negative),
    ),

    _t(i.d, 'pharmacological technique',
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasProbe, ilxtr.molecule),  # FIXME
                      restN(hasInput, restN(hasRole, OntTerm('CHEBI:23888')))),
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasProbe, ilxtr.molecule),  # FIXME
                      restN(hasInput, restN(hasRole, OntTerm('CHEBI:38632')))),
       synonyms=('pharmacology',),
       equivalentClass=oECN),

    _t(i.d, 'ttx bath application technique',
       (hasParticipant, ilxtr.bathSolution),
       (ilxtr.hasPrimaryAspectActualized, asp.location),  # in bath?
       (ilxtr.hasPrimaryInput, OntTerm('CHEBI:9506')),
      ),

    _t(i.d, 'photoactivation technique',
       (ilxtr.hasProbe, ilxtr.photons),
       (ilxtr.hasPrimaryAspect, asp.boundFunctionalAspect),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.positive),
    ),

    _t(i.d, 'photoinactivation technique',
       (ilxtr.hasProbe, ilxtr.photons),
       (ilxtr.hasPrimaryAspect, asp.boundFunctionalAspect),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.negative),
    ),

    _t(i.d, 'photobleaching technique',
       (ilxtr.hasProbe, ilxtr.photons),
       (ilxtr.hasSomething, i.d),
    ),

    _t(i.d, 'photoconversion technique',
       (ilxtr.hasProbe, ilxtr.photons),
       (ilxtr.hasSomething, i.d),
    ),

    _t(i.d, 'molecular uncaging technique',
       # FIXME caged molecule?
       (ilxtr.hasPrimaryParticipant, OntTerm('CHEBI:25367', label='molecule')),
       (ilxtr.hasPrimaryAspect, asp.boundFunctionalAspect),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.positive),
       synonyms=('uncaging', 'uncaging technique')
    ),

    _t(i.d, 'physical modification technique',
       # FIXME for all physical things is it that the aspect is physical?
       # or that there is actually a physical change induced?
       (ilxtr.hasSomething, i.d),
    ),

    _t(i.d, 'ablation technique',
       (ilxtr.hasSomething, i.d),
    ),

    _t(i.d, 'blinding technique',
       (ilxtr.hasPrimaryAspect, asp.vision),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.negative),
    ),

    _t(i.d, 'crushing technique',
       # tissue destruction technique
       (ilxtr.hasSomething, i.d),
    ),

    _t(i.d, 'deafferenting technique',
       # tissue destruction technique
       (ilxtr.hasSomething, i.d),
    ),

    _t(i.d, 'depolarization technique',
       (ilxtr.hasPrimaryAspect, asp.voltage),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.positive),  # or is it neative (heh)
       # yes this is confusing, but cells have negative membrane potentials
    ),

    _t(i.d, 'hyperpolarization technique',
       (ilxtr.hasPrimaryAspect, asp.voltage),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.negative),
    ),

    _t(i.d, 'illumination technique',
       # as distinct from a technique for illuminating a page in a medieval text
       #tech.agnostic,  # TODO agnostic techniques try to do nothing scientific usually
       # they are purely goal driven
       #(ilxtr.phenomena, ilxtr.photons),
       (ilxtr.hasPrimaryAspectActualized, asp.lumenance),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.positive),
    ),

    _t(i.d, 'lesioning technique',
       (hasPart, tech.surgical),  # is this true
       # has intention to destory some subset of the nervous system
       (ilxtr.hasSomething, i.d),
    ),

    _t(i.d, 'sensory deprivation technique',
       (ilxtr.hasPrimaryAspect, asp.sensory),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.negative),
       (ilxtr.hasSomething, i.d),
    ),

    _t(i.d, 'transection technique',
       (hasPart, tech.surgical),
       (ilxtr.hasSomething, i.d),
    ),

    _t(i.d, 'stimulation technique',
       #(ilxtr.hasPrimaryAspect, ilxtr.physiologicalActivity),  # TODO
       (ilxtr.hasProbe, ilxtr.materialEntity),
       (ilxtr.hasPrimaryAspect, asp.biologicalActivity),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.positive),
    ),

    #oc_(None,  # FIXME this is incorrect the equivalence is asymmetric
        # and the way we are using biological activity does not imply phsyiology
        #intersectionOf(ilxtr.technique,
                       #restN(ilxtr.techniqueHasAspect, asp.biologicalActivity)),
        #oECN(intersectionOf(ilxtr.technique,
                            #restN(ilxtr.hasPrimaryParticipant, ilxtr.physiologicalSystem)))),

    _t(i.d, 'physical stimulation technique',  # FIXME another use of physical
       (ilxtr.hasSomething, i.d),
       (ilxtr.hasProbe, ilxtr.mechanicalForce),  # but is this physical?
       def_='A technique using mechanical force to enduce a state change on a system.',
       synonyms=('mechanical stimulation technique',)
    ),

    _t(i.d, 'electrical stimulation technique',
       #(ilxtr.hasProbe, asp.electrical),  # FIXME the probe should be the physical mediator
       #(ilxtr.hasProbe, ilxtr.electricalPhenomena),  # electircal field?
       (ilxtr.hasProbe, ilxtr.electricalField),  # electircal field?
       (ilxtr.hasPrimaryAspect, asp.electrical),
       (ilxtr.hasSomething, i.d),
    ),

    _t(tech.stim_Magnetic, 'magnetic stimulation technique',
       # TODO need a way to accomodate the stimulation of biological activity
       # with the stimulating phenomena
       # has intention to stimulate???
       (ilxtr.hasProbe, ilxtr.magneticField),  # FIXME TODO duality between stimulus and response...
       (ilxtr.hasPrimaryAspect, asp.magnetic),
    ),

    _t(i.d, 'transcranial magnetic stimulation technique',
       (ilxtr.hasProbe, ilxtr.magneticField),
       (ilxtr.hasPrimaryAspect, asp.magnetic),
       (ilxtr.hasSomething, i.d),
    ),

    _t(i.d, 'cortico-cortical evoked potential technique',
       (ilxtr.hasSomething, i.d),
    ),

    _t(i.d, 'microstimulation technique',
       (ilxtr.hasSomething, i.d),
    ),

    _t(tech.cutting, 'cutting technique',
       (ilxtr.hasPrimaryInput, ilxtr.cuttingTool),  # FIXME tool use...
       # TODO
      ),

    _t(tech.surgical, 'surgical technique',
       (ilxtr.hasSomething, i.d),
       # any technique that involves the destruction of some anatomical structure
       # which requires healing (if possible)
       (hasPart, tech.cutting),  # FIXME obviously too broad
       synonyms=('surgery',),),

    oc_(i.d, blankc(rdfs.label, Literal('reconstructive surgery')),  # FIXME TODO
        oec(restN(hasPart, tech.surgical),
            restN(ilxtr.hasIntention, ilxtr.toReconstruct))),

    _t(i.d, 'biopsy technique',
       (hasPart, tech.surgical),  # FIXME
       #tech.maintaining,  # things that have output tissue that don't unis something
       # this is not creating so it is not a primary output
       # if maintaining and creating are disjoin on primary inputs then have to be careful
       # about usage of hasOutput vs hasPrimaryOutput
       (ilxtr.hasPrimaryOutput, ilxtr.tissue),  # TODO
    ),

    _t(i.d, 'craniotomy technique',
       (hasPart, tech.surgical),  # FIXME
       (ilxtr.hasSomething, i.d),
       def_='Makes a hold in the cranium (head).',
    ),

    _t(i.d, 'durotomy technique',
       (hasPart, tech.surgical),  # FIXME
       (ilxtr.hasSomething, i.d),
       def_='Makes a hold in the dura.',
    ),

    _t(i.d, 'transplantation technique',
       (hasPart, tech.surgical),  # FIXME
       (ilxtr.hasSomething, i.d),
       synonyms=('transplant',)
    ),

    _t(i.d, 'implantation technique',
       (hasPart, tech.surgical),  # FIXME
       (ilxtr.hasSomething, i.d),
    ),

    _t(i.d, 'stereotaxic technique',
       (hasPart, tech.surgical),  # FIXME
       (hasInput, ilxtr.stereotax),
       (ilxtr.isConstrainedBy, ilxtr.stereotaxiCoordinateSystem),
    ),

    _t(i.d, 'behavioral technique',  # FIXME this is almost always actually some environmental manipulation
       # asp.behavioral -> 'Something measurable aspect of an organisms behavior. i.e. the things that it does.'
       (ilxtr.hasPrimaryAspect, asp.behavioral),
    ),

    _t(i.d, 'behavioral conditioning technique',
       (ilxtr.hasSomething, i.d),
       def_='A technique for producing a specific behavioral response to a set of stimuli.',  # FIXME
       synonyms=('behavioral conditioning', 'conditioning', 'conditioning technique')
    ),

    _t(i.d, 'environmental manipulation technique',
       # FIXME extremely broad, includes basically everything we do in science that is not
       # done directly to the primary subject
       (ilxtr.hasPrimaryParticipant, ilxtr.notTheSubject),
    ),

    _t(i.d, 'environmental enrichment technique',
       (ilxtr.hasSomething, i.d),
       synonyms=('behavioral enrichment technique',)
       # and here we see the duality between environment and behavior
    ),

    _t(i.d, 'dietary technique',
       #ilxtr.technique,
       # unionOf hasPart dietary technique OR hasPrimaryParticipant food
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasPrimaryInput, ilxtr.food_and_water),
                      restN(ilxtr.hasPrimaryAspectActualized, asp.allocation)),
       intersectionOf(ilxtr.technique,
                      restN(hasPart, i.p)),
       #unionOf(intersectionOf(
           #restrictionN(ilxtr.hasPrimaryParticipant, ilxtr.food_and_water),  # metabolic input
           #restrictionN(ilxtr.hasPrimaryAspect, asp.allocation)),
           #restrictionN(hasPart, i.p))
       equivalentClass=oECN),

    _t(i.d, 'dietary restriction technique',
       #(ilxtr.hasSomething, i.d),
       (hasInput, ilxtr.food_and_water),  # metabolic input
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.negative),  # FIXME may need to use has part?
       # reduction in some metabolic input
    ),

    _t(i.d, 'food deprivation technique',
       (ilxtr.hasPrimaryParticipant, ilxtr.food),
       (ilxtr.hasPrimaryAspect, asp.allocation),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.negative),
       # the above is correct, use hasPart
       # where the food amount is decresed, how to bind food to negative
       # do we have to use has part?!
       #hasPart, food
       #(hasParticipant, ilxtr.food),
       #(ilxtr.hasConstrainingAspect, asp.amount),
       #oc_(ilxtr.food,
           #asp.amount, ilxtr.negative),
       #hasAspectChangeCombinator(asp.amount, ilxtr.negative),
       synonyms=('starvation technique',
                 'food restriction technique',
                )
    ),

    _t(i.b, 'technique that makes use of food deprivation',
       (hasPart, i.p),),

    _t(i.d, 'water deprivation technique',
       (ilxtr.hasPrimaryInput, ilxtr.water),
       (ilxtr.hasPrimaryAspect, asp.allocation),
       (ilxtr.hasPrimaryAspect_dAdT, ilxtr.negative),
       synonyms=('water restriction technique',
                 'water restriction',
       )
    ),

    _t(tech.sectioning, 'sectioning technique',
       #tech.destroying,  # ok to assert here
       # easier than having say inputs are not outputs every time
       # NOTE: the thing to be sectioned is thus the primary participant
       # conservation of mass/energy implies that it is also a creating technique
       # if viewed from the persective of the sections
       # we should be able to infer that the outputs
       # from a sectioning technique were 'created'
       (hasPart, ilxtr.destroying),  # this is the proper way to make duals I think
       (ilxtr.hasPrimaryOutput, ilxtr.section),
       #(hasOutput, ilxtr.sectionsOfPrimaryInput),  # FIXME circular
       #(hasOutput,
        #oc_.full_combinator(intersectionOf(
            #ilxtr.partOfSomePrimaryInput,
            #restN(partOf,
                  #restrictionN(ilxtr.primaryParticipantIn,
                               #tech.sectioning)),
            #restrictionN(ilxtr.hasAssessedAspect,
            #restN(ilxtr.hasConstrainingAspect, asp.flatness)))),
                        #intersectionOf(
                        # hasAssessedAspect better than hasAspect?
                        # implies there is another technique...
                        # you can measure the flatness of the himallayals
                        # or of an electron if you wanted
                        # so hasAspect is maybe not the best?
       synonyms=('sectioning',)),  # FIXME

    _t(i.d, 'tissue sectioning technique',
       #tech.destroying,
       (ilxtr.hasPrimaryOutput, ilxtr.section),
       # FIXME primary participant to be destroyed? seems like there is a comflict here...
       # the cardinality rules are not catching it?
       (hasPart, ilxtr.destroying),  # TODO put tissue in here?
       (ilxtr.hasPrimaryParticipant, OntTerm('UBERON:0000479', label='tissue')),
       synonyms=('tissue sectioning',)),

    _t(i.d, 'brain sectioning technique',
       (ilxtr.hasPrimaryOutput, ilxtr.section),
       (hasPart, ilxtr.destroying),
       (ilxtr.hasPrimaryParticipant, OntTerm('UBERON:0000955', label='brain')),
       synonyms=('brain sectioning',)),

    _t(i.d, 'block face sectioning technique',
       # SBEM vs block face for gross anatomical registration
       tech.sectioning,
       (ilxtr.hasSomething, i.d),
    ),

    _t(i.d, 'microtomy technique',
       (hasInput, ilxtr.microtome),
       (ilxtr.hasPrimaryOutput, ilxtr.thinSections),  # this prevents issues with microtome based warfare techniques
       synonyms=('microtomy',)
    ),

    _t(i.d, 'ultramicrotomy technique',
       (hasInput, ilxtr.ultramicrotome),
       (ilxtr.hasPrimaryOutput, ilxtr.veryThinSection),  # FIXME > 1?
       synonyms=('ultramicrotomy',)
    ),

    _t(i.d, 'array tomographic technique',
       (hasPart, tech.lightMicroscopy),
       #(hasParticipant, ilxtr.microscope),  # FIXME more precisely?
       (hasPart, tech.tomography),
       #(ilxtr.hasInformationInput, ilxtr.image),
       #(ilxtr.hasInformationOutput, ilxtr.image),
       #(ilxtr.isConstrainedBy, ilxtr.radonTransform),
       synonyms=('array tomography', 'array tomography technique')
    ),

    _t(tech.electronMicroscopy, 'electron microscopy technique',
       (hasInput, OntTerm('BIRNLEX:2041', label='Electron microscope', synonyms=[])),
       (ilxtr.detects, OntTerm('CHEBI:10545', label='electron')),  # FIXME chebi ok in this context?
       (ilxtr.hasInformationOutput, ilxtr.image),
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),
       # hasProbe ilxtr.electron and some focusing elements and detects ilxtr.electron
       synonyms=('electron microscopy',)),
    (tech.electronMicroscopy, oboInOwl.hasDbXref, OntTerm('NLX:82779')),  # ICK from assay branch which conflates measurement :/

    _t(i.d, 'electron tomography technique',
       (hasPart, tech.electronMicroscopy),
       (hasPart, tech.tomography),
      ),

    _t(i.d, 'correlative light-electron microscopy technique',
       #(hasInput, OntTerm('BIRNLEX:2041', label='Electron microscope')),
       # this works extremely well because the information outputs propagate nicely
       (hasPart, tech.lightMicroscopy),
       (hasPart, tech.electronMicroscopy),
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),
       (ilxtr.hasInformationOutput, ilxtr.image),
       synonyms=('correlative light-electron microscopy',)
    ),

    _t(i.d, 'serial blockface electron microscopy technique',
       (hasPart, tech.electronMicroscopy),
       (hasPart, tech.ultramicrotomy),
       (hasInput, ilxtr.serialBlockfaceUltraMicrotome),
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),
       #(hasParticipant, OntTerm('BIRNLEX:2041', label='Electron microscope')),
       #(hasParticipant, ilxtr.ultramicrotome),
       synonyms=('serial blockface electron microscopy',)
    ),

    _t(i.d, 'super resolution microscopy technique',
       #(hasParticipant, OntTerm('BIRNLEX:2106', label='Microscope', synonyms=[])),  # TODO more
       (hasPart, tech.lightMicroscopy),  # FIXME special restriction on the properties of the scope?
       (ilxtr.isConstrainedBy, ilxtr.superResolutionAlgorithem),
       (ilxtr.hasPrimaryParticipant, ilxtr.materialEntity),
       synonyms=('super resolution microscopy',)
    ),

    _t(i.d, 'northern blotting technique',
       (hasPart, tech.electrophoresis),
       # fixme knownDetectedPhenomena?
       (ilxtr.hasPrimaryParticipant, OntTerm('CHEBI:33697', label='RNA')),
       (ilxtr.hasProbe, ilxtr.hybridizationProbe),  # has part some probe addition?
       (ilxtr.hasPrimaryAspect, asp.sequence),
       synonyms=('northern blot',)
    ),
    _t(i.d, 'Southern blotting technique',
       (hasPart, tech.electrophoresis),
       (ilxtr.hasPrimaryParticipant, OntTerm('CHEBI:16991', term='DNA')),
       (ilxtr.hasProbe, ilxtr.hybridizationProbe),
       (ilxtr.hasPrimaryAspect, asp.sequence),
       synonyms=('Southern blot',)
    ),
    _t(i.d, 'western blotting technique',
       # FIXME dissociated
       (hasPart, tech.electrophoresis),
       (ilxtr.hasPrimaryParticipant, OntTerm('PR:000000001', label='protein')),  # at least one
       (ilxtr.hasProbe, OntTerm('BIRNLEX:2110', label='Antibody')),
       # FIXME is this really a probes in the way that say, an xray is a probe? I think yes
       # they create the contrast that will later be detected
       (ilxtr.hasPrimaryAspect, asp.epitopePresent),  # in sufficient quantity?
       # epitope is in theory more physical, but since we don't understand the mechanism
       # we don't really know what the antibody is 'measuring' about the epitope
       # to deal with this we make it a binary aspect and use the intentional nature of
       # has primary aspect to deal with false negatives
       # false negative is a failure with respect to a binary aspect intention caused by
       # a report of false when the omega measure implementation of the aspect on the
       # black box evaluates to true
       synonyms=('wester blot',
                 'protein immunoblot',)),
    (i.p, ilxtr.hasTempId, OntTerm("HBP_MEM:0000112")),

    _t(i.d, 'intracellular electrophysiology technique',
       (ilxtr.hasPrimaryParticipant, OntTerm('GO:0005622', label='intracellular')),
       # FIXME in a physiological (not dead) system
       (ilxtr.hasPrimaryAspect, asp.electrical),
       #(ilxtr.hasPrimaryParticipant, OntTerm('SAO:1289190043', label='Cellular Space')),  # TODO add intracellular as synonym
    ),

    _t(tech.extracellularEphys, 'extracellular electrophysiology technique',
       # or is it hasPrimaryParticipant hasPart some extracellularSpace? (no)
       (ilxtr.hasPrimaryParticipant, OntTerm('GO:0005615', label='extracellular space')),
       (ilxtr.hasPrimaryAspect, asp.electrical),
    ),
    (tech.extracellularEphys, ilxtr.hasTempId, OntTerm('HBP_MEM:0000015')),

    _t(tech.singleElectrodeEphys, 'single electrode extracellular electrophysiology technique',
       # FIXME extracellular space that is part of some other participant... how to convey this...
       (ilxtr.hasPrimaryAspect, asp.electrical),
       (ilxtr.hasPrimaryParticipant, OntTerm('GO:0005615', label='extracellular space')),
       (hasInput, ilxtr.singleElectrode),  # cardinality 1?
       synonyms=('single extracellular electrode technique',)),
       (tech.singleElectrodeEphys, ilxtr.hasTempId, OntTerm('HBP_MEM:0000019')),

    _t(tech.sharpElectrodeEphys, 'sharp intracellular electrode technique',
       (ilxtr.hasPrimaryAspect, asp.electrical),
       (ilxtr.hasPrimaryParticipant, OntTerm('GO:0005622', label='intracellular')),
       (hasInput, ilxtr.sharpElectrode),
       synonyms=('sharp electrode technique',)),
       (tech.sharpElectrodeEphys, ilxtr.hasTempId, OntTerm('HBP_MEM:0000023')),

    _t(tech.sharpElectrodeTechnique, 'sharp electrode technique',
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasPrimaryParticipant, ilxtr.cell),
                      restN(hasInput, ilxtr.sharpMicroPipette)),
       equivalentClass=oECN),

    _t(tech.cellPatching, 'cell patching technique',
       intersectionOf(ilxtr.technique,
                      restN(ilxtr.hasPrimaryParticipant,
                            unionOf(ilxtr.cellMembrane,
                                    restN(partOf, ilxtr.cellMembrane))),
                      restN(hasInput, ilxtr.patchPipette)),
       equivalentClass=oECN),
    oc_(tech.cellPatching, restriction(hasInput, ilxtr.inVitroEphysRig)),

    _t(tech.patchClamp, 'patch clamp technique',
       intersectionOf(ilxtr.technique,
                      restN(hasPart, tech.cellPatching),
                      restN(ilxtr.hasPrimaryAspect, asp.electrical),
                      restN(hasInput, ilxtr.patchElectrode)),
       intersectionOf(ilxtr.technique,
                      restN(hasPart, tech.patchClamp)),
       equivalentClass=oECN),
       (tech.patchClamp, ilxtr.hasTempId, OntTerm('HBP_MEM:0000017')),

    _t(i.d, 'cell attached patch technique',
       (ilxtr.hasPrimaryParticipant, ilxtr.cellMembrane),
       (hasInput, ilxtr.patchPipette),
       (hasParticipant, OntTerm('GO:0005622', label='intracellular')),
       # cell attached configuration?
       (ilxtr.hasSomething, i.b),
    ),
       (i.p, ilxtr.hasTempId, OntTerm('HBP_MEM:0000029')),

    _t(i.d, 'inside out patch technique',
       (ilxtr.hasPrimaryParticipant, ilxtr.cellMembrane),
       (hasInput, ilxtr.patchPipette),
       (ilxtr.hasSomething, i.b),
    ),
       (i.p, ilxtr.hasTempId, OntTerm('HBP_MEM:0000028')),

    _t(i.d, 'loose patch technique',
       (ilxtr.hasPrimaryParticipant, ilxtr.cellMembrane),
       (hasInput, ilxtr.patchPipette),
       (ilxtr.hasSomething, i.b),
    ),
       (i.p, ilxtr.hasTempId, OntTerm('HBP_MEM:0000024')),

    _t(i.d, 'outside out patch technique',
       (ilxtr.hasPrimaryParticipant, ilxtr.cellMembrane),
       (hasInput, ilxtr.patchPipette),
       (ilxtr.hasSomething, i.b),
    ),
       (i.p, ilxtr.hasTempId, OntTerm('HBP_MEM:0000026')),

    _t(i.d, 'perforated patch technique',
       (ilxtr.hasPrimaryParticipant, ilxtr.cellMembrane),
       (hasInput, ilxtr.patchPipette),
       (ilxtr.hasSomething, i.b),
    ),
       (i.p, ilxtr.hasTempId, OntTerm('HBP_MEM:0000025')),

    _t(tech.wholeCellPatch, 'whole cell patch technique',
       (ilxtr.hasPrimaryParticipant, ilxtr.cellMembrane),
       (hasParticipant, OntTerm('GO:0005622', label='intracellular')),
       (hasInput, ilxtr.patchPipette),
       (ilxtr.hasSomething, i.b),
    ),
       (i.p, ilxtr.hasTempId, OntTerm('HBP_MEM:0000027')),

    _t(tech.eClamp, 'electrical clamping technique',
       (hasInput, ilxtr.recordingElectrode),
       (ilxtr.hasPrimaryAspect, asp.electrical),
       (ilxtr.hasConstrainingAspect, asp.electrical),
       # FIXME should be different aspects??
      ),
    _t(i.d, 'current clamp technique',
       (hasInput, ilxtr.recordingElectrode),
       (ilxtr.hasPrimaryAspect, asp.voltage),
       (ilxtr.hasConstrainingAspect, asp.current),
       # TODO hasPrimaryAspectActualized, asp.current
       # TODO isConstrainedBy V=IR
    ),
       (i.p, ilxtr.hasTempId, OntTerm('HBP_MEM:0000204')),

    _t(tech.vClamp, 'voltage clamp technique',
       # voltage really only works in patch configuration
       # need to be able to inject enough current
       (hasInput, ilxtr.recordingElectrode),
       (ilxtr.hasPrimaryAspect, asp.current),
       (ilxtr.hasConstrainingAspect, asp.voltage),
       # TODO hasPrimaryAspectActualized, asp.current
    ),
       (i.p, ilxtr.hasTempId, OntTerm('HBP_MEM:0000203')),

    _t(i.d, 'dynamic clamp technique',
       (hasPart, tech.vClamp),
       (hasInput, ilxtr.dynamicClampAmplifier),
      ),

    _t(i.d, 'whole cell patch clamp technique',
       (hasPart, tech.eClamp),
       (hasPart, tech.wholeCellPatch),
       synonyms=('whole cell patch clamp',),
      ),

    _t(i.d, 'cell filling technique',
       (hasPart, tech.cellPatching),
       #(hasPart, tech.contrastEnhancement),  #not the right way to do this?
       #(hasParticipant, OntTerm('GO:0005622', label='intracellular')),
       (hasInput, ilxtr.contrastAgent),  # FIXME ...
      ),

    _t(i.d, ' blank technique',
       (ilxtr.hasSomething, i.d),
    ),
)

def ect():  # FIXME not used supposed to make dAdT zero equi to value hasValue 0
    b = rdflib.BNode()

    r = tuple(restG(None, POC(owl.onProperty, ilxtr.hasPrimaryAspect_dAdT),
                    POC(owl.someValuesFrom,
                        rdflib.Literal(1, datatype=rdflib.XSD.nonNegativeInteger)),
                    POC(owl.onClass, ilxtr.changeType)),
              restG(None, POC(owl.onProperty, ilxtr.hasPrimaryAspect_dAdT),
                    POC(owl.maxQualifiedCardinality,
                        rdflib.Literal(1, datatype=rdflib.XSD.nonNegativeInteger)),
                    POC(owl.onClass, ilxtr.changeType)))

    ax = (b, rdf.type, owl.Axiom)
    ecr = (b, owl.equivalentClass, r[0][0])

    return r1 + r2 + ax + ecr

#triples += ect()
"""
_t(tech.fMRI, 'functional magnetic resonance imaging',
   # AAAAAAA how to deal with
   # "change in nuclear magnetic resonance of iron molecules as a function of time and their bound oxygen"
   # "BOLD" blood oxygenation level dependent contrast is something different...
   #ilxtr.NMR_of_iron_in_the_blood  # ICK
   #(hasPrimaryParticipant, ilxtr.???)
   #(hasPart, tech.MRI),  # FIXME how to deal with this...
   #(hasPart, tech.bloodOxygenLevel),
   #(ilxtr.hasPrimaryAspect, ilxtr.nuclearMagneticResonance),
   tech.MRI,  # FIXME vs respeccing everything?
   #(ilxtr.hasPrimaryParticipantSubeset, ilxtr.haemoglobin)
   #(ilxtr.hasPrimaryParticipantPart, ilxtr.haemoglobin)
   (ilxtr.hasPrimaryParticipant, ilxtr.haemoglobin),
   (ilxtr.hasPrimaryParticipantSubsetRule, ilxtr.hasBoundOxygen),  # FIXME not quite right still?
   synonyms=('fMRI', 'functional nuclear magnetic resonance imaging'),),
olit(tech.fMRI, rdfs.comment,
     ('Note that this deals explicitly only with the image acquistion portion of fMRI. '
      'Other parts of the full process and techniques in an fMRI study should be modelled separately. '
      'They can be tied to fMRI using hasPart: or hasPriorTechnique something similar.')),  # TODO
(tech.fMRI, ilxtr.hasTempId, OntTerm("HBP_MEM:0000008")),
"""
"""
_t(tech.sequencing, 'sequencing technique',
   # hasParticipant molecule or chemical?
   (ilxtr.hasPrimaryParticipant, ilxtr.thingWithSequence),  # peptide nucleotie sacharide
   # can't use hasParticipant because then it would caputre peptide synthesis or oligo synthesis
   (ilxtr.hasPrimaryAspect, asp.sequence),  # nucleic and peptidergic, and chemical etc.
   (ilxtr.hasInformationOutput, ilxtr.informationArtifact),  # note use of artifact
    ),
"""
"""
_t(tech.rnaSeq, 'RNAseq',
   (ilxtr.knownDetectedPhenomena, OntTerm('CHEBI:33697', label='RNA')),
   (ilxtr.hasPrimaryAspect, asp.sequence),
   (ilxtr.hasInformationOutput, ilxtr.informationArtifact),  # note use of artifact
   synonyms=('RNA-seq',)
  ),

"""


methods = simpleOnt(filename=filename,
                    prefixes=prefixes,
                    imports=imports,
                    triples=triples,
                    comment=comment,
                    _repo=_repo)

[methods.graph.add((o2, rdfs.subClassOf, TEMP.urg))
 for s1, p1, o1 in methods.graph if
 p1 == owl.onProperty and
 o1 == ilxtr.hasSomething
 for p2, o2 in methods.graph[s1:] if
 p2 == owl.someValuesFrom]

methods._graph.add_namespace('asp', str(asp))
methods._graph.add_namespace('ilxtr', str(ilxtr))  # FIXME why is this now showing up...
methods._graph.add_namespace('prot', str(prot))
methods._graph.add_namespace('tech', str(tech))
methods._graph.add_namespace('HBP_MEM', OntCuries['HBP_MEM'])

from collections import defaultdict
data = defaultdict(set)
for t in methods.graph:
    for e in t:
        if isinstance(e, URIRef) and 'tgbugs' in e:
            prefix, suffix = methods._graph.qname(e).split(':')
            data[prefix].add(suffix)

intersection = defaultdict(set)
for ki, vi in data.items():
    for kj, vj in data.items():
        if ki == kj:
            continue

        intersection[ki,kj].update(vi & vj)

#assert not any(intersection.values()), f'duplicate namespace issue {intersection!r}'
#from IPython import embed
#embed()

methods._graph.write()


def halp():
    import rdflib
    from IPython import embed
    trips = sorted(flattenTriples(triples))
    graph = rdflib.Graph()
    *(graph.add(t) for t in trips),
    *(print(tuple(qname(e) if not isinstance(e, rdflib.BNode) else e[:5] for e in t)) for t in trips),
    embed()
    return trips
#trips = halp()

def expand(_makeGraph, *graphs, debug=False):
    import rdflib
    import RDFClosure as rdfc
    graph = rdflib.Graph()
    for graph_ in graphs:
        [graph.bind(k, v) for k, v in graph_.namespaces()]
        [graph.add(t) for t in graph_]
    g = _makeGraph.__class__('', graph=graph)
    g.filename = _makeGraph.filename
    # other options are
    # OWLRL_Semantis RDFS_OWLRL_Semantics but both cuase trouble
    # all of these are SUPER slow to run on cpython, very much suggest pypy3
    #rdfc.DeductiveClosure(rdfc.OWLRL_Extension_Trimming).expand(graph)  # monumentally slow even on pypy3
    #rdfc.DeductiveClosure(rdfc.OWLRL_Extension).expand(graph)
    eg = rdflib.Graph()
    [eg.add(t) for t in graph_]
    closure = rdfc.OWLRL_Semantics
    rdfc.DeductiveClosure(closure).expand(eg)
    [not graph.add((s, rdfs.subClassOf, o))
     and [graph.add(t) for t in annotation.serialize((s, rdfs.subClassOf, o),
                                                     ilxtr.isDefinedBy, closure.__name__)]
     for s, o in eg.subject_objects(rdfs.subClassOf)
     if s != o and  # prevent cluttering the graph
     #o not in [to for o_ in eg.objects(s, rdfs.subClassOf)  # not working correctly
               #for to in eg.objects(o_) if o_ != o] and
     not isinstance(s, rdflib.BNode) and
     not isinstance(o, rdflib.BNode) and
     'interlex' in s and 'interlex' in o]
    #g.write()
    displayGraph(graph, debug=debug)

def forComparison():

    obo, *_ = makeNamespaces('obo')
    filename = 'methods-external-test-bridge'
    imports = (obo['ero.owl'],
               #URIRef('https://www.eagle-i.net/ero/latest/ero.owl'),
               obo['obi.owl'],
               obo['ro.owl'],
               URIRef('http://www.ebi.ac.uk/efo/efo.owl'),
               URIRef('http://purl.org/incf/ontology/ExperimentalNeurophysiology/oen_term.owl'),
              )  # CNO still uses bfo1.1
    comment = 'Bridge for querying against established methods related ontologies.'
    _repo = True
    debug = False

    triples = tuple()

    methods_helper = simpleOnt(filename=filename,
                               #prefixes=prefixes,
                               imports=imports,
                               triples=triples,
                               comment=comment,
                               _repo=_repo)

def main():
    forComparison()
    displayGraph(methods.graph, debug=debug)
    mc = methods.graph.__class__()
    #mc.add(t) for t in methods_core.graph if t[0] not in
    expand(methods_core._graph, methods_core.graph)#, methods_core.graph)  # FIXME including core breaks everying?
    expand(methods._graph, methods.graph)#, methods_core.graph)  # FIXME including core breaks everying?

if __name__ == '__main__':
    #main()
    pass
