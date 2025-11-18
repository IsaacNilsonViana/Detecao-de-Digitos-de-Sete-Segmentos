import time
import subprocess
from collections import Counter
from datetime import datetime
import platform
import os

class GerenciadorImpressao:

    def __init__(self, segundos_de_espera= 3.0, segundos_para_confirmar=2.0):

        self.segundos_de_espera = segundos_de_espera
        self.segundos_para_confirmar = segundos_para_confirmar

        self.pode_imprimir = True
        self.ultima_leitura_impressa = ""
        self.clooldown_start_time= None

        self.leitura_candidata = None
        self.candidata_start_time = None

        self.estado_atual_texto = "Pronto"
        self.estado_atual_cor = (0, 255, 0)
        
        print(f"Gerenciador de Impressão iniciado (Confirmação: {self.segundos_para_confirmar}s, Reset: {self.segundos_de_espera}s)")
    
    def processar_leitura(self, leitura_estavel):
        
        start = time.time()
        if self.pode_imprimir:
            if leitura_estavel != "":
                if leitura_estavel != self.ultima_leitura_impressa:
                    if leitura_estavel != self.leitura_candidata:
                        self.leitura_candidata = leitura_estavel
                        self.candidata_start_time = time.time()
                        self.estado_atual_texto = f"Confirmando: {leitura_estavel}"
                        self.estado_atual_cor = (255,255,0)
                    elif self.candidata_start_time is not None:
                        tempo_decorrido = time.time() - self.candidata_start_time

                        if tempo_decorrido > self.segundos_para_confirmar:

                            self._disparar_impressao(self.leitura_candidata, start)

                            self.pode_imprimir = False
                            self.ultima_leitura_impressa = self.leitura_candidata
                            self.leitura_candidata = None
                            self.candidata_start_time = None
                            
                        
                else:
                    self.estado_atual_texto = "Ja Impresso: Remova o Painel."
                    self.estado_atual_cor = (0,165,255)
            else:
                if self.leitura_candidata is not None:
                    print("Confirmação Cancelada: Painel Removido")
                self.leitura_candidata = None
                self.candidata_start_time = None
                self.estado_atual_texto = "Pronto"
                self.estado_atual_cor = (0,255,0)

        else:
            self.estado_atual_texto = "Cooldown: REmova o Painel"
            self.estado_atual_cor = (0,165,2550
                                     )
            if leitura_estavel == "":
                if self.clooldown_start_time is None:
                    self.clooldown_start_time = time.time()
                    print("Timer de restet iniciado...")

                tempo_decorrido = time.time() - self.clooldown_start_time
                if tempo_decorrido > self.segundos_de_espera:
                    self.pode_imprimir = True
                    self.clooldown_start_time = None
                    self.leitura_candidata = None
                    self.candidata_start_time = None
                    self.ultima_leitura_impressa = ""
                    
                    print("Sistema Rearmado. Pronto para imprimir a próxima leitura")

            else:
                if self.clooldown_start_time is not None:
                    print("Reset cancelado (painel Detectado).")
                self.clooldown_start_time = None

    def _disparar_impressao(self, numero, start):
        print("="*30)
        print(f"Imprimindo Leitura: {numero} !")

        agora = datetime.now()
        data = agora.strftime("%d/%m/%Y")
        hora = agora.strftime("%H:%M:%S")
        
        end = time.time()
        ping = end - start
        

        texto_impressao = f"""

Posto Amigao Capinzal

Data: {data}
Hora: {hora}
ping: {f"{ping:.5f}"}

==============================

LEITURA DETECTADA: {numero}

==============================

Informacoes Adicionais:

Endereco:
Ac. Cidade Alta - 2397
Sao Cristovao,
Capinzal - SC 
89665-000
(49) 3555-3545



,
"""
        
        comando_corte = b'\x1D\x56\x00'

        try:
            sistema = platform.system()
            if sistema == "Linux":
                subprocess.run(
                ['lp'],
                input=texto_impressao.encode('utf-8') + comando_corte,
                check=True
                )
                print("Enviado para a fila de impressão local com sucesso.")
            elif sistema == "Windows":
                print("ATENÇÃO: A impressão direta no Windows requer a lib win32print.")
                print("O texto a ser impresso seria:", texto_impressao)

        except subprocess.CalledProcessError as e:
            print(f"[ERRO DE IMPRESSÃO] O comando 'lp' Falhou: {e}")
        except FileNotFoundError:
            print("[ERRO DE IMPRESSÃO] comando 'lp' não encontrado.")
            print("Verifique se o sistema de impressão esta instalado")
        except Exception as e:
            print(f"[ERRO INESPERADO] ao tentar imprimir: {e}")

        print("="*30)

    def get_estado_texto(self):
        return self.estado_atual_texto
    
    def get_estado_cor(self):
        return self.estado_atual_cor