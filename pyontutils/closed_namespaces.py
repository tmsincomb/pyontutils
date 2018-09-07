#!/usr/bin/env python3

from rdflib import Graph, URIRef, RDF as rdf, RDFS as rdfs
from rdflib.plugin import PluginException
from rdflib.namespace import ClosedNamespace

__all__ = [
    'dc',
    'dcterms',
    'oboInOwl',
    'owl',
    'prov',
    'rdf',
    'rdfs',
    'skos',
]

###

dc = ClosedNamespace(
    uri=URIRef('http://purl.org/dc/elements/1.1/'),
    terms=['contributor',
           'coverage',
           'creator',
           'date',
           'description',
           'format',
           'identifier',
           'language',
           'publisher',
           'relation',
           'rights',
           'source',
           'subject',
           'title',
           'type']
)

dcterms = ClosedNamespace(
    uri=URIRef('http://purl.org/dc/terms/'),
    terms=['Agent',
           'AgentClass',
           'BibliographicResource',
           'Box',
           'DCMIType',
           'DDC',
           'FileFormat',
           'Frequency',
           'IMT',
           'ISO3166',
           'ISO639-2',
           'ISO639-3',
           'Jurisdiction',
           'LCC',
           'LCSH',
           'LicenseDocument',
           'LinguisticSystem',
           'Location',
           'LocationPeriodOrJurisdiction',
           'MESH',
           'MediaType',
           'MediaTypeOrExtent',
           'MethodOfAccrual',
           'MethodOfInstruction',
           'NLM',
           'Period',
           'PeriodOfTime',
           'PhysicalMedium',
           'PhysicalResource',
           'Point',
           'Policy',
           'ProvenanceStatement',
           'RFC1766',
           'RFC3066',
           'RFC4646',
           'RFC5646',
           'RightsStatement',
           'SizeOrDuration',
           'Standard',
           'TGN',
           'UDC',
           'URI',
           'W3CDTF',
           'abstract',
           'accessRights',
           'accrualMethod',
           'accrualPeriodicity',
           'accrualPolicy',
           'alternative',
           'audience',
           'available',
           'bibliographicCitation',
           'conformsTo',
           'contributor',
           'coverage',
           'created',
           'creator',
           'date',
           'dateAccepted',
           'dateCopyrighted',
           'dateSubmitted',
           'description',
           'educationLevel',
           'extent',
           'format',
           'hasFormat',
           'hasPart',
           'hasVersion',
           'identifier',
           'instructionalMethod',
           'isFormatOf',
           'isPartOf',
           'isReferencedBy',
           'isReplacedBy',
           'isRequiredBy',
           'isVersionOf',
           'issued',
           'language',
           'license',
           'mediator',
           'medium',
           'modified',
           'provenance',
           'publisher',
           'references',
           'relation',
           'replaces',
           'requires',
           'rights',
           'rightsHolder',
           'source',
           'spatial',
           'subject',
           'tableOfContents',
           'temporal',
           'title',
           'type',
           'valid']
)

oboInOwl = ClosedNamespace(
    uri=URIRef('http://www.geneontology.org/formats/oboInOwl#'),
    terms=['DbXref',
           'Definition',
           'ObsoleteClass',
           'ObsoleteProperty',
           'Subset',
           'SubsetProperty',
           'Synonym',
           'SynonymType',
           'SynonymTypeProperty',
           'consider',
           'hasAlternativeId',
           'hasBroadSynonym',
           'hasDate',
           'hasDbXref',
           'hasDefaultNamespace',
           'hasDefinition',
           'hasExactSynonym',
           'hasNarrowSynonym',
           'hasOBONamespace',
           'hasRelatedSynonym',
           'hasSubset',
           'hasSynonym',
           'hasSynonymType',
           'hasURI',
           'hasVersion',
           'inSubset',
           'isCyclic',
           'replacedBy',
           'savedBy']
)

