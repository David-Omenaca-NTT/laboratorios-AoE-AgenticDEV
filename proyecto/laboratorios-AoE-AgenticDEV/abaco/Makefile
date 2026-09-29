.PHONY: ayuda test check estado cobertura eval mcp imagen corpus

ayuda:
	@echo "make test       ejecuta la suite"
	@echo "make check      verifica la estacion activa"
	@echo "make estado     muestra el progreso del laboratorio"
	@echo "make eval       evalua el agente de staffing"
	@echo "make mcp        inicia el servidor MCP de Ábaco"
	@echo "make imagen     construye la imagen OCI"

test:
	python3 -m pytest tests/ -q

cobertura:
	python3 -m pytest tests/ -q --cov=src/abaco --cov-report=term-missing

estado:
	python3 -m abaco_cli estado

check:
	python3 -m abaco_cli check

eval:
	python3 -m agentes.staffing.evaluar --guardar

mcp:
	python3 -m agentes.mcp_abaco.servidor

corpus:
	python3 herramientas/generar_corpus.py

imagen:
	podman build -t abaco:dev . || docker build -t abaco:dev .
