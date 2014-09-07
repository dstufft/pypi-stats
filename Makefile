.PHONY: mostlyclean clean all serve

all: output/line-py-versions.png \
	 output/stacked-py-pct.png

serve:
	mkdir -p output
	twistd -n web --path output/

mostlyclean:
	rm -f data/*.json
	rm -rf output

clean:
	rm -rf data
	rm -rf output

data/data.pkl:
	bin/load.py

data/%.json: data/data.pkl
	bin/json-$*.py

output/%.png: data/%.json
	mkdir -p output
	node_modules/.bin/vg2png data/$*.json > output/$*.png