owl = ClosedNamespace(
    uri=URIRef('http://www.w3.org/2002/07/owl#'),
    terms=['AllDifferent',
           'AllDisjointClasses',
           'AllDisjointProperties',
           'Annotation',
           'AnnotationProperty',
           'AsymmetricProperty',
           'Axiom',
           'Class',
           'DataRange',
           'DatatypeProperty',
           'DeprecatedClass',
           'DeprecatedProperty',
           'FunctionalProperty',
           'InverseFunctionalProperty',
           'IrreflexiveProperty',
           'NamedIndividual',
           'NegativePropertyAssertion',
           'Nothing',
           'ObjectProperty',
           'Ontology',
           'OntologyProperty',
           'ReflexiveProperty',
           'Restriction',
           'SymmetricProperty',
           'Thing',
           'TransitiveProperty',
           'allValuesFrom',
           'annotatedProperty',
           'annotatedSource',
           'annotatedTarget',
           'assertionProperty',
           'backwardCompatibleWith',
           'bottomDataProperty',
           'bottomObjectProperty',
           'cardinality',
           'complementOf',
           'datatypeComplementOf',
           'deprecated',
           'differentFrom',
           'disjointUnionOf',
           'disjointWith',
           'distinctMembers',
           'equivalentClass',
           'equivalentProperty',
           'hasKey',
           'hasSelf',
           'hasValue',
           'imports',
           'incompatibleWith',
           'intersectionOf',
           'inverseOf',
           'maxCardinality',
           'maxQualifiedCardinality',
           'members',
           'minCardinality',
           'minQualifiedCardinality',
           'onClass',
           'onDataRange',
           'onDatatype',
           'onProperties',
           'onProperty',
           'oneOf',
           'priorVersion',
           'propertyChainAxiom',
           'propertyDisjointWith',
           'qualifiedCardinality',
           'sameAs',
           'someValuesFrom',
           'sourceIndividual',
           'targetIndividual',
           'targetValue',
           'topDataProperty',
           'topObjectProperty',
           'unionOf',
           'versionIRI',
           'versionInfo',
           'withRestrictions']
)

prov = ClosedNamespace(
    uri=URIRef('http://www.w3.org/ns/prov#'),
    terms=['Accept',
           'Activity',
           'ActivityInfluence',
           'Agent',
           'AgentInfluence',
           'Association',
           'Attribution',
           'Bundle',
           'Collection',
           'Communication',
           'Contribute',
           'Contributor',
           'Copyright',
           'Create',
           'Creator',
           'Delegation',
           'Derivation',
           'Dictionary',
           'DirectQueryService',
           'EmptyCollection',
           'EmptyDictionary',
           'End',
           'Entity',
           'EntityInfluence',
           'Generation',
           'Influence',
           'Insertion',
           'InstantaneousEvent',
           'Invalidation',
           'KeyEntityPair',
           'Location',
           'Modify',
           'Organization',
           'Person',
           'Plan',
           'PrimarySource',
           'Publish',
           'Publisher',
           'Quotation',
           'Removal',
           'Replace',
           'Revision',
           'RightsAssignment',
           'RightsHolder',
           'Role',
           'ServiceDescription',
           'SoftwareAgent',
           'Start',
           'Submit',
           'Usage',
           'actedOnBehalfOf',
           'activity',
           'activityOfInfluence',
           'agent',
           'agentOfInfluence',
           'alternateOf',
           'aq',
           'asInBundle',
           'atLocation',
           'atTime',
           'category',
           'component',
           'constraints',
           'contributed',
           'definition',
           'derivedByInsertionFrom',
           'derivedByRemovalFrom',
           'describesService',
           'dictionary',
           'dm',
           'editorialNote',
           'editorsDefinition',
           'ended',
           'endedAtTime',
           'entity',
           'entityOfInfluence',
           'generalizationOf',
           'generated',
           'generatedAsDerivation',
           'generatedAtTime',
           'hadActivity',
           'hadDelegate',
           'hadDerivation',
           'hadDictionaryMember',
           'hadGeneration',
           'hadInfluence',
           'hadMember',
           'hadPlan',
           'hadPrimarySource',
           'hadRevision',
           'hadRole',
           'hadUsage',
           'has_anchor',
           'has_provenance',
           'has_query_service',
           'influenced',
           'influencer',
           'informed',
           'insertedKeyEntityPair',
           'invalidated',
           'invalidatedAtTime',
           'inverse',
           'locationOf',
           'mentionOf',
           'n',
           'order',
           'pairEntity',
           'pairKey',
           'pingback',
           'provenanceUriTemplate',
           'qualifiedAssociation',
           'qualifiedAssociationOf',
           'qualifiedAttribution',
           'qualifiedAttributionOf',
           'qualifiedCommunication',
           'qualifiedCommunicationOf',
           'qualifiedDelegation',
           'qualifiedDelegationOf',
           'qualifiedDerivation',
           'qualifiedDerivationOf',
           'qualifiedEnd',
           'qualifiedEndOf',
           'qualifiedForm',
           'qualifiedGeneration',
           'qualifiedGenerationOf',
           'qualifiedInfluence',
           'qualifiedInfluenceOf',
           'qualifiedInsertion',
           'qualifiedInvalidation',
           'qualifiedInvalidationOf',
           'qualifiedPrimarySource',
           'qualifiedQuotation',
           'qualifiedQuotationOf',
           'qualifiedRemoval',
           'qualifiedRevision',
           'qualifiedSourceOf',
           'qualifiedStart',
           'qualifiedStartOf',
           'qualifiedUsage',
           'qualifiedUsingActivity',
           'quotedAs',
           'removedKey',
           'revisedEntity',
           'sharesDefinitionWith',
           'specializationOf',
           'started',
           'startedAtTime',
           'todo',
           'unqualifiedForm',
           'used',
           'value',
           'wasActivityOfInfluence',
           'wasAssociateFor',
           'wasAssociatedWith',
           'wasAttributedTo',
           'wasDerivedFrom',
           'wasEndedBy',
           'wasGeneratedBy',
           'wasInfluencedBy',
           'wasInformedBy',
           'wasInvalidatedBy',
           'wasMemberOf',
           'wasPlanOf',
           'wasPrimarySourceOf',
           'wasQuotedFrom',
           'wasRevisionOf',
           'wasRoleIn',
           'wasStartedBy',
           'wasUsedBy',
           'wasUsedInDerivation']
)

