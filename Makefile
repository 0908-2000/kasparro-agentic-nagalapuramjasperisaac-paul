.PHONY: run test
run:
	python run_pipeline.py --input data/product_fixture.json --out_dir output
test:
	pytest -q
