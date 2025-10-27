# Projeto de Detecção de Dígitos em Displays de Sete Segmentos

Este projeto utiliza o modelo YOLOv8 para detecção de dígitos em displays de sete segmentos, com base em um dataset anotado e organizado para tarefas de visão computacional.

## Estrutura do Projeto

- `rodar_camera.py`: Script para rodar a detecção em tempo real usando a câmera.
- `yolov8n.pt`: Peso do modelo YOLOv8 pré-treinado.
- `dataset/`: Pasta contendo o dataset organizado em `train`, `valid` e `test`.
  - `data.yaml`: Arquivo de configuração do dataset.
  - `train/`, `valid/`, `test/`: Subpastas com imagens e labels.
- `runs/`: Resultados de execuções e treinamentos.
- `venv_yolo/`: Ambiente virtual Python para isolamento de dependências.

## Dataset

- **Número de classes:** 12
- **Classes:** '-', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
- **Formato:** YOLO (imagens e labels em pastas separadas)
- **Fonte:** Roboflow
- **Licença:** CC BY 4.0
- **Link para download:** [Roboflow - digit-finder v14](https://universe.roboflow.com/sevensegdigit/digit-finder/dataset/14)

## Como usar

1. Crie e ative o ambiente virtual:
   ```bash
   python3 -m venv venv_yolo
   source venv_yolo/bin/activate
   ```
2. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   # ou instale manualmente: ultralytics, opencv-python, etc.
   ```
3. Baixe o dataset pelo link acima e extraia na pasta `dataset/` se necessário.
4. Execute o script de detecção:
   ```bash
   python rodar_camera.py
   ```

## Referências

- [YOLOv8 - Ultralytics](https://docs.ultralytics.com/)
- [Roboflow - digit-finder](https://universe.roboflow.com/sevensegdigit/digit-finder)
- [Documentação do OpenCV](https://docs.opencv.org/)

## Licença

Este projeto utiliza dados sob a licença CC BY 4.0 conforme especificado pelo Roboflow.