skos = ClosedNamespace(
    uri=URIRef('http://www.w3.org/2004/02/skos/core#'),
    terms=['Collection',
           'Concept',
           'ConceptScheme',
           'OrderedCollection',
           'altLabel',
           'broadMatch',
           'broader',
           'broaderTransitive',
           'changeNote',
           'closeMatch',
           'definition',
           'editorialNote',
           'exactMatch',
           'example',
           'hasTopConcept',
           'hiddenLabel',
           'historyNote',
           'inScheme',
           'mappingRelation',
           'member',
           'memberList',
           'narrowMatch',
           'narrower',
           'narrowerTransitive',
           'notation',
           'note',
           'prefLabel',
           'related',
           'relatedMatch',
           'scopeNote',
           'semanticRelation',
           'topConceptOf']
)

###

def main():
    # use to populate terms
    uris = {
        'oboInOwl':'http://www.geneontology.org/formats/oboInOwl#',
        'owl':'http://www.w3.org/2002/07/owl#',
        'skos':'http://www.w3.org/2004/02/skos/core#',
        'dc':'http://purl.org/dc/elements/1.1/',
        'dcterms':'http://purl.org/dc/terms/',
        'prov':'http://www.w3.org/ns/prov#',
    }
    tw = 4
    tab = ' ' * tw
    ind = ' ' * (tw + len('terms=['))
    functions = ''
    for name, uri in sorted(uris.items()):
        try:
            g = Graph().parse(uri.rstrip('#'))
        except PluginException:
            g = Graph().parse(uri.rstrip('#') + '.owl')
        sep = uri[-1]
        globals().update(locals())
        terms = sorted(set(s.rsplit(sep, 1)[-1]
                           for s in g.subjects()
                           if uri in s and uri != s.toPython() and sep in s))
        block = ('\n'
                 '{name} = ClosedNamespace(\n'
                 "{tab}uri=URIRef('{uri}'),\n"
                 '{tab}' + "terms=['{t}',\n".format(t=terms[0]) + ''
                 '{ind}' + ',\n{ind}'.join("'{t}'".format(t=t)  # watch out for order of operations issues
                                           for t in terms[1:]) + ']\n'
                 ')\n')
        function = block.format(name=name,
                                uri=uri,
                                tab=tab,
                                ind=ind)
        functions += function

    functions += '\n'

    with open(__file__, 'rt') as f:
        text = f.read()

    sep = '###\n'
    start, mid, end = text.split(sep)
    code = sep.join((start, functions, end))
    with open(__file__, 'wt') as f:
        f.write(code)

if __name__ == '__main__':
    main()
