#!/usr/bin/env python


import sys
import json
from bmeg.ml_schema_pb2 import Model
from bmeg.phenotype_pb2 import Predictor
from ga4gh.genotype_phenotype_pb2 import PhenotypeInstance
from ga4gh.common_pb2 import OntologyTerm
from google.protobuf import json_format


def message_to_json(message):
    msg = json.dumps(json_format.MessageToDict(message))
    return msg

PUBCHEM_MAP = {}
with open("drugs.table") as handle:
    for line in handle:
        row = line.rstrip().split("\t")
        PUBCHEM_MAP[row[0]] = row[1]

predictor_out = open("predictors.json", "w")
model_out = open("models.json", "w")

with open(sys.argv[1]) as handle:
    for line in handle:
        s = json.loads(line)

        model_id = "ucsc.edu/james-prediction/%s" % (s['name'])
        pred = Predictor()
        pred.phenotype.type.term_id = "GO:0008219"
        pred.model_id = model_id

        for i in s["signatureForEdges"]:
            drugs = i.replace("drug:", "").split(" (")[0]
            for drug in drugs.split(":"):
                e = pred.environmental_contexts.add()
                e.id = "pubchem.ncbi.nlm.nih.gov/compound/%s" % (PUBCHEM_MAP[drug])
        predictor_out.write( message_to_json(pred) + "\n" )

        model = Model()
        model.id = model_id
        model.structure.linear.intercept = s["intercept"]

        for k, v in s['coefficients'].items():
            model.structure.linear.coeff[k] = v
        model_out.write( message_to_json(model) + "\n" )

predictor_out.close()
model_out.close()
