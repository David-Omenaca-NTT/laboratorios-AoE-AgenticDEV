.PHONY: ayuda verificar specs puertas aceptacion corpus estado referencia

ayuda:
	@echo "make verificar   todo: specs, bateria y puertas"
	@echo "make specs       openspec validate --all"
	@echo "make aceptacion  bateria de aceptacion externa"
	@echo "make puertas     las cuatro puertas de la modalidad"
	@echo "make corpus      regenera el corpus sintetico"
	@echo "make estado      progreso del laboratorio"
	@echo "make referencia  lista los cambios archivados por etapa"

specs:
	OPENSPEC_TELEMETRY=0 DO_NOT_TRACK=1 openspec validate --all

aceptacion:
	python3 -m pytest aceptacion/ -q

puertas:
	python3 -m herramientas.gates_sdd todos

verificar: specs aceptacion puertas

corpus:
	python3 herramientas/generar_corpus.py

estado:
	python3 -m abaco_cli estado

referencia:
	@ls -1 openspec/changes/archive/
