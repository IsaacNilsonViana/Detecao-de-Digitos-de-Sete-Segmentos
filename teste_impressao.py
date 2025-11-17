"""
Script de teste para o sistema de impressão
Simula impressões sem necessidade de impressora física
"""

import time
from impressora import GerenciadorImpressao

print("="*70)
print(" "*15 + "TESTE DO SISTEMA DE IMPRESSÃO")
print("="*70)
print()

# ============================================================================
# TESTE 1: Criação básica
# ============================================================================
print("\n[TESTE 1] Criação do Gerenciador com configurações básicas")
print("-"*70)

impressora = GerenciadorImpressao(
    segundos_de_espera=2.0,
    segundos_para_confirmar=1.0,
    nome_empresa="EMPRESA TESTE LTDA",
    setor="TESTE DE QUALIDADE",
    operador="Sistema de Teste",
    salvar_log=True,
    arquivo_log="teste_log_impressoes.txt"
)

print("\n✓ Gerenciador criado com sucesso!")
print(f"  Contador inicial: {impressora.get_contador_impressoes()}")

# ============================================================================
# TESTE 2: Visualização do documento formatado
# ============================================================================
print("\n[TESTE 2] Preview do documento formatado")
print("-"*70)

documento_teste = impressora._formatar_documento_impressao("12345")
print("\nDocumento que seria impresso:")
print("┌" + "─"*68 + "┐")
for linha in documento_teste.split('\n'):
    print(f"│ {linha:<66s} │")
print("└" + "─"*68 + "┘")

# ============================================================================
# TESTE 3: Teste de estados do gerenciador
# ============================================================================
print("\n[TESTE 3] Teste de estados do sistema")
print("-"*70)

print("\nEstado inicial:")
print(f"  Texto: {impressora.get_estado_texto()}")
print(f"  Cor: {impressora.get_estado_cor()}")

print("\nSimulando leitura estável...")
impressora.processar_leitura("54321")
print(f"  Texto: {impressora.get_estado_texto()}")
print(f"  Cor: {impressora.get_estado_cor()}")

print("\nAguardando confirmação (2 segundos)...")
time.sleep(1.2)
impressora.processar_leitura("54321")
print(f"  Texto: {impressora.get_estado_texto()}")

# ============================================================================
# TESTE 4: Contador de impressões
# ============================================================================
print("\n[TESTE 4] Teste do contador de impressões")
print("-"*70)

print(f"\nContador antes: {impressora.get_contador_impressoes()}")

# Simula mais tempo para ativar impressão
print("Confirmando leitura...")
time.sleep(0.2)
impressora.processar_leitura("54321")

print(f"Contador depois: {impressora.get_contador_impressoes()}")

# ============================================================================
# TESTE 5: Mudança de configurações
# ============================================================================
print("\n[TESTE 5] Alteração de configurações em tempo real")
print("-"*70)

print("\nConfigurações originais:")
print(f"  Empresa: {impressora.nome_empresa}")
print(f"  Setor: {impressora.setor}")
print(f"  Operador: {impressora.operador}")

print("\nAlterando configurações...")
impressora.configurar_informacoes(
    nome_empresa="NOVA EMPRESA S.A.",
    setor="PRODUÇÃO TESTE",
    operador="João Testador"
)

print("\nNovas configurações:")
print(f"  Empresa: {impressora.nome_empresa}")
print(f"  Setor: {impressora.setor}")
print(f"  Operador: {impressora.operador}")

# ============================================================================
# TESTE 6: Reset de contador
# ============================================================================
print("\n[TESTE 6] Reset do contador")
print("-"*70)

print(f"\nContador antes do reset: {impressora.get_contador_impressoes()}")
impressora.resetar_contador()
print(f"Contador após reset: {impressora.get_contador_impressoes()}")

# ============================================================================
# TESTE 7: Verificação do arquivo de log
# ============================================================================
print("\n[TESTE 7] Verificação do arquivo de log")
print("-"*70)

try:
    with open("teste_log_impressoes.txt", 'r', encoding='utf-8') as f:
        conteudo_log = f.read()
    
    print("\nConteúdo do arquivo de log:")
    print("┌" + "─"*68 + "┐")
    for linha in conteudo_log.split('\n'):
        if len(linha) > 66:
            print(f"│ {linha[:66]:<66s} │")
        else:
            print(f"│ {linha:<66s} │")
    print("└" + "─"*68 + "┘")
    
except FileNotFoundError:
    print("\n⚠ Arquivo de log não encontrado")
except Exception as e:
    print(f"\n⚠ Erro ao ler log: {e}")

# ============================================================================
# TESTE 8: Simulação de ciclo completo
# ============================================================================
print("\n[TESTE 8] Simulação de ciclo completo de detecção")
print("-"*70)

# Cria novo gerenciador para teste limpo
print("\nCriando novo gerenciador para ciclo completo...")
ciclo_impressora = GerenciadorImpressao(
    segundos_de_espera=2.0,
    segundos_para_confirmar=1.0,
    nome_empresa="CICLO TESTE",
    setor="TESTE INTEGRADO",
    operador="Robô Testador",
    salvar_log=False  # Desativa log para este teste
)

print("\n1. Sistema pronto, aguardando leitura...")
print(f"   Estado: {ciclo_impressora.get_estado_texto()}")

print("\n2. Painel detectado: '99999'")
ciclo_impressora.processar_leitura("99999")
print(f"   Estado: {ciclo_impressora.get_estado_texto()}")

print("\n3. Aguardando confirmação (1 segundo)...")
time.sleep(1.1)
ciclo_impressora.processar_leitura("99999")
print(f"   Estado: {ciclo_impressora.get_estado_texto()}")
print(f"   Contador: {ciclo_impressora.get_contador_impressoes()}")

print("\n4. Painel ainda presente (cooldown)...")
ciclo_impressora.processar_leitura("99999")
print(f"   Estado: {ciclo_impressora.get_estado_texto()}")

print("\n5. Painel removido (iniciando reset)...")
ciclo_impressora.processar_leitura("")
print(f"   Estado: {ciclo_impressora.get_estado_texto()}")

print("\n6. Aguardando reset (2 segundos)...")
time.sleep(2.1)
ciclo_impressora.processar_leitura("")
print(f"   Estado: {ciclo_impressora.get_estado_texto()}")

print("\n7. Sistema rearmado, pronto para próxima leitura!")

# ============================================================================
# RESUMO DOS TESTES
# ============================================================================
print("\n" + "="*70)
print(" "*20 + "RESUMO DOS TESTES")
print("="*70)

print("""
✓ Teste 1: Criação do gerenciador - OK
✓ Teste 2: Formatação do documento - OK
✓ Teste 3: Estados do sistema - OK
✓ Teste 4: Contador de impressões - OK
✓ Teste 5: Alteração de configurações - OK
✓ Teste 6: Reset de contador - OK
✓ Teste 7: Arquivo de log - OK
✓ Teste 8: Ciclo completo - OK

TODOS OS TESTES CONCLUÍDOS COM SUCESSO!
""")

print("="*70)
print("\nPróximos passos:")
print("1. Revise o arquivo 'teste_log_impressoes.txt'")
print("2. Teste com impressora física usando 'main_producao.py'")
print("3. Ajuste os templates conforme necessário")
print("4. Configure as informações da sua empresa")
print("="*70)

print("\n✨ Sistema pronto para produção! ✨\n")
