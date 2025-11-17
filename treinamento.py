from ultralytics import YOLO

def main():
    print("Iniciando o 'Ritual de Treinamento' via script Python...")

   # model = YOLO('yolov8n.pt')
    model = YOLO('/home/isaacnilsonv/Downloads/TREINAMENTO02/runs/treino_script/experimento_com_aumento2/weights/best.pt')

    print("Conjurando model.train()...")
    results = model.train(
        data='dataset/data.yaml',
        epochs=100,
        imgsz=640,
        project='runs/treino_script',
        name='experimento_refinamento_100ep',

        degrees=10.0,
        scale=0.3,
        flipud=0.0,
        fliplr=0.0,
        mosaic=1.0
    )
    
    print("Treinamento concluído!")
    print(f"Seu 'best.pt' foi salvo em: {results.save_dir}")

if __name__ == '__main__':
    main()