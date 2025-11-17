# Projeto de Detecção e Leitura de Displays de Sete Segmentos com YOLOv8

Sistema completo de detecção, leitura e impressão de valores exibidos em displays de sete segmentos (como multímetros digitais) utilizando YOLOv8 e OpenCV. O sistema captura imagens via webcam, detecta dígitos em tempo real, estabiliza a leitura e gerencia impressões automáticas.

## Características

- **Detecção em Tempo Real**: Captura e processa frames da câmera em tempo real
- **Leitura Estabilizada**: Sistema de histórico e votação para garantir leituras consistentes
- **ROI Configurável**: Define região de interesse para otimizar a detecção
- **Gerenciamento de Impressão**: Sistema inteligente com cooldown e confirmação de leituras
- **Logging**: Registro automático de todas as impressões com timestamp
- **Treinamento Customizado**: Scripts para treinar o modelo com dados próprios

## Estrutura do Projeto

```
TREINAMENTO02/
├── main.py                    # Script principal de detecção e leitura via câmera
├── treinamento.py             # Script para treinar o modelo YOLOv8
├── impressora.py              # Gerenciador de impressão com sistema de cooldown
├── teste_impressao.py         # Script de teste do sistema de impressão
├── test.ipynb                 # Notebook Jupyter para experimentos
├── yolov8n.pt                 # Modelo YOLOv8 base pré-treinado
├── requirements.txt           # Dependências do projeto
├── log_impressoes.txt         # Log de impressões realizadas
├── dataset/                   # Dataset para treinamento
│   ├── data.yaml             # Configuração do dataset
│   ├── train/                # Imagens e labels de treino
│   ├── valid/                # Imagens e labels de validação
│   └── test/                 # Imagens e labels de teste
├── runs/                     # Resultados de treinamentos
│   ├── treino_painel/        # Experimentos de treinamento
│   └── treino_script/        # Treinamentos via script
│       ├── experimento_com_aumento2/
│       └── experimento_refinamento_100ep/  # Modelo refinado (melhor)
└── venv_yolo/                # Ambiente virtual Python
```

## Dataset

- **Número de classes**: 12
- **Classes detectadas**: `-`, `.`, `0`, `1`, `2`, `3`, `4`, `5`, `6`, `7`, `8`, `9`
- **Formato**: YOLO (imagens e anotações em formato .txt)
- **Fonte**: [Roboflow - digit-finder v14](https://universe.roboflow.com/sevensegdigit/digit-finder/dataset/14)
- **Licença**: CC BY 4.0
- **Organização**:
  - Train: Imagens de treinamento
  - Valid: Imagens de validação
  - Test: Imagens de teste

## Como Usar

### 1. Configuração do Ambiente

```bash
# Clone ou navegue até o diretório do projeto
cd /home/isaacnilsonv/Downloads/TREINAMENTO02

# Crie e ative o ambiente virtual
python3 -m venv venv_yolo
source venv_yolo/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### 2. Executar o Sistema de Detecção

```bash
# Execute o script principal
python main.py
```

**Funcionalidades do `main.py`**:

- Captura frames da webcam (pode ser configurada para IP camera)
- Define ROI (Region of Interest) no frame
- Detecta dígitos usando modelo YOLOv8 treinado
- Estabiliza leituras usando histórico de 15 frames
- Gerencia impressões automáticas com confirmação
- Pressione 'q' para sair

### 3. Treinar o Modelo (Opcional)

```bash
# Execute o script de treinamento
python treinamento.py
```

**Parâmetros de treinamento configurados**:

- **Epochs**: 100
- **Image Size**: 640x640
- **Data Augmentation**:
  - Rotação: ±10°
  - Escala: ±30%
  - Mosaic: 100%
  - Flip horizontal/vertical desabilitado

### 4. Testar Sistema de Impressão

```bash
# Teste o gerenciador sem impressora física
python teste_impressao.py
```

## Configurações Principais

### ROI (Region of Interest)

Editável em `main.py`:

```python
ROI_X1 = 100   # Coordenada X inicial
ROI_Y1 = 150   # Coordenada Y inicial
ROI_X2 = 500   # Coordenada X final
ROI_Y2 = 300   # Coordenada Y final
```

### Gerenciador de Impressão

Configurável em `main.py`:

```python
impressora = GerenciadorImpressao(
    segundos_de_espera=3.0,        # Cooldown após impressão
    segundos_para_confirmar=2.0    # Tempo para confirmar leitura
)
```

### Modelo YOLOv8

Modelo treinado localizado em:

```python
model_path = 'runs/treino_script/experimento_refinamento_100ep/weights/best.pt'
```

### Fonte de Vídeo

Em `main.py`, escolha entre:

```python
cap = cv2.VideoCapture(0)                        # Webcam local
# cap = cv2.VideoCapture("http://IP:PORT/video") # IP Camera
```

## Sistema de Impressão

O `GerenciadorImpressao` implementa um sistema robusto:

1. **Confirmação de Leitura**: Aguarda estabilização por X segundos
2. **Cooldown**: Período de espera após impressão
3. **Reset Automático**: Reativa sistema quando display é removido
4. **Logging**: Registra todas impressões com data/hora
5. **Estados Visuais**:
   - Verde: Pronto para ler
   - Amarelo: Confirmando leitura
   - Laranja: Cooldown ativo

## Resultados do Treinamento

O modelo foi refinado através de múltiplos experimentos:

- **Modelo Base**: `yolov8n.pt` (COCO pré-treinado)
- **Experimento com Aumento**: Data augmentation inicial
- **Refinamento 100 epochs**: Modelo final otimizado (melhor performance)

Resultados disponíveis em:

- `runs/treino_script/experimento_refinamento_100ep/`
- Métricas, gráficos e checkpoints salvos automaticamente

## Dependências

```
ultralytics  # YOLOv8
opencv-python # Processamento de imagens
torch        # PyTorch (backend do YOLO)
numpy        # Operações numéricas
```

## Logs

Todas as impressões são registradas em `log_impressoes.txt` com:

- Data e hora
- Valor lido
- Contador de impressões
- Informações da empresa/setor (se configurado)

## Troubleshooting

**Câmera não abre**:

- Verifique se a câmera está conectada
- Teste com `cv2.VideoCapture(0)` para webcam local
- Para IP camera, verifique a URL e conectividade

**Detecções imprecisas**:

- Ajuste o ROI para focar no display
- Verifique iluminação adequada
- Aumente o `tamanho_historico` para mais estabilidade
- Considere retreinar o modelo com imagens do seu ambiente

**Modelo não encontrado**:

- Verifique o caminho em `model_path`
- Use o modelo base `yolov8n.pt` ou treine um novo

## Referências

- [YOLOv8 Documentation - Ultralytics](https://docs.ultralytics.com/)
- [OpenCV Documentation](https://docs.opencv.org/)
- [Roboflow - digit-finder Dataset](https://universe.roboflow.com/sevensegdigit/digit-finder)
- [PyTorch](https://pytorch.org/)
