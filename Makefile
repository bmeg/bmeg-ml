

all: ml-code phenotype-code ga4gh-code

ml-code:
	cd ml-schema && \
	protoc \
	-I . \
	--python_out=../ \
	bmeg/ml_schema.proto

	
phenotype-code:
	cd phenotype-schema && \
	protoc \
	-I . -I ../ga4gh-schemas/src/main/proto/ \
	--python_out=../ \
	bmeg/phenotype.proto

	
ga4gh-code:
	cd ga4gh-schemas/src/main/proto && \
	protoc \
	-I. \
	--python_out=../../../../ \
	ga4gh/genotype_phenotype.proto 	ga4gh/common.proto ga4gh/bio_metadata.proto ga4gh/metadata.proto \
	ga4gh/variants.proto
