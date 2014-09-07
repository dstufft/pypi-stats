.PHONY: mostlyclean clean all all-data serve

.SECONDARY:

all: all-data \
	 output/area-total-downloads.png \
	 output/line-py-versions.png \
	 output/stacked-py-pct.png \
	 output/stacked-py3-pct.png

all-data: data/python-totals.pkl \
		  data/python-versions.pkl

serve:
	mkdir -p output
	twistd -n web --path output/

mostlyclean:
	rm -f data/*.json
	rm -rf output

clean:
	rm -rf data
	rm -rf output

data/%.pkl:
	mkdir -p data
	bin/load-$*.py

data/%.json: all-data
	bin/json-$*.py

output/%.png: data/%.json
	mkdir -p output
	node_modules/.bin/vg2png data/$*.json > output/$*.png
