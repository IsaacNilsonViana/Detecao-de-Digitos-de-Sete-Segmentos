import cv2
from ultralytics import YOLO
from collections import Counter

model_path = '/home/isaacnilsonv/Downloads/TREINAMENTO02/runs/treino_painel/train/weights/best.pt'
model = YOLO(model_path)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro: não foi possivel abrir a câmera.")
    exit()

ROI_X1 = 100 
ROI_Y1 = 150
ROI_X2 = 500
ROI_Y2 = 300

historico_leituras = []
tamanho_historico = 15

while True:
    success, frame = cap.read()

    if not success:
        print("Erro: Não foi possivel ler o frame.")
        break

    cv2.rectangle(frame, (100, 150), (500, 300), (0, 255, 0), 2)


    frame_roi = frame[ROI_Y1:ROI_Y2, ROI_X1:ROI_X2]

    results = model(frame_roi, stream=True, verbose=False)

    deteccoes_frame = []

    for r in results:
        frame_com_deteccoes = r.boxes

        for box in r.boxes:
            confianca = box.conf[0]

            if confianca > 0.5:
                x1_rel = box.xyxy[0][0]
                class_id = box.cls[0]

                deteccoes_frame.append((x1_rel, int(class_id)))

                coords = box.xyxy[0]
                rel_x1, rel_y1, rel_x2, rel_y2 = int(coords[0]), int(coords[1]), int(coords[2]), int(coords[3])

                abs_x1 = rel_x1 + ROI_X1
                abs_y1 = rel_y1 + ROI_Y1
                abs_x2 = rel_x2 + ROI_X1
                abs_y2 = rel_y2 + ROI_Y1


                cv2.rectangle(frame,(abs_x1, abs_y1), (abs_x2, abs_y2),(255,0,0),2)

    deteccoes_frame.sort()

    numero_lido = ""

    for item in deteccoes_frame:
        class_id = item[1]
        char = model.names[class_id]
        numero_lido += char

    historico_leituras.append(numero_lido)

    if len(historico_leituras) > tamanho_historico:
        historico_leituras.pop(0)

    leitura_estavel = ""

    if historico_leituras:
        votos = Counter(historico_leituras).most_common(1)
        if votos:
            leitura_estavel = votos[0][0]

    cv2.putText(frame,leitura_estavel,(50,100), cv2.FONT_HERSHEY_SIMPLEX,3, (0,0,255), 3)

    cv2.imshow("Arena Yolov8 - Pressione 'q' para sair", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("Fechando a arena...")
cap.release()
cv2.destroyAllWindows()